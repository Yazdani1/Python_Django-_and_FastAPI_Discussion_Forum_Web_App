import uuid
from datetime import datetime, timezone

import pytest

from fastapi_app.schemas.post import PostListItem, PostRead
from fastapi_app.schemas.user import UserPublic
from fastapi_app.tests.conftest import make_user
from fastapi_app.utils.exceptions import ForbiddenError, NotFoundError
from fastapi_app.utils.responses import MetaData


def _author() -> UserPublic:
    user = make_user()
    return UserPublic(
        id=user.id, username=user.username, avatar_url=None, role=user.role
    )


def _post_read(post_id: uuid.UUID | None = None) -> PostRead:
    return PostRead(
        id=post_id or uuid.uuid4(),
        title="Test Post Title",
        content="This is the post content with enough characters.",
        author=_author(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def _post_list_item() -> PostListItem:
    return PostListItem(
        id=uuid.uuid4(),
        title="Test Post Title",
        preview="This is the post preview...",
        author=_author(),
        created_at=datetime.now(timezone.utc),
    )


@pytest.mark.asyncio
async def test_list_posts_empty(anon_post_client):
    ac, mock_svc = anon_post_client
    meta = MetaData(page=1, page_size=20, total=0, total_pages=0)
    mock_svc.list_posts.return_value = ([], meta)

    response = await ac.get("/api/v1/posts")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"] == []
    assert body["meta"]["total"] == 0


@pytest.mark.asyncio
async def test_list_posts_with_results(anon_post_client):
    ac, mock_svc = anon_post_client
    items = [_post_list_item(), _post_list_item()]
    meta = MetaData(page=1, page_size=20, total=2, total_pages=1)
    mock_svc.list_posts.return_value = (items, meta)

    response = await ac.get("/api/v1/posts?search=test")

    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 2
    mock_svc.list_posts.assert_called_once()


@pytest.mark.asyncio
async def test_create_post_success(post_client):
    ac, mock_svc = post_client
    post = _post_read()
    mock_svc.create_post.return_value = post

    response = await ac.post(
        "/api/v1/posts",
        json={
            "title": "My New Post Title",
            "content": "This is the content of my new post.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["title"] == "Test Post Title"
    mock_svc.create_post.assert_called_once()


@pytest.mark.asyncio
async def test_create_post_title_too_short(post_client):
    ac, mock_svc = post_client

    response = await ac.post(
        "/api/v1/posts",
        json={"title": "Hi", "content": "This is valid content."},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_post_unauthenticated(anon_post_client):
    ac, mock_svc = anon_post_client

    response = await ac.post(
        "/api/v1/posts",
        json={"title": "My New Post Title", "content": "Some content here."},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_post_success(anon_post_client):
    ac, mock_svc = anon_post_client
    post_id = uuid.uuid4()
    post = _post_read(post_id)
    mock_svc.get_post.return_value = post

    response = await ac.get(f"/api/v1/posts/{post_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["id"] == str(post_id)
    mock_svc.get_post.assert_called_once_with(post_id, None)


@pytest.mark.asyncio
async def test_get_post_not_found(anon_post_client):
    ac, mock_svc = anon_post_client
    post_id = uuid.uuid4()
    mock_svc.get_post.side_effect = NotFoundError("Post")

    response = await ac.get(f"/api/v1/posts/{post_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_post_success(post_client):
    ac, mock_svc = post_client
    post_id = uuid.uuid4()
    post = _post_read(post_id)
    post.title = "Updated Title Here"
    mock_svc.update_post.return_value = post

    response = await ac.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Updated Title Here"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["title"] == "Updated Title Here"


@pytest.mark.asyncio
async def test_update_post_forbidden(post_client):
    ac, mock_svc = post_client
    post_id = uuid.uuid4()
    mock_svc.update_post.side_effect = ForbiddenError(
        "You can only edit your own posts"
    )

    response = await ac.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Some Valid Title"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_post_success(post_client):
    ac, mock_svc = post_client
    post_id = uuid.uuid4()
    mock_svc.delete_post.return_value = None

    response = await ac.delete(f"/api/v1/posts/{post_id}")

    assert response.status_code == 204
    mock_svc.delete_post.assert_called_once()


@pytest.mark.asyncio
async def test_delete_post_forbidden(post_client):
    ac, mock_svc = post_client
    post_id = uuid.uuid4()
    mock_svc.delete_post.side_effect = ForbiddenError(
        "You can only delete your own posts"
    )

    response = await ac.delete(f"/api/v1/posts/{post_id}")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_post_not_found(post_client):
    ac, mock_svc = post_client
    post_id = uuid.uuid4()
    mock_svc.delete_post.side_effect = NotFoundError("Post")

    response = await ac.delete(f"/api/v1/posts/{post_id}")

    assert response.status_code == 404
