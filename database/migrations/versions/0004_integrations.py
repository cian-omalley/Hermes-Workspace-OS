"""Integrations & sync bookkeeping: integrations, sync_state, webhook_events, sync_log.

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-21
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
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
    op.create_table(
        "integrations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("provider", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("secret_name", sa.String(length=200), nullable=True),
        sa.Column("config", sa.JSON(), nullable=False),
        *_ts_columns(),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("workspace_id", "provider", name="uq_integrations_workspace_provider"),
    )
    op.create_index("ix_integrations_workspace_id", "integrations", ["workspace_id"])

    op.create_table(
        "sync_state",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("integration_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("hermes_id", sa.Uuid(), nullable=False),
        sa.Column("external_id", sa.String(length=200), nullable=True),
        sa.Column("checksum", sa.String(length=64), nullable=True),
        *_ts_columns(),
        sa.ForeignKeyConstraint(["integration_id"], ["integrations.id"], ondelete="CASCADE"),
        sa.UniqueConstraint(
            "integration_id", "entity_type", "hermes_id", name="uq_sync_state_entity"
        ),
    )
    op.create_index("ix_sync_state_integration_id", "sync_state", ["integration_id"])
    op.create_index("ix_sync_state_hermes_id", "sync_state", ["hermes_id"])
    op.create_index("ix_sync_state_external_id", "sync_state", ["external_id"])

    op.create_table(
        "webhook_events",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("provider", sa.String(length=20), nullable=False),
        sa.Column("external_id", sa.String(length=300), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("processed", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_ts_columns(),
        sa.UniqueConstraint("provider", "external_id", name="uq_webhook_events_provider_external"),
    )

    op.create_table(
        "sync_log",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("integration_id", sa.Uuid(), nullable=False),
        sa.Column("direction", sa.String(length=20), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=True),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("detail", sa.String(length=500), nullable=True),
        *_ts_columns(),
        sa.ForeignKeyConstraint(["integration_id"], ["integrations.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_sync_log_integration_id", "sync_log", ["integration_id"])


def downgrade() -> None:
    op.drop_table("sync_log")
    op.drop_table("webhook_events")
    op.drop_table("sync_state")
    op.drop_table("integrations")
