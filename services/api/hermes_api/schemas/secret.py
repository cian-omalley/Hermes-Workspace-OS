"""Secret schemas. Values are write-only + admin-reveal; never listed in plaintext."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SecretCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    value: str = Field(min_length=1)
    provider: str | None = Field(default=None, max_length=50)


class SecretRead(BaseModel):
    """Secret metadata — deliberately excludes the value."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    name: str
    provider: str | None
    created_at: datetime
    updated_at: datetime


class SecretValueRead(BaseModel):
    """The decrypted value — returned only from the explicit admin reveal endpoint."""

    id: uuid.UUID
    name: str
    value: str
