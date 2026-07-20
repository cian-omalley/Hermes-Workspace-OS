"""Tag API schemas and the tag-attachment payload."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    color: str | None = Field(default=None, max_length=20)


class TagUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    color: str | None = Field(default=None, max_length=20)


class TagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    name: str
    color: str | None
    created_at: datetime
    updated_at: datetime


class TagAttach(BaseModel):
    """Attach a tag to any entity via its type + id."""

    entity_type: str = Field(min_length=1, max_length=50)
    entity_id: uuid.UUID


class TagLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tag_id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    created_at: datetime
