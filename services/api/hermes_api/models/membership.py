"""Membership model — a user's role within a workspace (RBAC)."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.auth.roles import Role
from hermes_api.db import Base
from hermes_api.models.base import TimestampMixin, UUIDMixin


class Membership(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "user_memberships"
    __table_args__ = (
        UniqueConstraint("workspace_id", "user_id", name="uq_memberships_workspace_user"),
    )

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False, default=Role.VIEWER.value)
