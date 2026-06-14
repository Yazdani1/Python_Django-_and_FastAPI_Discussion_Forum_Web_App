import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from fastapi_app.models.answer import Answer
from fastapi_app.repositories.base import BaseRepository


class AnswerRepository(BaseRepository[Answer]):
    model = Answer

    async def list_by_post(self, post_id: uuid.UUID) -> list[Answer]:
        result = await self._session.execute(
            select(Answer)
            .options(joinedload(Answer.author))
            .where(Answer.post_id == post_id)
            .order_by(Answer.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_with_author(self, answer_id: uuid.UUID) -> Answer | None:
        result = await self._session.execute(
            select(Answer)
            .options(joinedload(Answer.author))
            .where(Answer.id == answer_id)
        )
        return result.scalar_one_or_none()

    async def count_by_post(self, post_id: uuid.UUID) -> int:
        result = await self._session.execute(
            select(func.count(Answer.id)).where(Answer.post_id == post_id)
        )
        return result.scalar_one()

    async def bulk_count_by_posts(
        self, post_ids: list[uuid.UUID]
    ) -> dict[uuid.UUID, int]:
        if not post_ids:
            return {}
        result = await self._session.execute(
            select(Answer.post_id, func.count(Answer.id).label("cnt"))
            .where(Answer.post_id.in_(post_ids))
            .group_by(Answer.post_id)
        )
        return {row.post_id: row.cnt for row in result}
