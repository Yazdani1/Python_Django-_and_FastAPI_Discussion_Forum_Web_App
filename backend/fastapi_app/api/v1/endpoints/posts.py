import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query, Response, status

from fastapi_app.api.v1.dependencies import get_post_service
from fastapi_app.core.cache import cache_delete, cache_delete_pattern, cache_get, cache_set
from fastapi_app.core.dependencies import get_current_user
from fastapi_app.models.user import User
from fastapi_app.schemas.post import PostCreate, PostListItem, PostRead, PostUpdate
from fastapi_app.services.post_service import PostService
from fastapi_app.utils.responses import ApiResponse

router = APIRouter(prefix="/posts", tags=["posts"])

_LIST_TTL = 60       # seconds — list cache
_DETAIL_TTL = 300    # seconds — single post cache


def _list_key(search: str | None, date_from: date | None, date_to: date | None, page: int, page_size: int) -> str:
    return f"posts:list:{search}:{date_from}:{date_to}:{page}:{page_size}"


def _detail_key(post_id: uuid.UUID) -> str:
    return f"posts:detail:{post_id}"


@router.get("", response_model=ApiResponse[list[PostListItem]])
async def list_posts(
    response: Response,
    search: str | None = Query(default=None, max_length=100),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: PostService = Depends(get_post_service),
) -> ApiResponse[list[PostListItem]]:
    cache_key = _list_key(search, date_from, date_to, page, page_size)
    cached = await cache_get(cache_key)
    if cached:
        response.headers["X-Cache"] = "HIT"
        return ApiResponse(**cached)

    items, meta = await service.list_posts(
        search=search,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size,
    )
    result = ApiResponse.ok(data=items, meta=meta)
    await cache_set(cache_key, result.model_dump(mode="json"), ttl=_LIST_TTL)
    response.headers["X-Cache"] = "MISS"
    return result


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[PostRead]
)
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
) -> ApiResponse[PostRead]:
    post = await service.create_post(current_user, data)
    await cache_delete_pattern("posts:list:*")
    return ApiResponse.created(data=post, message="Post created successfully")


@router.get("/{post_id}", response_model=ApiResponse[PostRead])
async def get_post(
    post_id: uuid.UUID,
    response: Response,
    service: PostService = Depends(get_post_service),
) -> ApiResponse[PostRead]:
    cache_key = _detail_key(post_id)
    cached = await cache_get(cache_key)
    if cached:
        response.headers["X-Cache"] = "HIT"
        return ApiResponse(**cached)

    post = await service.get_post(post_id)
    result = ApiResponse.ok(data=post)
    await cache_set(cache_key, result.model_dump(mode="json"), ttl=_DETAIL_TTL)
    response.headers["X-Cache"] = "MISS"
    return result


@router.put("/{post_id}", response_model=ApiResponse[PostRead])
async def update_post(
    post_id: uuid.UUID,
    data: PostUpdate,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
) -> ApiResponse[PostRead]:
    post = await service.update_post(post_id, current_user, data)
    await cache_delete(_detail_key(post_id))
    await cache_delete_pattern("posts:list:*")
    return ApiResponse.ok(data=post, message="Post updated successfully")


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
) -> None:
    await service.delete_post(post_id, current_user)
    await cache_delete(_detail_key(post_id))
    await cache_delete_pattern("posts:list:*")
