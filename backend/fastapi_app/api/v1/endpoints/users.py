from fastapi import APIRouter, Depends, File, UploadFile, status

from fastapi_app.api.v1.dependencies import get_user_service
from fastapi_app.core.dependencies import get_current_user
from fastapi_app.models.user import User
from fastapi_app.schemas.user import UserRead, UserUpdate
from fastapi_app.services.user_service import UserService
from fastapi_app.utils.responses import ApiResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=ApiResponse[UserRead])
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> ApiResponse[UserRead]:
    profile = await service.get_profile(current_user.id)
    return ApiResponse.ok(data=profile)


@router.patch("/me", response_model=ApiResponse[UserRead])
async def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> ApiResponse[UserRead]:
    profile = await service.update_profile(current_user, data)
    return ApiResponse.ok(data=profile, message="Profile updated successfully")


@router.post("/me/avatar", response_model=ApiResponse[UserRead])
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> ApiResponse[UserRead]:
    profile = await service.upload_avatar(current_user, file)
    return ApiResponse.ok(data=profile, message="Avatar uploaded successfully")
