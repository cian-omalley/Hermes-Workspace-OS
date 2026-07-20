"""Task use-cases."""

from __future__ import annotations

import uuid

from hermes_api.models.task import Task
from hermes_api.schemas.task import TaskCreate, TaskUpdate
from hermes_api.services.errors import NotFoundError
from hermes_api.uow import UnitOfWork


class TaskService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def _get_project_workspace(self, workspace_id: uuid.UUID, project_id: uuid.UUID) -> None:
        project = self.uow.projects.get(project_id)
        if project is None or project.workspace_id != workspace_id:
            raise NotFoundError(f"Project {project_id} not found")

    def create(self, workspace_id: uuid.UUID, project_id: uuid.UUID, data: TaskCreate) -> Task:
        self._get_project_workspace(workspace_id, project_id)
        return self.uow.tasks.add(
            Task(
                workspace_id=workspace_id,
                project_id=project_id,
                title=data.title,
                description=data.description,
                status=data.status.value,
                priority=data.priority.value,
                position=data.position,
            )
        )

    def get(self, workspace_id: uuid.UUID, project_id: uuid.UUID, task_id: uuid.UUID) -> Task:
        task = self.uow.tasks.get(task_id)
        if task is None or task.project_id != project_id or task.workspace_id != workspace_id:
            raise NotFoundError(f"Task {task_id} not found")
        return task

    def list(self, workspace_id: uuid.UUID, project_id: uuid.UUID) -> list[Task]:
        self._get_project_workspace(workspace_id, project_id)
        return self.uow.tasks.list_for_project(project_id)

    def update(
        self,
        workspace_id: uuid.UUID,
        project_id: uuid.UUID,
        task_id: uuid.UUID,
        data: TaskUpdate,
    ) -> Task:
        task = self.get(workspace_id, project_id, task_id)
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.status is not None:
            task.status = data.status.value
        if data.priority is not None:
            task.priority = data.priority.value
        if data.position is not None:
            task.position = data.position
        return self.uow.tasks.add(task)

    def delete(self, workspace_id: uuid.UUID, project_id: uuid.UUID, task_id: uuid.UUID) -> None:
        self.uow.tasks.delete(self.get(workspace_id, project_id, task_id))
