"""Project repository."""

from __future__ import annotations

import uuid

from hermes_api.models.project import Project
from hermes_api.repositories.base import Repository


class ProjectRepository(Repository[Project]):
    model = Project

    def list_for_workspace(self, workspace_id: uuid.UUID) -> list[Project]:
        return self.list(workspace_id=workspace_id)
