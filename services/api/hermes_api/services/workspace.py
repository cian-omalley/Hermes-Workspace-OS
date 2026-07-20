"""Workspace use-cases."""

from __future__ import annotations

import uuid

from hermes_api.models.workspace import Workspace
from hermes_api.schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from hermes_api.services.errors import ConflictError, NotFoundError
from hermes_api.uow import UnitOfWork


class WorkspaceService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def create(self, data: WorkspaceCreate) -> Workspace:
        if self.uow.workspaces.get_by_slug(data.slug) is not None:
            raise ConflictError(f"Workspace slug '{data.slug}' already exists")
        return self.uow.workspaces.add(Workspace(name=data.name, slug=data.slug))

    def get(self, workspace_id: uuid.UUID) -> Workspace:
        workspace = self.uow.workspaces.get(workspace_id)
        if workspace is None:
            raise NotFoundError(f"Workspace {workspace_id} not found")
        return workspace

    def list(self) -> list[Workspace]:
        return self.uow.workspaces.list()

    def update(self, workspace_id: uuid.UUID, data: WorkspaceUpdate) -> Workspace:
        workspace = self.get(workspace_id)
        if data.name is not None:
            workspace.name = data.name
        self.uow.workspaces.add(workspace)
        return workspace

    def delete(self, workspace_id: uuid.UUID) -> None:
        self.uow.workspaces.delete(self.get(workspace_id))
