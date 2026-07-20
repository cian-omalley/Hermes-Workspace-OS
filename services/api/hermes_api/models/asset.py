"""Asset model — an uploaded/synced file's metadata (bytes handled in Milestone 6)."""

from __future__ import annotations

from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.db import Base
from hermes_api.enums import AssetKind, AssetStatus
from hermes_api.models.base import TimestampMixin, UUIDMixin
from hermes_api.models.mixins import WorkspaceScopedMixin


class Asset(UUIDMixin, WorkspaceScopedMixin, TimestampMixin, Base):
    __tablename__ = "assets"

    kind: Mapped[str] = mapped_column(String(20), nullable=False, default=AssetKind.FILE.value)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(200), nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=AssetStatus.PENDING.value
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
