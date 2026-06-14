import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.core.database import Base
from fastapi_app.enums import ModerationAction

if TYPE_CHECKING:
    from fastapi_app.models.user import User


class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    admin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[ModerationAction] = mapped_column(
        Enum(
            ModerationAction,
            name="moderation_action",
            native_enum=True,
            create_type=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )
    target_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    admin: Mapped["User | None"] = relationship(
        "User", foreign_keys=[admin_id], lazy="select"
    )
