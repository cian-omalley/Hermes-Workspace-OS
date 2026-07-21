"""Authentication & RBAC: user passwords, memberships, secrets, audit log.

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-20
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _ts_columns() -> list[sa.Column]:
    return [
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    ]


def upgrade() -> None:
    op.add_column("users", sa.Column("password_hash", sa.String(length=200), nullable=True))

    op.create_table(
        "user_memberships",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        *_ts_columns(),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("workspace_id", "user_id", name="uq_memberships_workspace_user"),
    )
    op.create_index("ix_memberships_workspace_id", "user_memberships", ["workspace_id"])
    op.create_index("ix_memberships_user_id", "user_memberships", ["user_id"])

    op.create_table(
        "secrets",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=True),
        sa.Column("ciphertext", sa.LargeBinary(), nullable=False),
        *_ts_columns(),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("workspace_id", "name", name="uq_secrets_workspace_name"),
    )
    op.create_index("ix_secrets_workspace_id", "secrets", ["workspace_id"])

    op.create_table(
        "audit_log",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("actor_type", sa.String(length=20), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("workspace_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("method", sa.String(length=10), nullable=True),
        sa.Column("path", sa.String(length=500), nullable=True),
        sa.Column("status_code", sa.Integer(), nullable=True),
        *_ts_columns(),
    )
    op.create_index("ix_audit_actor_id", "audit_log", ["actor_id"])
    op.create_index("ix_audit_workspace_id", "audit_log", ["workspace_id"])


def downgrade() -> None:
    op.drop_table("audit_log")
    op.drop_table("secrets")
    op.drop_table("user_memberships")
    op.drop_column("users", "password_hash")
