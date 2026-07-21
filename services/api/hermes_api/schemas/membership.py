"""Workspace membership schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from hermes_api.auth.roles import Role


class MemberAdd(BaseModel):
    email: EmailStr
    role: Role = Role.VIEWER


class MemberRoleUpdate(BaseModel):
    role: Role


class MemberRead(BaseModel):
    id: uuid.UUID = Field(description="Membership id")
    user_id: uuid.UUID
    email: EmailStr
    name: str
    role: Role
    created_at: datetime
