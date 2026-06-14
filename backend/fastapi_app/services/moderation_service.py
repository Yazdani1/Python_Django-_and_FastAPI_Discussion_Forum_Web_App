import uuid

from fastapi_app.enums import ModerationAction
from fastapi_app.models.moderation_log import ModerationLog
from fastapi_app.models.user import User
from fastapi_app.repositories.base import BaseRepository
from fastapi_app.repositories.user_repository import UserRepository
from fastapi_app.schemas.user import UserRead
from fastapi_app.services.base import BaseService
from fastapi_app.utils.exceptions import ForbiddenError, NotFoundError


class ModerationRepository(BaseRepository[ModerationLog]):
    model = ModerationLog


class ModerationService(BaseService[ModerationLog, ModerationRepository]):
    def __init__(
        self,
        repository: ModerationRepository,
        user_repo: UserRepository,
    ) -> None:
        super().__init__(repository)
        self._user_repo = user_repo

    async def _log(
        self,
        admin: User,
        action: ModerationAction,
        target_user_id: uuid.UUID,
        reason: str | None,
    ) -> None:
        await self._repo.create(
            admin_id=admin.id,
            action=action,
            target_user_id=target_user_id,
            reason=reason,
        )

    async def block_user(
        self, admin: User, target_id: uuid.UUID, reason: str | None = None
    ) -> UserRead:
        target = await self._user_repo.get_by_id(target_id)
        if not target:
            raise NotFoundError("User")
        if target.id == admin.id:
            raise ForbiddenError("You cannot block yourself")
        target = await self._user_repo.update(target, is_active=False)
        await self._log(admin, ModerationAction.BLOCK_USER, target.id, reason)
        post_count = await self._user_repo.count_posts_by_user(target.id)
        return UserRead.model_validate({**vars(target), "post_count": post_count})

    async def unblock_user(
        self, admin: User, target_id: uuid.UUID, reason: str | None = None
    ) -> UserRead:
        target = await self._user_repo.get_by_id(target_id)
        if not target:
            raise NotFoundError("User")
        target = await self._user_repo.update(target, is_active=True)
        await self._log(admin, ModerationAction.UNBLOCK_USER, target.id, reason)
        post_count = await self._user_repo.count_posts_by_user(target.id)
        return UserRead.model_validate({**vars(target), "post_count": post_count})

    async def list_logs(
        self, *, page: int = 1, page_size: int = 50
    ) -> list[ModerationLog]:
        offset = (page - 1) * page_size
        return await self._repo.get_all(offset=offset, limit=page_size)
