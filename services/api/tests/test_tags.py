"""CRUD + attach/detach tests for the tags API."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _tags(workspace_id: str) -> str:
    return f"/api/v1/workspaces/{workspace_id}/tags"


def test_create_and_list_tag(client: TestClient, workspace_id: str) -> None:
    created = client.post(_tags(workspace_id), json={"name": "urgent", "color": "#f00"})
    assert created.status_code == 201
    assert created.json()["name"] == "urgent"
    assert len(client.get(_tags(workspace_id)).json()) == 1


def test_duplicate_tag_name_conflicts(client: TestClient, workspace_id: str) -> None:
    client.post(_tags(workspace_id), json={"name": "dup"})
    dup = client.post(_tags(workspace_id), json={"name": "dup"})
    assert dup.status_code == 409


def test_attach_and_detach_tag(client: TestClient, workspace_id: str, project_id: str) -> None:
    tag = client.post(_tags(workspace_id), json={"name": "area"}).json()
    attach = client.post(
        f"{_tags(workspace_id)}/{tag['id']}/links",
        json={"entity_type": "project", "entity_id": project_id},
    )
    assert attach.status_code == 201
    link = attach.json()
    assert link["entity_type"] == "project"
    assert link["entity_id"] == project_id

    assert len(client.get(f"{_tags(workspace_id)}/{tag['id']}/links").json()) == 1

    # Attaching the same target again is idempotent (returns the existing link).
    again = client.post(
        f"{_tags(workspace_id)}/{tag['id']}/links",
        json={"entity_type": "project", "entity_id": project_id},
    )
    assert again.json()["id"] == link["id"]

    detach = client.delete(f"{_tags(workspace_id)}/{tag['id']}/links/{link['id']}")
    assert detach.status_code == 204
    assert client.get(f"{_tags(workspace_id)}/{tag['id']}/links").json() == []


def test_update_and_delete_tag(client: TestClient, workspace_id: str) -> None:
    tag = client.post(_tags(workspace_id), json={"name": "old"}).json()
    updated = client.patch(f"{_tags(workspace_id)}/{tag['id']}", json={"name": "new"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "new"
    assert client.delete(f"{_tags(workspace_id)}/{tag['id']}").status_code == 204
