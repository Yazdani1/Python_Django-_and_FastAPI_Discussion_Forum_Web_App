import uuid
from datetime import date, datetime, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.orm import joinedload

from fastapi_app.models.post import Post
from fastapi_app.repositories.base import BaseRepository
from fastapi_app.utils.responses import MetaData


class PostRepository(BaseRepository[Post]):
    model = Post

    async def get_with_author(self, post_id: uuid.UUID) -> Post | None:
        result = await self._session.execute(
            select(Post).options(joinedload(Post.author)).where(Post.id == post_id)
        )
        return result.scalar_one_or_none()

    async def list_with_authors(
        self,
        *,
        search: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Post], MetaData]:
        query = select(Post).options(joinedload(Post.author))

        if search:
            term = f"%{search}%"
            query = query.where(or_(Post.title.ilike(term), Post.content.ilike(term)))
        if date_from:
            dt_from = datetime(
                date_from.year, date_from.month, date_from.day, tzinfo=timezone.utc
            )
            query = query.where(Post.created_at >= dt_from)
        if date_to:
            dt_to = datetime(
                date_to.year,
                date_to.month,
                date_to.day,
                23,
                59,
                59,
                tzinfo=timezone.utc,
            )
            query = query.where(Post.created_at <= dt_to)

        count_result = await self._session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar_one()
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        offset = (page - 1) * page_size
        result = await self._session.execute(
            query.order_by(Post.created_at.desc()).offset(offset).limit(page_size)
        )
        posts = list(result.scalars().all())

        meta = MetaData(
            page=page, page_size=page_size, total=total, total_pages=total_pages
        )
        return posts, meta

    async def count_by_author(self, author_id: uuid.UUID) -> int:
        result = await self._session.execute(
            select(func.count(Post.id)).where(Post.author_id == author_id)
        )
        return result.scalar_one()
