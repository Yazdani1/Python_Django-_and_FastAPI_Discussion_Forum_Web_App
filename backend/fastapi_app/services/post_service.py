import uuid
from datetime import date

from fastapi_app.enums import ROLE_LEVELS, UserRole
from fastapi_app.models.post import Post
from fastapi_app.models.user import User
from fastapi_app.repositories.answer_repository import AnswerRepository
from fastapi_app.repositories.post_repository import PostRepository
from fastapi_app.repositories.vote_repository import VoteRepository
from fastapi_app.schemas.post import PostCreate, PostListItem, PostRead, PostUpdate
from fastapi_app.schemas.user import UserPublic
from fastapi_app.services.base import BaseService
from fastapi_app.utils.exceptions import ForbiddenError, NotFoundError
from fastapi_app.utils.responses import MetaData


class PostService(BaseService[Post, PostRepository]):
    def __init__(
        self,
        repository: PostRepository,
        vote_repo: VoteRepository,
        answer_repo: AnswerRepository,
    ) -> None:
        super().__init__(repository)
        self._vote_repo = vote_repo
        self._answer_repo = answer_repo

    async def create_post(self, author: User, data: PostCreate) -> PostRead:
        post = await self._repo.create(
            title=data.title,
            content=data.content,
            author_id=author.id,
        )
        post = await self._repo.get_with_author(post.id)
        return PostRead(
            id=post.id,  # type: ignore[union-attr]
            title=post.title,  # type: ignore[union-attr]
            content=post.content,  # type: ignore[union-attr]
            author=UserPublic.model_validate(post.author),  # type: ignore[union-attr]
            vote_count=0,
            answer_count=0,
            user_vote=None,
            created_at=post.created_at,  # type: ignore[union-attr]
            updated_at=post.updated_at,  # type: ignore[union-attr]
        )

    async def get_post(
        self,
        post_id: uuid.UUID,
        current_user_id: uuid.UUID | None = None,
    ) -> PostRead:
        post = await self._repo.get_with_author(post_id)
        if not post:
            raise NotFoundError("Post")
        vote_count = await self._vote_repo.get_post_vote_count(post_id)
        answer_count = await self._answer_repo.count_by_post(post_id)
        user_vote = None
        if current_user_id:
            existing = await self._vote_repo.get_post_vote(current_user_id, post_id)
            user_vote = existing.vote_type.value if existing else None
        return PostRead(
            id=post.id,
            title=post.title,
            content=post.content,
            author=UserPublic.model_validate(post.author),
            vote_count=vote_count,
            answer_count=answer_count,
            user_vote=user_vote,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

    async def list_posts(
        self,
        *,
        search: str | None = None,
        author: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[PostListItem], MetaData]:
        posts, meta = await self._repo.list_with_authors(
            search=search,
            author=author,
            date_from=date_from,
            date_to=date_to,
            page=page,
            page_size=page_size,
        )
        post_ids = [p.id for p in posts]
        answer_counts = await self._answer_repo.bulk_count_by_posts(post_ids)
        vote_counts = await self._vote_repo.bulk_post_vote_counts(post_ids)
        items = [
            PostListItem(
                id=p.id,
                title=p.title,
                preview=p.content[:200],
                author=p.author,
                answer_count=answer_counts.get(p.id, 0),
                vote_count=vote_counts.get(p.id, 0),
                created_at=p.created_at,
            )
            for p in posts
        ]
        return items, meta

    async def update_post(
        self, post_id: uuid.UUID, current_user: User, data: PostUpdate
    ) -> PostRead:
        post = await self._repo.get_with_author(post_id)
        if not post:
            raise NotFoundError("Post")

        is_owner = post.author_id == current_user.id
        is_privileged = (
            ROLE_LEVELS.get(current_user.role, 0) >= ROLE_LEVELS[UserRole.MODERATOR]
        )
        if not is_owner and not is_privileged:
            raise ForbiddenError("You can only edit your own posts")

        updates: dict = {}
        if data.title is not None:
            updates["title"] = data.title
        if data.content is not None:
            updates["content"] = data.content

        if updates:
            await self._repo.update(post, **updates)
            post = await self._repo.get_with_author(post_id)

        return await self.get_post(post_id, current_user.id)

    async def delete_post(self, post_id: uuid.UUID, current_user: User) -> None:
        post = await self._repo.get_by_id(post_id)
        if not post:
            raise NotFoundError("Post")

        is_owner = post.author_id == current_user.id
        is_privileged = (
            ROLE_LEVELS.get(current_user.role, 0) >= ROLE_LEVELS[UserRole.MODERATOR]
        )
        if not is_owner and not is_privileged:
            raise ForbiddenError("You can only delete your own posts")

        await self._repo.delete(post)
