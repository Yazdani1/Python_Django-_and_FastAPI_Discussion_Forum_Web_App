import uuid

from sqlalchemy import func, select

from fastapi_app.core.database import Base
from fastapi_app.models.post import Post
from fastapi_app.models.user import User
from fastapi_app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        result = await self._session.execute(
            select(func.count()).select_from(User).where(User.email == email.lower())
        )
        return result.scalar_one() > 0

    async def username_exists(self, username: str, exclude_id: uuid.UUID | None = None) -> bool:
        query = select(func.count()).select_from(User).where(User.username == username)
        if exclude_id is not None:
            query = query.where(User.id != exclude_id)
        result = await self._session.execute(query)
        return result.scalar_one() > 0

    async def count_posts_by_user(self, user_id: uuid.UUID) -> int:
        result = await self._session.execute(
            select(func.count(Post.id)).where(Post.author_id == user_id)
        )
        return result.scalar_one()
