"""Sync bookkeeping: per-entity sync state, inbound webhook dedup, and a sync log.

These make external sync idempotent and conflict-aware without making the external tool
authoritative. See ``docs/05-DATABASE_DESIGN.md`` §1.10 and ``docs/07-NOTION_INTEGRATION.md``.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from hermes_api.db import Base
from hermes_api.models.base import TimestampMixin, UUIDMixin


class SyncState(UUIDMixin, TimestampMixin, Base):
    """Binds a Hermes entity to its external counterpart and tracks last-synced state."""

    __tablename__ = "sync_state"
    __table_args__ = (
        UniqueConstraint("integration_id", "entity_type", "hermes_id", name="uq_sync_state_entity"),
    )

    integration_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    hermes_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    external_id: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    # Checksum of the fields last pushed to / received from the external tool. Used to
    # detect whether Hermes changed since the last sync (conflict detection).
    checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)


class WebhookEvent(UUIDMixin, TimestampMixin, Base):
    """Inbound event idempotency: a unique external id per (provider, event)."""

    __tablename__ = "webhook_events"
    __table_args__ = (
        UniqueConstraint("provider", "external_id", name="uq_webhook_events_provider_external"),
    )

    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    external_id: Mapped[str] = mapped_column(String(300), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    processed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class SyncLog(UUIDMixin, TimestampMixin, Base):
    """Human-readable record of sync operations and their outcomes."""

    __tablename__ = "sync_log"

    integration_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    direction: Mapped[str] = mapped_column(String(20), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    detail: Mapped[str | None] = mapped_column(String(500), nullable=True)
