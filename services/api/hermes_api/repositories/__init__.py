"""Repository layer: the only place that talks to the database.

Services depend on repositories (not on the ORM/session directly), keeping persistence
swappable and the domain logic testable. See
``docs/PROJECT_BIBLE/02_Architecture/Technical_Architecture.md``.
"""

from hermes_api.repositories.project import ProjectRepository
from hermes_api.repositories.task import TaskRepository
from hermes_api.repositories.workspace import WorkspaceRepository

__all__ = ["ProjectRepository", "TaskRepository", "WorkspaceRepository"]
