import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from fastapi_app.schemas.user import UserPublic


class AnswerCreate(BaseModel):
    content: str = Field(min_length=10)


class AnswerUpdate(BaseModel):
    content: str = Field(min_length=10)


class AnswerRead(BaseModel):
    id: uuid.UUID
    content: str
    author: UserPublic
    post_id: uuid.UUID
    vote_count: int = 0
    user_vote: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
