"""Asset API schemas (metadata; byte upload arrives in Milestone 6)."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from hermes_api.enums import AssetKind, AssetStatus


class AssetCreate(BaseModel):
    kind: AssetKind = AssetKind.FILE
    filename: str = Field(min_length=1, max_length=500)
    mime_type: str | None = Field(default=None, max_length=200)
    size_bytes: int | None = Field(default=None, ge=0)
    status: AssetStatus = AssetStatus.PENDING
    summary: str | None = None
    project_id: uuid.UUID | None = None


class AssetUpdate(BaseModel):
    filename: str | None = Field(default=None, min_length=1, max_length=500)
    status: AssetStatus | None = None
    summary: str | None = None
    project_id: uuid.UUID | None = None


class AssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    project_id: uuid.UUID | None
    kind: AssetKind
    filename: str
    mime_type: str | None
    size_bytes: int | None
    status: AssetStatus
    summary: str | None
    created_at: datetime
    updated_at: datetime
