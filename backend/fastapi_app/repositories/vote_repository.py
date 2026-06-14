import uuid

from sqlalchemy import case, func, select

from fastapi_app.enums import VoteType
from fastapi_app.models.vote import Vote
from fastapi_app.repositories.base import BaseRepository


class VoteRepository(BaseRepository[Vote]):
    model = Vote

    async def get_post_vote(
        self, user_id: uuid.UUID, post_id: uuid.UUID
    ) -> Vote | None:
        result = await self._session.execute(
            select(Vote).where(Vote.user_id == user_id, Vote.post_id == post_id)
        )
        return result.scalar_one_or_none()

    async def get_answer_vote(
        self, user_id: uuid.UUID, answer_id: uuid.UUID
    ) -> Vote | None:
        result = await self._session.execute(
            select(Vote).where(Vote.user_id == user_id, Vote.answer_id == answer_id)
        )
        return result.scalar_one_or_none()

    async def get_post_vote_count(self, post_id: uuid.UUID) -> int:
        result = await self._session.execute(
            select(
                func.coalesce(
                    func.sum(case((Vote.vote_type == VoteType.UP, 1), else_=-1)),
                    0,
                )
            ).where(Vote.post_id == post_id)
        )
        return result.scalar_one()

    async def get_answer_vote_count(self, answer_id: uuid.UUID) -> int:
        result = await self._session.execute(
            select(
                func.coalesce(
                    func.sum(case((Vote.vote_type == VoteType.UP, 1), else_=-1)),
                    0,
                )
            ).where(Vote.answer_id == answer_id)
        )
        return result.scalar_one()

    async def bulk_post_vote_counts(
        self, post_ids: list[uuid.UUID]
    ) -> dict[uuid.UUID, int]:
        if not post_ids:
            return {}
        result = await self._session.execute(
            select(
                Vote.post_id,
                func.coalesce(
                    func.sum(case((Vote.vote_type == VoteType.UP, 1), else_=-1)),
                    0,
                ).label("cnt"),
            )
            .where(Vote.post_id.in_(post_ids))
            .group_by(Vote.post_id)
        )
        return {row.post_id: row.cnt for row in result}
