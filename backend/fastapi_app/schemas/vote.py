from pydantic import BaseModel

from fastapi_app.enums import VoteType


class VoteRequest(BaseModel):
    vote_type: VoteType


class VoteResult(BaseModel):
    vote_count: int
    user_vote: str | None
