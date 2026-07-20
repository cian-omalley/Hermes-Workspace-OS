"""CRUD tests for the projects API."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_project(client: TestClient, workspace_id: str) -> None:
    resp = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects",
        json={"key": "PROJ", "name": "My Project", "description": "desc"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["key"] == "PROJ"
    assert body["workspace_id"] == workspace_id
    assert body["status"] == "planned"


def test_create_project_in_missing_workspace_404(client: TestClient) -> None:
    missing = "00000000-0000-0000-0000-000000000000"
    resp = client.post(
        f"/api/v1/workspaces/{missing}/projects",
        json={"key": "X", "name": "Nope"},
    )
    assert resp.status_code == 404


def test_list_projects_scoped_to_workspace(client: TestClient, workspace_id: str) -> None:
    client.post(f"/api/v1/workspaces/{workspace_id}/projects", json={"key": "A", "name": "A"})
    client.post(f"/api/v1/workspaces/{workspace_id}/projects", json={"key": "B", "name": "B"})
    resp = client.get(f"/api/v1/workspaces/{workspace_id}/projects")
    assert resp.status_code == 200
    assert {p["key"] for p in resp.json()} == {"A", "B"}


def test_update_project_status(client: TestClient, workspace_id: str) -> None:
    proj = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects", json={"key": "P", "name": "P"}
    ).json()
    resp = client.patch(
        f"/api/v1/workspaces/{workspace_id}/projects/{proj['id']}",
        json={"status": "active"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "active"


def test_invalid_status_rejected(client: TestClient, workspace_id: str) -> None:
    proj = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects", json={"key": "P", "name": "P"}
    ).json()
    resp = client.patch(
        f"/api/v1/workspaces/{workspace_id}/projects/{proj['id']}",
        json={"status": "nonsense"},
    )
    assert resp.status_code == 422


def test_delete_project(client: TestClient, workspace_id: str) -> None:
    proj = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects", json={"key": "P", "name": "P"}
    ).json()
    assert (
        client.delete(f"/api/v1/workspaces/{workspace_id}/projects/{proj['id']}").status_code == 204
    )
    assert client.get(f"/api/v1/workspaces/{workspace_id}/projects/{proj['id']}").status_code == 404
