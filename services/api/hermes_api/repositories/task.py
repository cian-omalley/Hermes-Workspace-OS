"""Task repository."""

from __future__ import annotations

import uuid

from hermes_api.models.task import Task
from hermes_api.repositories.base import Repository


class TaskRepository(Repository[Task]):
    model = Task

    def list_for_project(self, project_id: uuid.UUID) -> list[Task]:
        return self.list(project_id=project_id)
