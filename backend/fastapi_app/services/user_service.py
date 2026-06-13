import uuid
from pathlib import Path

from fastapi import UploadFile

from fastapi_app.models.user import User
from fastapi_app.repositories.user_repository import UserRepository
from fastapi_app.schemas.user import UserRead, UserUpdate
from fastapi_app.services.base import BaseService
from fastapi_app.utils.exceptions import ConflictError, NotFoundError, ValidationError

ALLOWED_AVATAR_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5 MB
AVATARS_DIR = Path("static/avatars")


class UserService(BaseService[User, UserRepository]):
    async def get_profile(self, user_id: uuid.UUID) -> UserRead:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User")
        post_count = await self._repo.count_posts_by_user(user_id)
        return UserRead.model_validate({**vars(user), "post_count": post_count})

    async def update_profile(self, user: User, data: UserUpdate) -> UserRead:
        updates: dict = {}

        if data.username is not None:
            if await self._repo.username_exists(data.username, exclude_id=user.id):
                raise ConflictError("Username is already taken")
            updates["username"] = data.username

        if data.bio is not None:
            updates["bio"] = data.bio

        if updates:
            user = await self._repo.update(user, **updates)

        post_count = await self._repo.count_posts_by_user(user.id)
        return UserRead.model_validate({**vars(user), "post_count": post_count})

    async def upload_avatar(self, user: User, file: UploadFile) -> UserRead:
        if file.content_type not in ALLOWED_AVATAR_TYPES:
            raise ValidationError("Only JPEG, PNG, GIF, and WebP images are allowed")

        contents = await file.read()
        if len(contents) > MAX_AVATAR_SIZE:
            raise ValidationError("Avatar file size must be under 5 MB")

        AVATARS_DIR.mkdir(parents=True, exist_ok=True)
        ext = (
            file.filename.rsplit(".", 1)[-1]
            if file.filename and "." in file.filename
            else "jpg"
        )
        filename = f"{user.id}.{ext}"
        file_path = AVATARS_DIR / filename

        file_path.write_bytes(contents)
        avatar_url = f"/static/avatars/{filename}"

        user = await self._repo.update(user, avatar_url=avatar_url)
        post_count = await self._repo.count_posts_by_user(user.id)
        return UserRead.model_validate({**vars(user), "post_count": post_count})
