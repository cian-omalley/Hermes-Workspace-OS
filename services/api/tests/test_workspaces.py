"""CRUD tests for the workspaces API."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_and_get_workspace(client: TestClient) -> None:
    created = client.post("/api/v1/workspaces", json={"name": "Acme", "slug": "acme"})
    assert created.status_code == 201
    body = created.json()
    assert body["name"] == "Acme"
    assert body["slug"] == "acme"

    fetched = client.get(f"/api/v1/workspaces/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == body["id"]


def test_list_workspaces(client: TestClient) -> None:
    client.post("/api/v1/workspaces", json={"name": "One", "slug": "one"})
    client.post("/api/v1/workspaces", json={"name": "Two", "slug": "two"})
    resp = client.get("/api/v1/workspaces")
    assert resp.status_code == 200
    assert {w["slug"] for w in resp.json()} == {"one", "two"}


def test_duplicate_slug_conflicts(client: TestClient) -> None:
    client.post("/api/v1/workspaces", json={"name": "One", "slug": "dup"})
    dup = client.post("/api/v1/workspaces", json={"name": "Two", "slug": "dup"})
    assert dup.status_code == 409


def test_invalid_slug_rejected(client: TestClient) -> None:
    resp = client.post("/api/v1/workspaces", json={"name": "Bad", "slug": "Not Valid!"})
    assert resp.status_code == 422


def test_update_and_delete_workspace(client: TestClient) -> None:
    ws = client.post("/api/v1/workspaces", json={"name": "Acme", "slug": "acme"}).json()
    updated = client.patch(f"/api/v1/workspaces/{ws['id']}", json={"name": "Acme Inc"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Acme Inc"

    deleted = client.delete(f"/api/v1/workspaces/{ws['id']}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/workspaces/{ws['id']}").status_code == 404


def test_get_missing_workspace_returns_404(client: TestClient) -> None:
    missing = "00000000-0000-0000-0000-000000000000"
    assert client.get(f"/api/v1/workspaces/{missing}").status_code == 404
