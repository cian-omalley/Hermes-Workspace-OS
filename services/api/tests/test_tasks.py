"""CRUD tests for the tasks API."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _base(workspace_id: str, project_id: str) -> str:
    return f"/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks"


def test_create_task_defaults(client: TestClient, workspace_id: str, project_id: str) -> None:
    resp = client.post(_base(workspace_id, project_id), json={"title": "Do the thing"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Do the thing"
    assert body["status"] == "backlog"
    assert body["priority"] == "none"
    assert body["project_id"] == project_id
    assert body["workspace_id"] == workspace_id


def test_task_lifecycle(client: TestClient, workspace_id: str, project_id: str) -> None:
    task = client.post(
        _base(workspace_id, project_id),
        json={"title": "Ship it", "priority": "high"},
    ).json()

    updated = client.patch(
        f"{_base(workspace_id, project_id)}/{task['id']}",
        json={"status": "in_progress", "position": 5},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "in_progress"
    assert updated.json()["position"] == 5

    listing = client.get(_base(workspace_id, project_id))
    assert listing.status_code == 200
    assert len(listing.json()) == 1

    assert client.delete(f"{_base(workspace_id, project_id)}/{task['id']}").status_code == 204
    assert client.get(f"{_base(workspace_id, project_id)}/{task['id']}").status_code == 404


def test_task_in_missing_project_404(client: TestClient, workspace_id: str) -> None:
    missing = "00000000-0000-0000-0000-000000000000"
    resp = client.post(_base(workspace_id, missing), json={"title": "orphan"})
    assert resp.status_code == 404


def test_invalid_priority_rejected(client: TestClient, workspace_id: str, project_id: str) -> None:
    resp = client.post(
        _base(workspace_id, project_id),
        json={"title": "x", "priority": "supercritical"},
    )
    assert resp.status_code == 422
