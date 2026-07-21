"""User model — an identity (auth/RBAC is layered on in Milestone 3)."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.db import Base
from hermes_api.models.base import TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    # Nullable: users may be provisioned via an external IdP (OIDC) with no local password.
    password_hash: Mapped[str | None] = mapped_column(String(200), nullable=True)
