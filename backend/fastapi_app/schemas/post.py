import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from fastapi_app.schemas.user import UserPublic


class PostCreate(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    content: str = Field(min_length=10)


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=200)
    content: str | None = Field(default=None, min_length=10)


class PostRead(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    author: UserPublic
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostListItem(BaseModel):
    id: uuid.UUID
    title: str
    preview: str
    author: UserPublic
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
