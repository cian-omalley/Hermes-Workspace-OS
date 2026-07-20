"""Repository model — a linked source-code repository (GitHub, etc.)."""

from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.db import Base
from hermes_api.enums import RepositoryProvider
from hermes_api.models.base import TimestampMixin, UUIDMixin
from hermes_api.models.mixins import WorkspaceScopedMixin


class Repository(UUIDMixin, WorkspaceScopedMixin, TimestampMixin, Base):
    __tablename__ = "repositories"

    provider: Mapped[str] = mapped_column(
        String(20), nullable=False, default=RepositoryProvider.GITHUB.value
    )
    full_name: Mapped[str] = mapped_column(String(300), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    default_branch: Mapped[str] = mapped_column(String(200), nullable=False, default="main")
    private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
