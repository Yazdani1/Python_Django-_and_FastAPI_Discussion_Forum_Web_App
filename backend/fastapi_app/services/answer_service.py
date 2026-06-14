import uuid

from fastapi_app.enums import ROLE_LEVELS, UserRole
from fastapi_app.models.answer import Answer
from fastapi_app.models.user import User
from fastapi_app.repositories.answer_repository import AnswerRepository
from fastapi_app.repositories.vote_repository import VoteRepository
from fastapi_app.schemas.answer import AnswerCreate, AnswerRead, AnswerUpdate
from fastapi_app.schemas.user import UserPublic
from fastapi_app.services.base import BaseService
from fastapi_app.utils.exceptions import ForbiddenError, NotFoundError


class AnswerService(BaseService[Answer, AnswerRepository]):
    def __init__(self, repository: AnswerRepository, vote_repo: VoteRepository) -> None:
        super().__init__(repository)
        self._vote_repo = vote_repo

    async def _to_read(
        self, answer: Answer, current_user_id: uuid.UUID | None = None
    ) -> AnswerRead:
        vote_count = await self._vote_repo.get_answer_vote_count(answer.id)
        user_vote = None
        if current_user_id:
            existing = await self._vote_repo.get_answer_vote(current_user_id, answer.id)
            user_vote = existing.vote_type.value if existing else None
        return AnswerRead(
            id=answer.id,
            content=answer.content,
            author=UserPublic.model_validate(answer.author),
            post_id=answer.post_id,
            vote_count=vote_count,
            user_vote=user_vote,
            created_at=answer.created_at,
            updated_at=answer.updated_at,
        )

    async def list_answers(
        self,
        post_id: uuid.UUID,
        current_user_id: uuid.UUID | None = None,
    ) -> list[AnswerRead]:
        answers = await self._repo.list_by_post(post_id)
        return [await self._to_read(a, current_user_id) for a in answers]

    async def add_answer(
        self, post_id: uuid.UUID, author: User, data: AnswerCreate
    ) -> AnswerRead:
        answer = await self._repo.create(
            content=data.content,
            author_id=author.id,
            post_id=post_id,
        )
        answer = await self._repo.get_with_author(answer.id)
        return await self._to_read(answer, author.id)  # type: ignore[arg-type]

    async def update_answer(
        self,
        answer_id: uuid.UUID,
        current_user: User,
        data: AnswerUpdate,
    ) -> AnswerRead:
        answer = await self._repo.get_with_author(answer_id)
        if not answer:
            raise NotFoundError("Answer")
        if answer.author_id != current_user.id:
            raise ForbiddenError("You can only edit your own answers")
        answer = await self._repo.update(answer, content=data.content)
        answer = await self._repo.get_with_author(answer.id)
        return await self._to_read(answer, current_user.id)  # type: ignore[arg-type]

    async def delete_answer(self, answer_id: uuid.UUID, current_user: User) -> None:
        answer = await self._repo.get_by_id(answer_id)
        if not answer:
            raise NotFoundError("Answer")
        is_owner = answer.author_id == current_user.id
        is_privileged = (
            ROLE_LEVELS.get(current_user.role, 0) >= ROLE_LEVELS[UserRole.MODERATOR]
        )
        if not is_owner and not is_privileged:
            raise ForbiddenError("You can only delete your own answers")
        await self._repo.delete(answer)
