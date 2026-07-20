"""HTTP routers. Thin: validate + authorize (later) + delegate to services."""

from hermes_api.routers.projects import router as projects_router
from hermes_api.routers.tasks import router as tasks_router
from hermes_api.routers.workspaces import router as workspaces_router

__all__ = ["projects_router", "tasks_router", "workspaces_router"]
