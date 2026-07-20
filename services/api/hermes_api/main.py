"""Hermes API application factory and root routes.

Milestone 1 provides a minimal, real FastAPI app with a health endpoint so the stack
is verifiably runnable and CI has something to exercise. Core domain routers are added
from Milestone 2. See ``docs/PROJECT_BIBLE/04_Integrations/API_Design.md``.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from hermes_api import __version__
from hermes_api.config import Settings, get_settings


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

    return app


app = create_app()
