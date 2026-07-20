"""Research item model — a unit of gathered/summarized research."""

from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.db import Base
from hermes_api.enums import ResearchStatus
from hermes_api.models.base import TimestampMixin, UUIDMixin
from hermes_api.models.mixins import WorkspaceScopedMixin


class ResearchItem(UUIDMixin, WorkspaceScopedMixin, TimestampMixin, Base):
    __tablename__ = "research_items"

    title: Mapped[str] = mapped_column(String(300), nullable=False)
    source: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=ResearchStatus.QUEUED.value
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
