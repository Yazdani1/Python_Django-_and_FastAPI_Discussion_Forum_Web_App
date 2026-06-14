"""add moderation_logs table

Revision ID: 0004
Revises: 0003
Create Date: 2024-01-04 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "moderation_logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("admin_id", sa.UUID(), nullable=True),
        sa.Column(
            "action",
            sa.Enum(
                "block_user",
                "unblock_user",
                name="moderation_action",
            ),
            nullable=False,
        ),
        sa.Column("target_user_id", sa.UUID(), nullable=True),
        sa.Column("reason", sa.String(500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["admin_id"], ["users.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_moderation_logs_admin_id", "moderation_logs", ["admin_id"])
    op.create_index(
        "ix_moderation_logs_target_user_id",
        "moderation_logs",
        ["target_user_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_moderation_logs_target_user_id", "moderation_logs")
    op.drop_index("ix_moderation_logs_admin_id", "moderation_logs")
    op.drop_table("moderation_logs")
    op.execute("DROP TYPE IF EXISTS moderation_action")
