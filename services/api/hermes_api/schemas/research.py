"""Research item API schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from hermes_api.enums import ResearchStatus


class ResearchCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    source: str | None = Field(default=None, max_length=2000)
    status: ResearchStatus = ResearchStatus.QUEUED
    summary: str | None = None
    project_id: uuid.UUID | None = None


class ResearchUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    source: str | None = Field(default=None, max_length=2000)
    status: ResearchStatus | None = None
    summary: str | None = None
    project_id: uuid.UUID | None = None


class ResearchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    project_id: uuid.UUID | None
    title: str
    source: str | None
    status: ResearchStatus
    summary: str | None
    created_at: datetime
    updated_at: datetime
