"""Workspace routes.

Any authenticated user may create a workspace (becoming its owner) and list the
workspaces they belong to. Access to a specific workspace is role-gated: read → member,
update → admin, delete → owner.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.audit import audit
from hermes_api.auth.dependencies import get_current_user, require_workspace_role
from hermes_api.auth.roles import Role
from hermes_api.models.user import User
from hermes_api.schemas.workspace import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate
from hermes_api.services import ConflictError, NotFoundError, WorkspaceService
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v1/workspaces", tags=["workspaces"])


@router.post("", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
def create_workspace(
    data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
) -> WorkspaceRead:
    try:
        workspace = WorkspaceService(uow).create(data, owner_id=current_user.id)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    audit(
        uow.session,
        actor_id=current_user.id,
        workspace_id=workspace.id,
        action="POST /api/v1/workspaces",
        method="POST",
        path="/api/v1/workspaces",
    )
    return WorkspaceRead.model_validate(workspace)


@router.get("", response_model=list[WorkspaceRead])
def list_workspaces(
    current_user: User = Depends(get_current_user), uow: UnitOfWork = Depends(get_uow)
) -> list[WorkspaceRead]:
    workspaces = WorkspaceService(uow).list_for_user(current_user.id)
    return [WorkspaceRead.model_validate(w) for w in workspaces]


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceRead,
    dependencies=[Depends(require_workspace_role(Role.VIEWER))],
)
def get_workspace(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> WorkspaceRead:
    try:
        workspace = WorkspaceService(uow).get(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return WorkspaceRead.model_validate(workspace)


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceRead,
    dependencies=[Depends(require_workspace_role(Role.ADMIN))],
)
def update_workspace(
    workspace_id: uuid.UUID,
    data: WorkspaceUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> WorkspaceRead:
    try:
        workspace = WorkspaceService(uow).update(workspace_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return WorkspaceRead.model_validate(workspace)


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_workspace_role(Role.OWNER))],
)
def delete_workspace(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> None:
    try:
        WorkspaceService(uow).delete(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
