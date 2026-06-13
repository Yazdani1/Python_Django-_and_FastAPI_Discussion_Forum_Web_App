import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from fastapi_app.enums import UserRole


class UserPublic(BaseModel):
    id: uuid.UUID
    username: str
    avatar_url: str | None
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    role: UserRole
    avatar_url: str | None
    bio: str | None
    is_active: bool
    created_at: datetime
    post_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
    )
    bio: str | None = Field(default=None, max_length=500)
