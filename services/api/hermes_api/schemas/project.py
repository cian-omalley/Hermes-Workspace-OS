"""Project API schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from hermes_api.enums import ProjectStatus


class ProjectCreate(BaseModel):
    key: str = Field(min_length=1, max_length=20, pattern=r"^[A-Z0-9]+$")
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: ProjectStatus = ProjectStatus.PLANNED


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: ProjectStatus | None = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    key: str
    name: str
    description: str | None
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
