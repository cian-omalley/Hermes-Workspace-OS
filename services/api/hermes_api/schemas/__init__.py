"""Pydantic request/response schemas (the API contract)."""

from hermes_api.schemas.agent import AgentCreate, AgentRead, AgentUpdate
from hermes_api.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from hermes_api.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate
from hermes_api.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from hermes_api.schemas.repository import (
    RepositoryCreate,
    RepositoryRead,
    RepositoryUpdate,
)
from hermes_api.schemas.research import ResearchCreate, ResearchRead, ResearchUpdate
from hermes_api.schemas.tag import (
    TagAttach,
    TagCreate,
    TagLinkRead,
    TagRead,
    TagUpdate,
)
from hermes_api.schemas.task import TaskCreate, TaskRead, TaskUpdate
from hermes_api.schemas.user import UserCreate, UserRead, UserUpdate
from hermes_api.schemas.workspace import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate

__all__ = [
    "AgentCreate",
    "AgentRead",
    "AgentUpdate",
    "AssetCreate",
    "AssetRead",
    "AssetUpdate",
    "DocumentCreate",
    "DocumentRead",
    "DocumentUpdate",
    "ProjectCreate",
    "ProjectRead",
    "ProjectUpdate",
    "RepositoryCreate",
    "RepositoryRead",
    "RepositoryUpdate",
    "ResearchCreate",
    "ResearchRead",
    "ResearchUpdate",
    "TagAttach",
    "TagCreate",
    "TagLinkRead",
    "TagRead",
    "TagUpdate",
    "TaskCreate",
    "TaskRead",
    "TaskUpdate",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "WorkspaceCreate",
    "WorkspaceRead",
    "WorkspaceUpdate",
]
