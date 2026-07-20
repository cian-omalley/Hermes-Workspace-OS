"""Generic workspace-scoped CRUD service.

Most core entities (documents, research, repositories, assets, agents, tags) are simple
workspace-scoped records with identical create/read/update/delete/list semantics. This
base captures that once; each entity service is a two-line subclass that sets ``model``.
Bespoke logic (e.g. Workspace/Project/Task) still uses dedicated services.
"""

from __future__ import annotations

import uuid
from typing import Any

from hermes_api.db import Base
from hermes_api.repositories.base import Repository
from hermes_api.services.errors import NotFoundError
from hermes_api.uow import UnitOfWork


class CrudService[ModelT: Base]:
    """CRUD over a workspace-scoped model with an optional ``project_id`` link."""

    model: type[ModelT]
    entity_name: str = "Entity"

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    @property
    def _repo(self) -> Repository[ModelT]:
        return self.uow.repo_for(self.model)

    def _ensure_workspace(self, workspace_id: uuid.UUID) -> None:
        if self.uow.workspaces.get(workspace_id) is None:
            raise NotFoundError(f"Workspace {workspace_id} not found")

    def _ensure_project(self, workspace_id: uuid.UUID, fields: dict[str, Any]) -> None:
        project_id = fields.get("project_id")
        if project_id is None:
            return
        project = self.uow.projects.get(project_id)
        if project is None or project.workspace_id != workspace_id:
            raise NotFoundError(f"Project {project_id} not found")

    def create(self, workspace_id: uuid.UUID, fields: dict[str, Any]) -> ModelT:
        self._ensure_workspace(workspace_id)
        self._ensure_project(workspace_id, fields)
        return self._repo.add(self.model(workspace_id=workspace_id, **fields))

    def get(self, workspace_id: uuid.UUID, entity_id: uuid.UUID) -> ModelT:
        entity = self._repo.get(entity_id)
        if entity is None or entity.workspace_id != workspace_id:  # type: ignore[attr-defined]
            raise NotFoundError(f"{self.entity_name} {entity_id} not found")
        return entity

    def list(self, workspace_id: uuid.UUID) -> list[ModelT]:
        self._ensure_workspace(workspace_id)
        return self._repo.list(workspace_id=workspace_id)

    def update(
        self, workspace_id: uuid.UUID, entity_id: uuid.UUID, fields: dict[str, Any]
    ) -> ModelT:
        entity = self.get(workspace_id, entity_id)
        for key, value in fields.items():
            setattr(entity, key, value)
        return self._repo.add(entity)

    def delete(self, workspace_id: uuid.UUID, entity_id: uuid.UUID) -> None:
        self._repo.delete(self.get(workspace_id, entity_id))
