"""Stable status/priority vocabularies shared by models and schemas.

Stored as strings in the database (portable across SQLite/PostgreSQL) and validated at
the API boundary via these enums. Values mirror ``docs/05-DATABASE_DESIGN.md``.
"""

from __future__ import annotations

from enum import StrEnum


class ProjectStatus(StrEnum):
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    DONE = "done"
    ARCHIVED = "archived"


class TaskStatus(StrEnum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELED = "canceled"


class TaskPriority(StrEnum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
