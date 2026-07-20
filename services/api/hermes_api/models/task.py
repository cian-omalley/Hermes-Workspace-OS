"""Task model — a work item within a project."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hermes_api.db import Base
from hermes_api.enums import TaskPriority, TaskStatus
from hermes_api.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from hermes_api.models.project import Project


class Task(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "tasks"

    # Denormalized workspace_id (matches the multi-tenant scoping in the data model);
    # cascade is handled via the project relationship.
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=TaskStatus.BACKLOG.value
    )
    priority: Mapped[str] = mapped_column(
        String(20), nullable=False, default=TaskPriority.NONE.value
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    project: Mapped[Project] = relationship(back_populates="tasks")
