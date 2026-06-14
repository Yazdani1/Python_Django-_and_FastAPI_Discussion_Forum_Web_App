import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from fastapi_app.enums import UserRole
from fastapi_app.schemas.user import UserRead
from fastapi_app.tests.conftest import make_user
from fastapi_app.utils.exceptions import NotFoundError


def _user_read() -> UserRead:
    user = make_user()
    return UserRead(
        id=user.id,
        email=user.email,
        username=user.username,
        role=user.role,
        avatar_url=None,
        bio=None,
        is_active=False,
        created_at=datetime.now(timezone.utc),
        post_count=0,
    )


@pytest.fixture
def mock_mod_service():
    return AsyncMock()


@pytest.fixture
async def admin_client(mock_mod_service):
    from fastapi_app.main import app
    from fastapi_app.api.v1.dependencies import get_moderation_service
    from fastapi_app.core.dependencies import get_current_user, require_role
    from httpx import ASGITransport, AsyncClient

    admin = make_user(role=UserRole.ADMIN)
    app.dependency_overrides[get_moderation_service] = lambda: mock_mod_service
    app.dependency_overrides[get_current_user] = lambda: admin
    app.dependency_overrides[require_role(UserRole.ADMIN)] = lambda: admin
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac, mock_mod_service
    app.dependency_overrides.pop(get_moderation_service, None)
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(require_role(UserRole.ADMIN), None)


@pytest.mark.asyncio
async def test_block_user_success(admin_client):
    ac, mock_svc = admin_client
    user_id = uuid.uuid4()
    blocked = _user_read()
    mock_svc.block_user.return_value = blocked

    response = await ac.post(f"/api/v1/admin/users/{user_id}/block")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    mock_svc.block_user.assert_called_once()


@pytest.mark.asyncio
async def test_unblock_user_success(admin_client):
    ac, mock_svc = admin_client
    user_id = uuid.uuid4()
    unblocked = _user_read()
    mock_svc.unblock_user.return_value = unblocked

    response = await ac.post(f"/api/v1/admin/users/{user_id}/unblock")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    mock_svc.unblock_user.assert_called_once()


@pytest.mark.asyncio
async def test_block_user_not_found(admin_client):
    ac, mock_svc = admin_client
    user_id = uuid.uuid4()
    mock_svc.block_user.side_effect = NotFoundError("User")

    response = await ac.post(f"/api/v1/admin/users/{user_id}/block")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_logs(admin_client):
    ac, mock_svc = admin_client
    mock_svc.list_logs.return_value = []

    response = await ac.get("/api/v1/admin/logs")

    assert response.status_code == 200
    body = response.json()
    assert body["data"] == []


@pytest.mark.asyncio
async def test_admin_requires_auth():
    from fastapi_app.main import app
    from httpx import ASGITransport, AsyncClient

    user_id = uuid.uuid4()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(f"/api/v1/admin/users/{user_id}/block")
    assert response.status_code == 401
