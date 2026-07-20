"""Agent API schemas (records only; execution arrives in Milestone 9)."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from hermes_api.enums import AgentRole, AgentStatus


class AgentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    role: AgentRole = AgentRole.CUSTOM
    status: AgentStatus = AgentStatus.IDLE
    project_id: uuid.UUID | None = None


class AgentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    role: AgentRole | None = None
    status: AgentStatus | None = None
    project_id: uuid.UUID | None = None


class AgentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    project_id: uuid.UUID | None
    name: str
    role: AgentRole
    status: AgentStatus
    created_at: datetime
    updated_at: datetime
