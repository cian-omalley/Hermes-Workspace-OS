"""Contract tests: assert the published OpenAPI schema matches the intended surface.

These guard the frontend/backend contract seam (the generated TS client is produced from
this schema). See ``docs/PROJECT_BIBLE/04_Integrations/API_Design.md``.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_core_paths_present(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    paths = schema["paths"]
    assert "/api/v1/workspaces" in paths
    assert "/api/v1/workspaces/{workspace_id}/projects" in paths
    assert "/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}" in paths
    # Remaining core entities added while finishing Milestone 2.
    assert "/api/v1/users" in paths
    for segment in ("documents", "research", "repositories", "assets", "agents", "tags"):
        assert f"/api/v1/workspaces/{{workspace_id}}/{segment}" in paths
    assert "/api/v1/workspaces/{workspace_id}/tags/{tag_id}/links" in paths
    # Auth & RBAC (Milestone 3).
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/me" in paths
    assert "/api/v1/workspaces/{workspace_id}/members" in paths
    assert "/api/v1/workspaces/{workspace_id}/secrets" in paths


def test_crud_methods_declared(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    assert set(paths["/api/v1/workspaces"]) >= {"get", "post"}
    item = paths["/api/v1/workspaces/{workspace_id}"]
    assert set(item) >= {"get", "patch", "delete"}


def test_schemas_published(client: TestClient) -> None:
    components = client.get("/openapi.json").json()["components"]["schemas"]
    for name in ("WorkspaceRead", "ProjectCreate", "TaskRead", "TaskUpdate"):
        assert name in components


def test_status_enum_values_in_schema(client: TestClient) -> None:
    components = client.get("/openapi.json").json()["components"]["schemas"]
    # ProjectStatus enum should be represented with its allowed values.
    status_enum = components["ProjectStatus"]["enum"]
    assert set(status_enum) == {"planned", "active", "paused", "done", "archived"}
