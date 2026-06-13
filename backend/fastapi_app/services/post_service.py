import uuid
from datetime import date

from fastapi_app.enums import ROLE_LEVELS, UserRole
from fastapi_app.models.post import Post
from fastapi_app.models.user import User
from fastapi_app.repositories.post_repository import PostRepository
from fastapi_app.schemas.post import PostCreate, PostListItem, PostRead, PostUpdate
from fastapi_app.services.base import BaseService
from fastapi_app.utils.exceptions import ForbiddenError, NotFoundError
from fastapi_app.utils.responses import MetaData


class PostService(BaseService[Post, PostRepository]):
    async def create_post(self, author: User, data: PostCreate) -> PostRead:
        post = await self._repo.create(
            title=data.title,
            content=data.content,
            author_id=author.id,
        )
        post = await self._repo.get_with_author(post.id)
        return PostRead.model_validate(post)

    async def get_post(self, post_id: uuid.UUID) -> PostRead:
        post = await self._repo.get_with_author(post_id)
        if not post:
            raise NotFoundError("Post")
        return PostRead.model_validate(post)

    async def list_posts(
        self,
        *,
        search: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[PostListItem], MetaData]:
        posts, meta = await self._repo.list_with_authors(
            search=search,
            date_from=date_from,
            date_to=date_to,
            page=page,
            page_size=page_size,
        )
        items = [
            PostListItem(
                id=p.id,
                title=p.title,
                preview=p.content[:200],
                author=p.author,
                created_at=p.created_at,
            )
            for p in posts
        ]
        return items, meta

    async def update_post(
        self, post_id: uuid.UUID, current_user: User, data: PostUpdate
    ) -> PostRead:
        post = await self._repo.get_with_author(post_id)
        if not post:
            raise NotFoundError("Post")

        is_owner = post.author_id == current_user.id
        is_privileged = (
            ROLE_LEVELS.get(current_user.role, 0) >= ROLE_LEVELS[UserRole.MODERATOR]
        )
        if not is_owner and not is_privileged:
            raise ForbiddenError("You can only edit your own posts")

        updates: dict = {}
        if data.title is not None:
            updates["title"] = data.title
        if data.content is not None:
            updates["content"] = data.content

        if updates:
            await self._repo.update(post, **updates)
            post = await self._repo.get_with_author(post_id)

        return PostRead.model_validate(post)

    async def delete_post(self, post_id: uuid.UUID, current_user: User) -> None:
        post = await self._repo.get_by_id(post_id)
        if not post:
            raise NotFoundError("Post")

        is_owner = post.author_id == current_user.id
        is_privileged = (
            ROLE_LEVELS.get(current_user.role, 0) >= ROLE_LEVELS[UserRole.MODERATOR]
        )
        if not is_owner and not is_privileged:
            raise ForbiddenError("You can only delete your own posts")

        await self._repo.delete(post)
