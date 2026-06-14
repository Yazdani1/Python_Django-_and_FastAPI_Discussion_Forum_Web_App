import uuid

from fastapi_app.enums import VoteType
from fastapi_app.models.user import User
from fastapi_app.models.vote import Vote
from fastapi_app.repositories.post_repository import PostRepository
from fastapi_app.repositories.answer_repository import AnswerRepository
from fastapi_app.repositories.vote_repository import VoteRepository
from fastapi_app.schemas.vote import VoteResult
from fastapi_app.services.base import BaseService
from fastapi_app.utils.exceptions import NotFoundError


class VoteService(BaseService[Vote, VoteRepository]):
    def __init__(
        self,
        repository: VoteRepository,
        post_repo: PostRepository,
        answer_repo: AnswerRepository,
    ) -> None:
        super().__init__(repository)
        self._post_repo = post_repo
        self._answer_repo = answer_repo

    async def vote_post(
        self, post_id: uuid.UUID, user: User, vote_type: VoteType
    ) -> VoteResult:
        post = await self._post_repo.get_by_id(post_id)
        if not post:
            raise NotFoundError("Post")

        existing = await self._repo.get_post_vote(user.id, post_id)
        if existing:
            if existing.vote_type == vote_type:
                await self._repo.delete(existing)
            else:
                await self._repo.update(existing, vote_type=vote_type)
        else:
            await self._repo.create(
                user_id=user.id, post_id=post_id, vote_type=vote_type
            )

        count = await self._repo.get_post_vote_count(post_id)
        current = await self._repo.get_post_vote(user.id, post_id)
        return VoteResult(
            vote_count=count,
            user_vote=current.vote_type.value if current else None,
        )

    async def remove_post_vote(self, post_id: uuid.UUID, user: User) -> VoteResult:
        existing = await self._repo.get_post_vote(user.id, post_id)
        if existing:
            await self._repo.delete(existing)
        count = await self._repo.get_post_vote_count(post_id)
        return VoteResult(vote_count=count, user_vote=None)

    async def vote_answer(
        self, answer_id: uuid.UUID, user: User, vote_type: VoteType
    ) -> VoteResult:
        answer = await self._answer_repo.get_by_id(answer_id)
        if not answer:
            raise NotFoundError("Answer")

        existing = await self._repo.get_answer_vote(user.id, answer_id)
        if existing:
            if existing.vote_type == vote_type:
                await self._repo.delete(existing)
            else:
                await self._repo.update(existing, vote_type=vote_type)
        else:
            await self._repo.create(
                user_id=user.id, answer_id=answer_id, vote_type=vote_type
            )

        count = await self._repo.get_answer_vote_count(answer_id)
        current = await self._repo.get_answer_vote(user.id, answer_id)
        return VoteResult(
            vote_count=count,
            user_vote=current.vote_type.value if current else None,
        )

    async def remove_answer_vote(self, answer_id: uuid.UUID, user: User) -> VoteResult:
        existing = await self._repo.get_answer_vote(user.id, answer_id)
        if existing:
            await self._repo.delete(existing)
        count = await self._repo.get_answer_vote_count(answer_id)
        return VoteResult(vote_count=count, user_vote=None)
