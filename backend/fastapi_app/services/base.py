from typing import Any, Generic, TypeVar

from fastapi_app.repositories.base import BaseRepository
from fastapi_app.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)
RepoT = TypeVar("RepoT", bound=BaseRepository)


class BaseService(Generic[ModelT, RepoT]):
    """Abstract base service providing common business logic wrappers.

    Subclasses receive a repository instance and delegate all data access
    to it, keeping business logic separate from persistence concerns.
    """

    def __init__(self, repository: RepoT) -> None:
        self._repo = repository

    async def get_by_id(self, record_id: Any) -> ModelT | None:
        return await self._repo.get_by_id(record_id)

    async def get_all(self, *, offset: int = 0, limit: int = 20) -> list[ModelT]:
        return await self._repo.get_all(offset=offset, limit=limit)

    async def delete(self, record_id: Any) -> bool:
        instance = await self._repo.get_by_id(record_id)
        if instance is None:
            return False
        await self._repo.delete(instance)
        return True
