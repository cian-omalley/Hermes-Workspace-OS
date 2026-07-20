"""Repository API schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from hermes_api.enums import RepositoryProvider


class RepositoryCreate(BaseModel):
    provider: RepositoryProvider = RepositoryProvider.GITHUB
    full_name: str = Field(min_length=1, max_length=300)
    url: str = Field(min_length=1, max_length=1000)
    default_branch: str = Field(default="main", max_length=200)
    private: bool = False
    project_id: uuid.UUID | None = None


class RepositoryUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=300)
    url: str | None = Field(default=None, min_length=1, max_length=1000)
    default_branch: str | None = Field(default=None, max_length=200)
    private: bool | None = None
    project_id: uuid.UUID | None = None


class RepositoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    project_id: uuid.UUID | None
    provider: RepositoryProvider
    full_name: str
    url: str
    default_branch: str
    private: bool
    created_at: datetime
    updated_at: datetime
