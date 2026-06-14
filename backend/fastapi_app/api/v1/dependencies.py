from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.core.database import get_db
from fastapi_app.repositories.answer_repository import AnswerRepository
from fastapi_app.repositories.post_repository import PostRepository
from fastapi_app.repositories.user_repository import UserRepository
from fastapi_app.repositories.vote_repository import VoteRepository
from fastapi_app.services.answer_service import AnswerService
from fastapi_app.services.auth_service import AuthService
from fastapi_app.services.moderation_service import (
    ModerationRepository,
    ModerationService,
)
from fastapi_app.services.post_service import PostService
from fastapi_app.services.user_service import UserService
from fastapi_app.services.vote_service import VoteService


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def get_post_service(db: AsyncSession = Depends(get_db)) -> PostService:
    return PostService(
        PostRepository(db),
        VoteRepository(db),
        AnswerRepository(db),
    )


def get_answer_service(db: AsyncSession = Depends(get_db)) -> AnswerService:
    return AnswerService(AnswerRepository(db), VoteRepository(db))


def get_vote_service(db: AsyncSession = Depends(get_db)) -> VoteService:
    return VoteService(VoteRepository(db), PostRepository(db), AnswerRepository(db))


def get_moderation_service(db: AsyncSession = Depends(get_db)) -> ModerationService:
    return ModerationService(ModerationRepository(db), UserRepository(db))
