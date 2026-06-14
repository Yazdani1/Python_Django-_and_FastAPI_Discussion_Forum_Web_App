"""add votes table

Revision ID: 0003
Revises: 0002
Create Date: 2024-01-03 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("post_id", sa.UUID(), nullable=True),
        sa.Column("answer_id", sa.UUID(), nullable=True),
        sa.Column(
            "vote_type",
            sa.Enum("up", "down", name="vote_type"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["answer_id"], ["answers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "post_id", name="uq_vote_user_post"),
        sa.UniqueConstraint("user_id", "answer_id", name="uq_vote_user_answer"),
    )
    op.create_index("ix_votes_user_id", "votes", ["user_id"])
    op.create_index("ix_votes_post_id", "votes", ["post_id"])
    op.create_index("ix_votes_answer_id", "votes", ["answer_id"])


def downgrade() -> None:
    op.drop_index("ix_votes_answer_id", "votes")
    op.drop_index("ix_votes_post_id", "votes")
    op.drop_index("ix_votes_user_id", "votes")
    op.drop_table("votes")
    op.execute("DROP TYPE IF EXISTS vote_type")
