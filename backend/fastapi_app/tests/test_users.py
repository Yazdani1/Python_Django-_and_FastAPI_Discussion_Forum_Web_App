import uuid
from datetime import datetime, timezone

import pytest
from httpx import AsyncClient

from fastapi_app.schemas.user import UserRead
from fastapi_app.tests.conftest import make_user
from fastapi_app.utils.exceptions import ConflictError


def _user_read(user=None) -> UserRead:
    u = user or make_user()
    return UserRead(
        id=u.id,
        email=u.email,
        username=u.username,
        role=u.role,
        avatar_url=None,
        bio=None,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        post_count=3,
    )


@pytest.mark.asyncio
async def test_get_my_profile(user_client):
    ac, mock_svc = user_client
    profile = _user_read()
    mock_svc.get_profile.return_value = profile

    response = await ac.get("/api/v1/users/me")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["post_count"] == 3
    mock_svc.get_profile.assert_called_once()


@pytest.mark.asyncio
async def test_get_my_profile_unauthenticated(anon_post_client):
    ac, _ = anon_post_client

    response = await ac.get("/api/v1/users/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_profile_success(user_client):
    ac, mock_svc = user_client
    profile = _user_read()
    profile.username = "newname"
    profile.bio = "My bio"
    mock_svc.update_profile.return_value = profile

    response = await ac.patch(
        "/api/v1/users/me",
        json={"username": "newname", "bio": "My bio"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["username"] == "newname"
    mock_svc.update_profile.assert_called_once()


@pytest.mark.asyncio
async def test_update_profile_duplicate_username(user_client):
    ac, mock_svc = user_client
    mock_svc.update_profile.side_effect = ConflictError("Username is already taken")

    response = await ac.patch(
        "/api/v1/users/me",
        json={"username": "taken"},
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_profile_empty_body(user_client):
    ac, mock_svc = user_client
    profile = _user_read()
    mock_svc.update_profile.return_value = profile

    response = await ac.patch("/api/v1/users/me", json={})

    assert response.status_code == 200
