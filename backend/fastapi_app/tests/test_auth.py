from datetime import datetime, timezone

import pytest

from fastapi_app.schemas.user import UserRead
from fastapi_app.tests.conftest import make_user
from fastapi_app.utils.exceptions import ConflictError, UnauthorizedError


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
        post_count=0,
    )


@pytest.mark.asyncio
async def test_register_success(auth_client):
    ac, mock_svc = auth_client
    user_data = _user_read()
    mock_svc.register.return_value = user_data

    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["email"] == user_data.email
    mock_svc.register.assert_called_once()


@pytest.mark.asyncio
async def test_register_duplicate_email(auth_client):
    ac, mock_svc = auth_client
    mock_svc.register.side_effect = ConflictError("Email is already registered")

    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "existing@example.com",
            "username": "newuser",
            "password": "password123",
        },
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_duplicate_username(auth_client):
    ac, mock_svc = auth_client
    mock_svc.register.side_effect = ConflictError("Username is already taken")

    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "email": "new@example.com",
            "username": "taken",
            "password": "password123",
        },
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_invalid_email(auth_client):
    ac, mock_svc = auth_client

    response = await ac.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "username": "user", "password": "password123"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_password_too_short(auth_client):
    ac, mock_svc = auth_client

    response = await ac.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "user", "password": "short"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(auth_client):
    ac, mock_svc = auth_client
    user = make_user()
    mock_svc.login.return_value = (user, "access-token", "refresh-token")

    response = await ac.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "access_token" in response.cookies or body["message"] == "Login successful"
    mock_svc.login.assert_called_once()


@pytest.mark.asyncio
async def test_login_wrong_password(auth_client):
    ac, mock_svc = auth_client
    mock_svc.login.side_effect = UnauthorizedError("Invalid email or password")

    response = await ac.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_email(auth_client):
    ac, mock_svc = auth_client
    mock_svc.login.side_effect = UnauthorizedError("Invalid email or password")

    response = await ac.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "password123"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_success(auth_client):
    ac, mock_svc = auth_client

    response = await ac.post("/api/v1/auth/logout")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Logged out successfully"


@pytest.mark.asyncio
async def test_refresh_missing_cookie(auth_client):
    ac, mock_svc = auth_client

    response = await ac.post("/api/v1/auth/refresh")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_invalid_token(auth_client):
    ac, mock_svc = auth_client
    mock_svc.refresh.side_effect = UnauthorizedError("Invalid or expired refresh token")
    ac.cookies.set("refresh_token", "invalid-token")

    response = await ac.post("/api/v1/auth/refresh")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_success(auth_client):
    ac, mock_svc = auth_client
    mock_svc.refresh.return_value = ("new-access", "new-refresh")
    ac.cookies.set("refresh_token", "valid-refresh-token")

    response = await ac.post("/api/v1/auth/refresh")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    mock_svc.refresh.assert_called_once_with("valid-refresh-token")
