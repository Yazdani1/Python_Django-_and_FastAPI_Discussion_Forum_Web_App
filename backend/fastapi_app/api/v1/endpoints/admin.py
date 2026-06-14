import uuid

from fastapi import APIRouter, Depends, Query

from fastapi_app.api.v1.dependencies import get_moderation_service
from fastapi_app.core.dependencies import get_current_user, require_role
from fastapi_app.enums import UserRole
from fastapi_app.models.user import User
from fastapi_app.schemas.user import UserRead
from fastapi_app.services.moderation_service import ModerationService
from fastapi_app.utils.responses import ApiResponse

router = APIRouter(prefix="/admin", tags=["admin"])

_require_admin = require_role(UserRole.ADMIN)


class ModerationLogRead:
    pass


@router.post(
    "/users/{user_id}/block",
    response_model=ApiResponse[UserRead],
)
async def block_user(
    user_id: uuid.UUID,
    reason: str | None = Query(default=None, max_length=500),
    _: User = Depends(_require_admin),
    admin: User = Depends(get_current_user),
    service: ModerationService = Depends(get_moderation_service),
) -> ApiResponse[UserRead]:
    user = await service.block_user(admin, user_id, reason)
    return ApiResponse.ok(data=user, message="User blocked")


@router.post(
    "/users/{user_id}/unblock",
    response_model=ApiResponse[UserRead],
)
async def unblock_user(
    user_id: uuid.UUID,
    reason: str | None = Query(default=None, max_length=500),
    _: User = Depends(_require_admin),
    admin: User = Depends(get_current_user),
    service: ModerationService = Depends(get_moderation_service),
) -> ApiResponse[UserRead]:
    user = await service.unblock_user(admin, user_id, reason)
    return ApiResponse.ok(data=user, message="User unblocked")


@router.get("/logs", response_model=ApiResponse[list[dict]])
async def list_moderation_logs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    _: User = Depends(_require_admin),
    service: ModerationService = Depends(get_moderation_service),
) -> ApiResponse[list[dict]]:
    logs = await service.list_logs(page=page, page_size=page_size)
    data = [
        {
            "id": str(log.id),
            "admin_id": str(log.admin_id) if log.admin_id else None,
            "action": log.action.value,
            "target_user_id": str(log.target_user_id) if log.target_user_id else None,
            "reason": log.reason,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]
    return ApiResponse.ok(data=data)
