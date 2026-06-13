from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.core.database import get_db
from fastapi_app.repositories.post_repository import PostRepository
from fastapi_app.repositories.user_repository import UserRepository
from fastapi_app.services.auth_service import AuthService
from fastapi_app.services.post_service import PostService
from fastapi_app.services.user_service import UserService


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def get_post_service(db: AsyncSession = Depends(get_db)) -> PostService:
    return PostService(PostRepository(db))
