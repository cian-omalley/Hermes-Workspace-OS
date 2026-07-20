"""Document API schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from hermes_api.enums import DocumentKind, DocumentStatus


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    kind: DocumentKind = DocumentKind.DOC
    status: DocumentStatus = DocumentStatus.DRAFT
    content_md: str | None = None
    project_id: uuid.UUID | None = None


class DocumentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    kind: DocumentKind | None = None
    status: DocumentStatus | None = None
    content_md: str | None = None
    project_id: uuid.UUID | None = None


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    project_id: uuid.UUID | None
    title: str
    kind: DocumentKind
    status: DocumentStatus
    content_md: str | None
    created_at: datetime
    updated_at: datetime
