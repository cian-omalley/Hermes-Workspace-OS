"""SQLAlchemy ORM models.

Importing this package registers every model on ``Base.metadata`` (used by Alembic and
by ``create_all`` in tests). Milestone 2 implements the core hierarchy
Workspace → Project → Task; further entities (`docs/05-DATABASE_DESIGN.md`) follow the
same pattern in later milestones.
"""

from hermes_api.models.project import Project
from hermes_api.models.task import Task
from hermes_api.models.workspace import Workspace

__all__ = ["Project", "Task", "Workspace"]
