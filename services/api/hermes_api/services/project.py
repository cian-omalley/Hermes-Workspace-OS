"""Project use-cases."""

from __future__ import annotations

import uuid

from hermes_api.models.project import Project
from hermes_api.schemas.project import ProjectCreate, ProjectUpdate
from hermes_api.services.errors import NotFoundError
from hermes_api.uow import UnitOfWork


class ProjectService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def _ensure_workspace(self, workspace_id: uuid.UUID) -> None:
        if self.uow.workspaces.get(workspace_id) is None:
            raise NotFoundError(f"Workspace {workspace_id} not found")

    def create(self, workspace_id: uuid.UUID, data: ProjectCreate) -> Project:
        self._ensure_workspace(workspace_id)
        return self.uow.projects.add(
            Project(
                workspace_id=workspace_id,
                key=data.key,
                name=data.name,
                description=data.description,
                status=data.status.value,
            )
        )

    def get(self, workspace_id: uuid.UUID, project_id: uuid.UUID) -> Project:
        project = self.uow.projects.get(project_id)
        if project is None or project.workspace_id != workspace_id:
            raise NotFoundError(f"Project {project_id} not found")
        return project

    def list(self, workspace_id: uuid.UUID) -> list[Project]:
        self._ensure_workspace(workspace_id)
        return self.uow.projects.list_for_workspace(workspace_id)

    def update(
        self, workspace_id: uuid.UUID, project_id: uuid.UUID, data: ProjectUpdate
    ) -> Project:
        project = self.get(workspace_id, project_id)
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        if data.status is not None:
            project.status = data.status.value
        return self.uow.projects.add(project)

    def delete(self, workspace_id: uuid.UUID, project_id: uuid.UUID) -> None:
        self.uow.projects.delete(self.get(workspace_id, project_id))
