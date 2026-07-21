"""Integration model — a workspace's connection to an external tool (e.g. Notion).

Hermes' database is the source of record; an integration is a replaceable interface. The
credential itself lives in the encrypted secret vault and is referenced by name, not
stored here. See ``docs/07-NOTION_INTEGRATION.md``.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from hermes_api.db import Base
from hermes_api.enums import IntegrationStatus
from hermes_api.models.base import TimestampMixin, UUIDMixin


class Integration(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "integrations"
    __table_args__ = (
        UniqueConstraint("workspace_id", "provider", name="uq_integrations_workspace_provider"),
    )

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=IntegrationStatus.DISCONNECTED.value
    )
    # Name of the vault secret holding the provider token (if any).
    secret_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    # Provider-specific configuration (database ids, mapping overrides, etc.).
    config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
