"""Workspace routes."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.schemas.workspace import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate
from hermes_api.services import ConflictError, NotFoundError, WorkspaceService
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v1/workspaces", tags=["workspaces"])


@router.post("", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
def create_workspace(data: WorkspaceCreate, uow: UnitOfWork = Depends(get_uow)) -> WorkspaceRead:
    try:
        workspace = WorkspaceService(uow).create(data)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return WorkspaceRead.model_validate(workspace)


@router.get("", response_model=list[WorkspaceRead])
def list_workspaces(uow: UnitOfWork = Depends(get_uow)) -> list[WorkspaceRead]:
    return [WorkspaceRead.model_validate(w) for w in WorkspaceService(uow).list()]


@router.get("/{workspace_id}", response_model=WorkspaceRead)
def get_workspace(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> WorkspaceRead:
    try:
        workspace = WorkspaceService(uow).get(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return WorkspaceRead.model_validate(workspace)


@router.patch("/{workspace_id}", response_model=WorkspaceRead)
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


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> None:
    try:
        WorkspaceService(uow).delete(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
