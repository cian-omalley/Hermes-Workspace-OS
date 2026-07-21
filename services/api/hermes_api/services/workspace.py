"""Workspace use-cases."""

from __future__ import annotations

import uuid

from sqlalchemy import select

from hermes_api.auth.roles import Role
from hermes_api.models.membership import Membership
from hermes_api.models.workspace import Workspace
from hermes_api.schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from hermes_api.services.errors import ConflictError, NotFoundError
from hermes_api.uow import UnitOfWork


class WorkspaceService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def create(self, data: WorkspaceCreate, owner_id: uuid.UUID) -> Workspace:
        if self.uow.workspaces.get_by_slug(data.slug) is not None:
            raise ConflictError(f"Workspace slug '{data.slug}' already exists")
        workspace = self.uow.workspaces.add(Workspace(name=data.name, slug=data.slug))
        # The creator becomes the workspace owner.
        self.uow.repo_for(Membership).add(
            Membership(workspace_id=workspace.id, user_id=owner_id, role=Role.OWNER.value)
        )
        return workspace

    def get(self, workspace_id: uuid.UUID) -> Workspace:
        workspace = self.uow.workspaces.get(workspace_id)
        if workspace is None:
            raise NotFoundError(f"Workspace {workspace_id} not found")
        return workspace

    def list_for_user(self, user_id: uuid.UUID) -> list[Workspace]:
        """Only workspaces the user is a member of."""
        stmt = (
            select(Workspace)
            .join(Membership, Membership.workspace_id == Workspace.id)
            .where(Membership.user_id == user_id)
        )
        return list(self.uow.session.scalars(stmt).all())

    def update(self, workspace_id: uuid.UUID, data: WorkspaceUpdate) -> Workspace:
        workspace = self.get(workspace_id)
        if data.name is not None:
            workspace.name = data.name
        self.uow.workspaces.add(workspace)
        return workspace

    def delete(self, workspace_id: uuid.UUID) -> None:
        self.uow.workspaces.delete(self.get(workspace_id))
