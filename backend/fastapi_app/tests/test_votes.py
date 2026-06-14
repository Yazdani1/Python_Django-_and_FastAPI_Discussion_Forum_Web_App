import uuid
from unittest.mock import AsyncMock

import pytest

from fastapi_app.schemas.vote import VoteResult


@pytest.fixture
def mock_vote_service():
    return AsyncMock()


@pytest.fixture
async def vote_client(mock_vote_service, test_user):
    from fastapi_app.main import app
    from fastapi_app.api.v1.dependencies import get_vote_service
    from fastapi_app.core.dependencies import get_current_user
    from httpx import ASGITransport, AsyncClient

    app.dependency_overrides[get_vote_service] = lambda: mock_vote_service
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac, mock_vote_service
    app.dependency_overrides.pop(get_vote_service, None)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_vote_post_upvote(vote_client):
    ac, mock_svc = vote_client
    post_id = uuid.uuid4()
    mock_svc.vote_post.return_value = VoteResult(vote_count=1, user_vote="up")

    response = await ac.post(
        f"/api/v1/posts/{post_id}/vote",
        json={"vote_type": "up"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["vote_count"] == 1
    assert body["data"]["user_vote"] == "up"
    mock_svc.vote_post.assert_called_once()


@pytest.mark.asyncio
async def test_vote_post_downvote(vote_client):
    ac, mock_svc = vote_client
    post_id = uuid.uuid4()
    mock_svc.vote_post.return_value = VoteResult(vote_count=-1, user_vote="down")

    response = await ac.post(
        f"/api/v1/posts/{post_id}/vote",
        json={"vote_type": "down"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["vote_count"] == -1
    assert body["data"]["user_vote"] == "down"


@pytest.mark.asyncio
async def test_remove_post_vote(vote_client):
    ac, mock_svc = vote_client
    post_id = uuid.uuid4()
    mock_svc.remove_post_vote.return_value = VoteResult(vote_count=0, user_vote=None)

    response = await ac.delete(f"/api/v1/posts/{post_id}/vote")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["user_vote"] is None
    mock_svc.remove_post_vote.assert_called_once()


@pytest.mark.asyncio
async def test_vote_unauthenticated():
    from fastapi_app.main import app
    from httpx import ASGITransport, AsyncClient

    post_id = uuid.uuid4()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            f"/api/v1/posts/{post_id}/vote",
            json={"vote_type": "up"},
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_vote_answer_upvote(vote_client):
    ac, mock_svc = vote_client
    answer_id = uuid.uuid4()
    mock_svc.vote_answer.return_value = VoteResult(vote_count=1, user_vote="up")

    response = await ac.post(
        f"/api/v1/answers/{answer_id}/vote",
        json={"vote_type": "up"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["vote_count"] == 1
    mock_svc.vote_answer.assert_called_once()


@pytest.mark.asyncio
async def test_remove_answer_vote(vote_client):
    ac, mock_svc = vote_client
    answer_id = uuid.uuid4()
    mock_svc.remove_answer_vote.return_value = VoteResult(vote_count=0, user_vote=None)

    response = await ac.delete(f"/api/v1/answers/{answer_id}/vote")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["user_vote"] is None
