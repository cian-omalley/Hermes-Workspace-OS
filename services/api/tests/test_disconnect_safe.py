"""The headline resilience guarantee: Hermes works fully without Notion connected."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_core_crud_works_without_notion(client: TestClient, workspace_id: str) -> None:
    # A full project → task flow with NO integration configured.
    project = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects",
        json={"key": "NN", "name": "No Notion"},
    ).json()
    tasks_url = f"/api/v1/workspaces/{workspace_id}/projects/{project['id']}/tasks"
    task = client.post(tasks_url, json={"title": "Works offline"})
    assert task.status_code == 201
    assert client.get(tasks_url).status_code == 200
    # Status reports disconnected rather than erroring.
    status = client.get(f"/api/v1/workspaces/{workspace_id}/integrations/notion").json()
    assert status["connected"] is False


def test_sync_when_not_connected_returns_conflict(client: TestClient, workspace_id: str) -> None:
    resp = client.post(f"/api/v1/workspaces/{workspace_id}/integrations/notion/sync")
    assert resp.status_code == 409


def test_disconnect_then_sync_is_blocked(client: TestClient, workspace_id: str) -> None:
    client.post(
        f"/api/v1/workspaces/{workspace_id}/integrations/notion/connect",
        json={"token": "t", "databases": {"projects": "p", "tasks": "tk"}},
    )
    assert (
        client.delete(f"/api/v1/workspaces/{workspace_id}/integrations/notion").json()["connected"]
        is False
    )
    # After disconnect, sync is refused but core data is untouched.
    assert (
        client.post(f"/api/v1/workspaces/{workspace_id}/integrations/notion/sync").status_code
        == 409
    )
