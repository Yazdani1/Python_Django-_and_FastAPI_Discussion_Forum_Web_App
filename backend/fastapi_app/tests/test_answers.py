import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from fastapi_app.schemas.answer import AnswerRead
from fastapi_app.schemas.user import UserPublic
from fastapi_app.tests.conftest import make_user
from fastapi_app.utils.exceptions import ForbiddenError, NotFoundError


def _author() -> UserPublic:
    user = make_user()
    return UserPublic(
        id=user.id, username=user.username, avatar_url=None, role=user.role
    )


def _answer_read(answer_id: uuid.UUID | None = None) -> AnswerRead:
    return AnswerRead(
        id=answer_id or uuid.uuid4(),
        content="This is a valid answer with enough content.",
        author=_author(),
        post_id=uuid.uuid4(),
        vote_count=0,
        user_vote=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_answer_service():
    return AsyncMock()


@pytest.fixture
async def answer_client(mock_answer_service, test_user):
    from fastapi_app.main import app
    from fastapi_app.api.v1.dependencies import get_answer_service
    from fastapi_app.core.dependencies import get_current_user
    from httpx import ASGITransport, AsyncClient

    app.dependency_overrides[get_answer_service] = lambda: mock_answer_service
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac, mock_answer_service
    app.dependency_overrides.pop(get_answer_service, None)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
async def anon_answer_client(mock_answer_service):
    from fastapi_app.main import app
    from fastapi_app.api.v1.dependencies import get_answer_service
    from httpx import ASGITransport, AsyncClient

    app.dependency_overrides[get_answer_service] = lambda: mock_answer_service
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac, mock_answer_service
    app.dependency_overrides.pop(get_answer_service, None)


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_answers(anon_answer_client):
    ac, mock_svc = anon_answer_client
    post_id = uuid.uuid4()
    mock_svc.list_answers.return_value = [_answer_read(), _answer_read()]

    response = await ac.get(f"/api/v1/posts/{post_id}/answers")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 2


@pytest.mark.asyncio
async def test_add_answer_success(answer_client):
    ac, mock_svc = answer_client
    post_id = uuid.uuid4()
    answer = _answer_read()
    mock_svc.add_answer.return_value = answer

    response = await ac.post(
        f"/api/v1/posts/{post_id}/answers",
        json={"content": "This is a detailed and valid answer."},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    mock_svc.add_answer.assert_called_once()


@pytest.mark.asyncio
async def test_add_answer_too_short(answer_client):
    ac, mock_svc = answer_client
    post_id = uuid.uuid4()

    response = await ac.post(
        f"/api/v1/posts/{post_id}/answers",
        json={"content": "Short"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_answer_unauthenticated(anon_answer_client):
    ac, mock_svc = anon_answer_client
    post_id = uuid.uuid4()

    response = await ac.post(
        f"/api/v1/posts/{post_id}/answers",
        json={"content": "This is a valid answer content."},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_answer_success(answer_client):
    ac, mock_svc = answer_client
    answer_id = uuid.uuid4()
    answer = _answer_read(answer_id)
    mock_svc.update_answer.return_value = answer

    response = await ac.put(
        f"/api/v1/answers/{answer_id}",
        json={"content": "Updated answer with sufficient length."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    mock_svc.update_answer.assert_called_once()


@pytest.mark.asyncio
async def test_update_answer_forbidden(answer_client):
    ac, mock_svc = answer_client
    answer_id = uuid.uuid4()
    mock_svc.update_answer.side_effect = ForbiddenError(
        "You can only edit your own answers"
    )

    response = await ac.put(
        f"/api/v1/answers/{answer_id}",
        json={"content": "Updated answer content here."},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_answer_success(answer_client):
    ac, mock_svc = answer_client
    answer_id = uuid.uuid4()
    mock_svc.delete_answer.return_value = None

    response = await ac.delete(f"/api/v1/answers/{answer_id}")

    assert response.status_code == 204
    mock_svc.delete_answer.assert_called_once()


@pytest.mark.asyncio
async def test_delete_answer_not_found(answer_client):
    ac, mock_svc = answer_client
    answer_id = uuid.uuid4()
    mock_svc.delete_answer.side_effect = NotFoundError("Answer")

    response = await ac.delete(f"/api/v1/answers/{answer_id}")

    assert response.status_code == 404
