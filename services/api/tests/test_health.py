"""Tests for the API skeleton (health + root)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from hermes_api.config import Settings
from hermes_api.main import create_app


def _client() -> TestClient:
    # Build an app with explicit test settings so tests don't depend on the env.
    settings = Settings(hermes_env="test", api_cors_origins="http://localhost:3000")
    return TestClient(create_app(settings))


def test_health_returns_ok() -> None:
    response = _client().get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "hermes-api"
    assert body["environment"] == "test"
    assert body["version"]


def test_root_points_at_docs() -> None:
    response = _client().get("/")
    assert response.status_code == 200
    assert response.json()["health"] == "/health"


def test_openapi_schema_is_served() -> None:
    response = _client().get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Hermes Workspace OS API"
