from fastapi import APIRouter, Cookie, Depends, Response, status

from fastapi_app.api.v1.dependencies import get_auth_service
from fastapi_app.core.config import settings
from fastapi_app.schemas.auth import LoginRequest, RegisterRequest
from fastapi_app.schemas.user import UserRead
from fastapi_app.services.auth_service import AuthService
from fastapi_app.utils.responses import ApiResponse

router = APIRouter(prefix="/auth", tags=["auth"])

_COOKIE_OPTS = dict(
    httponly=settings.COOKIE_HTTPONLY,
    secure=settings.COOKIE_SECURE,
    samesite=settings.COOKIE_SAMESITE,
    path="/",
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[UserRead],
)
async def register(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> ApiResponse[UserRead]:
    user = await service.register(data)
    return ApiResponse.created(data=user, message="Registration successful")


@router.post("/login", response_model=ApiResponse[UserRead])
async def login(
    data: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
) -> ApiResponse[UserRead]:
    user, access_token, refresh_token = await service.login(data)

    response.set_cookie(
        "access_token",
        access_token,
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        **_COOKIE_OPTS,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        **_COOKIE_OPTS,
    )

    user_data = UserRead.model_validate({**vars(user), "post_count": 0})
    return ApiResponse.ok(data=user_data, message="Login successful")


@router.post("/logout", response_model=ApiResponse[None])
async def logout(response: Response) -> ApiResponse[None]:
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return ApiResponse.ok(message="Logged out successfully")


@router.post("/refresh", response_model=ApiResponse[None])
async def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    service: AuthService = Depends(get_auth_service),
) -> ApiResponse[None]:
    if not refresh_token:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Refresh token missing")

    new_access, new_refresh = await service.refresh(refresh_token)

    response.set_cookie(
        "access_token",
        new_access,
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        **_COOKIE_OPTS,
    )
    response.set_cookie(
        "refresh_token",
        new_refresh,
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        **_COOKIE_OPTS,
    )
    return ApiResponse.ok(message="Token refreshed")
