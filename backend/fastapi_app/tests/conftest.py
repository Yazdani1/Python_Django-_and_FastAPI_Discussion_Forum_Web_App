import os
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("APP_SECRET_KEY", "test-secret-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test_db")
os.environ.setdefault("DATABASE_PASSWORD", "test")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
os.environ.setdefault("CORS_ALLOWED_ORIGINS", '["http://localhost:5173"]')

from fastapi_app.main import app  # noqa: E402
from fastapi_app.api.v1.dependencies import (  # noqa: E402
    get_auth_service,
    get_user_service,
    get_post_service,
)
from fastapi_app.core.dependencies import get_current_user  # noqa: E402
from fastapi_app.enums import UserRole  # noqa: E402
from fastapi_app.models.user import User  # noqa: E402


def make_user(
    *,
    user_id: uuid.UUID | None = None,
    email: str = "test@example.com",
    username: str = "testuser",
    role: UserRole = UserRole.USER,
) -> User:
    user = User()
    user.id = user_id or uuid.uuid4()
    user.email = email
    user.username = username
    user.hashed_password = "hashed"
    user.role = role
    user.avatar_url = None
    user.bio = None
    user.is_active = True
    user.created_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    return user


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_auth_service():
    return AsyncMock()


@pytest.fixture
def mock_user_service():
    return AsyncMock()


@pytest.fixture
def mock_post_service():
    return AsyncMock()


@pytest.fixture
def test_user() -> User:
    return make_user()


@pytest.fixture
def admin_user() -> User:
    return make_user(username="admin", email="admin@example.com", role=UserRole.ADMIN)


@pytest.fixture
async def auth_client(mock_auth_service):
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac, mock_auth_service
    app.dependency_overrides.pop(get_auth_service, None)


@pytest.fixture
async def user_client(mock_user_service, test_user):
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac, mock_user_service
    app.dependency_overrides.pop(get_user_service, None)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
async def post_client(mock_post_service, test_user):
    app.dependency_overrides[get_post_service] = lambda: mock_post_service
    app.dependency_overrides[get_current_user] = lambda: test_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac, mock_post_service
    app.dependency_overrides.pop(get_post_service, None)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
async def anon_post_client(mock_post_service):
    app.dependency_overrides[get_post_service] = lambda: mock_post_service
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac, mock_post_service
    app.dependency_overrides.pop(get_post_service, None)
