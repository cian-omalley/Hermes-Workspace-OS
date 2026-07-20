"""Project routes (nested under a workspace)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from hermes_api.services import NotFoundError, ProjectService
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/projects", tags=["projects"])


def _service(uow: UnitOfWork) -> ProjectService:
    return ProjectService(uow)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    workspace_id: uuid.UUID,
    data: ProjectCreate,
    uow: UnitOfWork = Depends(get_uow),
) -> ProjectRead:
    try:
        project = _service(uow).create(workspace_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return ProjectRead.model_validate(project)


@router.get("", response_model=list[ProjectRead])
def list_projects(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> list[ProjectRead]:
    try:
        projects = _service(uow).list(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [ProjectRead.model_validate(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> ProjectRead:
    try:
        project = _service(uow).get(workspace_id, project_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    data: ProjectUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> ProjectRead:
    try:
        project = _service(uow).update(workspace_id, project_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return ProjectRead.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> None:
    try:
        _service(uow).delete(workspace_id, project_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
