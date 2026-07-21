"""Audit log model — an append-only record of sensitive actions."""

from __future__ import annotations

import uuid

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.db import Base
from hermes_api.models.base import TimestampMixin, UUIDMixin


class AuditLog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "audit_log"

    # actor_type: user | system | integration | agent
    actor_type: Mapped[str] = mapped_column(String(20), nullable=False, default="user")
    actor_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    workspace_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    method: Mapped[str | None] = mapped_column(String(10), nullable=True)
    path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
