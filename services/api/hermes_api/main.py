"""Hermes API application factory and root routes.

Milestone 1 provides a minimal, real FastAPI app with a health endpoint so the stack
is verifiably runnable and CI has something to exercise. Core domain routers are added
from Milestone 2. See ``docs/PROJECT_BIBLE/04_Integrations/API_Design.md``.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from hermes_api import __version__
from hermes_api.auth.dependencies import get_current_user, require_workspace_role, workspace_guard
from hermes_api.auth.roles import Role
from hermes_api.config import Settings, get_settings
from hermes_api.db import SessionLocal
from hermes_api.routers import (
    ADMIN_ROUTERS,
    WORKSPACE_SCOPED_ROUTERS,
    auth_router,
    users_router,
    workspaces_router,
)


class HealthResponse(BaseModel):
    """Response body for the health endpoint."""

    status: str
    service: str
    version: str
    environment: str


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Using a factory keeps the app testable (tests build an app with overridden
    settings) and mirrors the layered architecture described in the Project Bible.
    """
    settings = settings or get_settings()

    app = FastAPI(
        title="Hermes Workspace OS API",
        version=__version__,
        summary="Self-hostable AI Workspace Operating System — core API.",
    )

    # Session factory used by request dependencies. Tests set this to a SQLite factory;
    # production uses the configured database.
    app.state.session_factory = SessionLocal

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", response_model=HealthResponse, tags=["system"])
    def health() -> HealthResponse:
        """Liveness/readiness probe used by the compose stack and CI."""
        return HealthResponse(
            status="ok",
            service="hermes-api",
            version=__version__,
            environment=settings.hermes_env,
        )

    @app.get("/", tags=["system"])
    def root() -> dict[str, str]:
        """Friendly root pointing at the API docs."""
        return {"name": "Hermes Workspace OS API", "docs": "/docs", "health": "/health"}

    # Public auth routes (register/login; /auth/me self-guards).
    app.include_router(auth_router)
    # Workspaces: create/list require auth; per-workspace routes are role-gated in-router.
    app.include_router(workspaces_router)
    # Users require authentication.
    app.include_router(users_router, dependencies=[Depends(get_current_user)])
    # Workspace-scoped resources: method-based RBAC (read → viewer, write → editor).
    for router in WORKSPACE_SCOPED_ROUTERS:
        app.include_router(router, dependencies=[Depends(workspace_guard)])
    # Admin-only workspace resources (secrets, member management).
    for router in ADMIN_ROUTERS:
        app.include_router(router, dependencies=[Depends(require_workspace_role(Role.ADMIN))])

    return app


app = create_app()
