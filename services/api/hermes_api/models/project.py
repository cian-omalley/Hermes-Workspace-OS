"""Project model — a unit of work within a workspace."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hermes_api.db import Base
from hermes_api.enums import ProjectStatus
from hermes_api.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from hermes_api.models.task import Task
    from hermes_api.models.workspace import Workspace


class Project(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "projects"

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    key: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=ProjectStatus.PLANNED.value
    )

    workspace: Mapped[Workspace] = relationship(back_populates="projects")
    tasks: Mapped[list[Task]] = relationship(back_populates="project", cascade="all, delete-orphan")
