"""Workspace model — the top-level tenant boundary."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hermes_api.db import Base
from hermes_api.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from hermes_api.models.project import Project


class Workspace(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "workspaces"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)

    projects: Mapped[list[Project]] = relationship(
        back_populates="workspace", cascade="all, delete-orphan"
    )
