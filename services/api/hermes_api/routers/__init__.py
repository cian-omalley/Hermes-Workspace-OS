"""HTTP routers, grouped by the authorization guard they need (applied in main.py)."""

from hermes_api.routers.auth import router as auth_router
from hermes_api.routers.content import CONTENT_ROUTERS
from hermes_api.routers.integrations import router as integrations_router
from hermes_api.routers.members import router as members_router
from hermes_api.routers.projects import router as projects_router
from hermes_api.routers.secrets import router as secrets_router
from hermes_api.routers.tags import router as tags_router
from hermes_api.routers.tasks import router as tasks_router
from hermes_api.routers.users import router as users_router
from hermes_api.routers.webhooks import router as webhooks_router
from hermes_api.routers.workspaces import router as workspaces_router

# Workspace-scoped routers guarded by method-based RBAC (read → viewer, write → editor).
WORKSPACE_SCOPED_ROUTERS = [projects_router, tasks_router, tags_router, *CONTENT_ROUTERS]

# Workspace-scoped routers that require admin for every operation.
ADMIN_ROUTERS = [secrets_router, members_router, integrations_router]

# Public routers (no auth): inbound webhooks are signature-verified instead.
PUBLIC_ROUTERS = [webhooks_router]

__all__ = [
    "ADMIN_ROUTERS",
    "PUBLIC_ROUTERS",
    "WORKSPACE_SCOPED_ROUTERS",
    "auth_router",
    "users_router",
    "workspaces_router",
]
