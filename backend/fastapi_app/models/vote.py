import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.core.database import Base
from fastapi_app.enums import VoteType

if TYPE_CHECKING:
    from fastapi_app.models.answer import Answer
    from fastapi_app.models.post import Post
    from fastapi_app.models.user import User


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_vote_user_post"),
        UniqueConstraint("user_id", "answer_id", name="uq_vote_user_answer"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    post_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    answer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("answers.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    vote_type: Mapped[VoteType] = mapped_column(
        Enum(
            VoteType,
            name="vote_type",
            native_enum=True,
            create_type=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", lazy="select")
    post: Mapped["Post | None"] = relationship("Post", lazy="select")
    answer: Mapped["Answer | None"] = relationship("Answer", lazy="select")
