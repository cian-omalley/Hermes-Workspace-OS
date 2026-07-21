"""Secret model — an envelope-encrypted credential scoped to a workspace.

Only the ciphertext is stored; plaintext never touches the database. See
``docs/PROJECT_BIBLE/02_Architecture/Security_Model.md``.
"""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from hermes_api.db import Base
from hermes_api.models.base import TimestampMixin, UUIDMixin


class Secret(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "secrets"
    __table_args__ = (UniqueConstraint("workspace_id", "name", name="uq_secrets_workspace_name"),)

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ciphertext: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
