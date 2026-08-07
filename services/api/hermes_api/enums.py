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


class DocumentKind(StrEnum):
    DOC = "doc"
    WIKI = "wiki"
    SPEC = "spec"
    NOTE = "note"
    GENERATED = "generated"


class DocumentStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ResearchStatus(StrEnum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"


class RepositoryProvider(StrEnum):
    GITHUB = "github"
    GITLAB = "gitlab"
    OTHER = "other"


class AssetKind(StrEnum):
    FILE = "file"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ARCHIVE = "archive"
    REPO_SNAPSHOT = "repo_snapshot"


class AssetStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class AgentRole(StrEnum):
    PROJECT_MANAGER = "project_manager"
    RESEARCH = "research"
    DOCUMENTATION = "documentation"
    DEVELOPER = "developer"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    RELEASE = "release"
    CUSTOM = "custom"


class AgentStatus(StrEnum):
    IDLE = "idle"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    DISABLED = "disabled"


class IntegrationProvider(StrEnum):
    NOTION = "notion"
    GITHUB = "github"


class IntegrationStatus(StrEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class SyncDirection(StrEnum):
    OUTBOUND = "outbound"
    INBOUND = "inbound"
