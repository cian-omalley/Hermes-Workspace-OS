"""Agent model — a (dormant) AI agent record; execution arrives in Milestone 9."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.db import Base
from hermes_api.enums import AgentRole, AgentStatus
from hermes_api.models.base import TimestampMixin, UUIDMixin
from hermes_api.models.mixins import WorkspaceScopedMixin


class Agent(UUIDMixin, WorkspaceScopedMixin, TimestampMixin, Base):
    __tablename__ = "agents"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False, default=AgentRole.CUSTOM.value)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=AgentStatus.IDLE.value)
