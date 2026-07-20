"""Seed the database with a small amount of example data for local development.

Idempotent-ish: creates a demo workspace (skipping if the slug already exists) with one
project and a couple of tasks. Run with:  just seed  (after `just migrate`).
"""

from __future__ import annotations

from hermes_api.enums import TaskPriority, TaskStatus
from hermes_api.schemas.project import ProjectCreate
from hermes_api.schemas.task import TaskCreate
from hermes_api.schemas.workspace import WorkspaceCreate
from hermes_api.services import ProjectService, TaskService, WorkspaceService
from hermes_api.services.errors import ConflictError
from hermes_api.uow import UnitOfWork


def main() -> None:
    with UnitOfWork() as uow:
        workspaces = WorkspaceService(uow)
        try:
            workspace = workspaces.create(WorkspaceCreate(name="Demo Workspace", slug="demo"))
        except ConflictError:
            existing = uow.workspaces.get_by_slug("demo")
            assert existing is not None
            print("Demo workspace already exists; nothing to seed.")
            return

        project = ProjectService(uow).create(
            workspace.id,
            ProjectCreate(key="DEMO", name="Getting Started", description="Sample project"),
        )
        tasks = TaskService(uow)
        tasks.create(
            workspace.id,
            project.id,
            TaskCreate(title="Read the Project Bible", status=TaskStatus.TODO),
        )
        tasks.create(
            workspace.id,
            project.id,
            TaskCreate(
                title="Run the stack", status=TaskStatus.IN_PROGRESS, priority=TaskPriority.HIGH
            ),
        )
        uow.commit()
        print(f"Seeded workspace '{workspace.slug}' with 1 project and 2 tasks.")


if __name__ == "__main__":
    main()
