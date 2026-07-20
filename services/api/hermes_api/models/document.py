"""Document model — Markdown knowledge content within a workspace/project."""

from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.db import Base
from hermes_api.enums import DocumentKind, DocumentStatus
from hermes_api.models.base import TimestampMixin, UUIDMixin
from hermes_api.models.mixins import WorkspaceScopedMixin


class Document(UUIDMixin, WorkspaceScopedMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(String(300), nullable=False)
    kind: Mapped[str] = mapped_column(String(20), nullable=False, default=DocumentKind.DOC.value)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=DocumentStatus.DRAFT.value
    )
    # Milestone 2 stores content inline; full version history (document_versions) is a
    # later addition per docs/05-DATABASE_DESIGN.md.
    content_md: Mapped[str | None] = mapped_column(Text, nullable=True)
