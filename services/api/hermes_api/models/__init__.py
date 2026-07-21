"""SQLAlchemy ORM models.

Importing this package registers every model on ``Base.metadata`` (used by Alembic and
by ``create_all`` in tests). Milestone 2 implements the core entities from
``docs/05-DATABASE_DESIGN.md``; further entities and join tables follow the same pattern
in later milestones.
"""

from hermes_api.models.agent import Agent
from hermes_api.models.asset import Asset
from hermes_api.models.audit import AuditLog
from hermes_api.models.document import Document
from hermes_api.models.membership import Membership
from hermes_api.models.project import Project
from hermes_api.models.repository import Repository
from hermes_api.models.research import ResearchItem
from hermes_api.models.secret import Secret
from hermes_api.models.tag import Tag, TagLink
from hermes_api.models.task import Task
from hermes_api.models.user import User
from hermes_api.models.workspace import Workspace

__all__ = [
    "Agent",
    "Asset",
    "AuditLog",
    "Document",
    "Membership",
    "Project",
    "Repository",
    "ResearchItem",
    "Secret",
    "Tag",
    "TagLink",
    "Task",
    "User",
    "Workspace",
]
