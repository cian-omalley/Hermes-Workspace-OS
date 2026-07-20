"""Task routes (nested under a project)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.schemas.task import TaskCreate, TaskRead, TaskUpdate
from hermes_api.services import NotFoundError, TaskService
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(
    prefix="/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks",
    tags=["tasks"],
)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    data: TaskCreate,
    uow: UnitOfWork = Depends(get_uow),
) -> TaskRead:
    try:
        task = TaskService(uow).create(workspace_id, project_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return TaskRead.model_validate(task)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> list[TaskRead]:
    try:
        tasks = TaskService(uow).list(workspace_id, project_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [TaskRead.model_validate(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> TaskRead:
    try:
        task = TaskService(uow).get(workspace_id, project_id, task_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    data: TaskUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> TaskRead:
    try:
        task = TaskService(uow).update(workspace_id, project_id, task_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    workspace_id: uuid.UUID,
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> None:
    try:
        TaskService(uow).delete(workspace_id, project_id, task_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
