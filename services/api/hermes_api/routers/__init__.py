"""HTTP routers. Thin: validate + authorize (later) + delegate to services."""

from hermes_api.routers.content import CONTENT_ROUTERS
from hermes_api.routers.projects import router as projects_router
from hermes_api.routers.tags import router as tags_router
from hermes_api.routers.tasks import router as tasks_router
from hermes_api.routers.users import router as users_router
from hermes_api.routers.workspaces import router as workspaces_router

# All routers in registration order (workspaces first so nested resources resolve).
ALL_ROUTERS = [
    workspaces_router,
    projects_router,
    tasks_router,
    users_router,
    tags_router,
    *CONTENT_ROUTERS,
]

__all__ = [
    "ALL_ROUTERS",
    "CONTENT_ROUTERS",
    "projects_router",
    "tags_router",
    "tasks_router",
    "users_router",
    "workspaces_router",
]
