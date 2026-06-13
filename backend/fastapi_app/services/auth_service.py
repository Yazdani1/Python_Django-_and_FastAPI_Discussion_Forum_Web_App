from fastapi_app.core.security import JWTHandler, PasswordHandler
from fastapi_app.models.user import User
from fastapi_app.repositories.user_repository import UserRepository
from fastapi_app.schemas.auth import LoginRequest, RegisterRequest
from fastapi_app.schemas.user import UserRead
from fastapi_app.services.base import BaseService
from fastapi_app.utils.exceptions import ConflictError, UnauthorizedError


class AuthService(BaseService[User, UserRepository]):
    async def register(self, data: RegisterRequest) -> UserRead:
        if await self._repo.email_exists(data.email.lower()):
            raise ConflictError("Email is already registered")
        if await self._repo.username_exists(data.username):
            raise ConflictError("Username is already taken")

        user = await self._repo.create(
            email=data.email.lower(),
            username=data.username,
            hashed_password=PasswordHandler.hash(data.password),
        )
        return UserRead.model_validate({**vars(user), "post_count": 0})

    async def login(self, data: LoginRequest) -> tuple[User, str, str]:
        user = await self._repo.get_by_email(data.email.lower())
        if not user or not user.is_active:
            raise UnauthorizedError("Invalid email or password")
        if not PasswordHandler.verify(data.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        access_token = JWTHandler.create_access_token(
            subject=str(user.id), extra_claims={"role": user.role}
        )
        refresh_token = JWTHandler.create_refresh_token(subject=str(user.id))
        return user, access_token, refresh_token

    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        try:
            payload = JWTHandler.decode_token(refresh_token)
        except ValueError as exc:
            raise UnauthorizedError("Invalid or expired refresh token") from exc

        if payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Invalid token")

        user = await self._repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")

        new_access = JWTHandler.create_access_token(
            subject=str(user.id), extra_claims={"role": user.role}
        )
        new_refresh = JWTHandler.create_refresh_token(subject=str(user.id))
        return new_access, new_refresh
