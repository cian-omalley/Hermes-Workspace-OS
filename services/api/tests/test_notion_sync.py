"""Notion two-way sync tests (against the in-memory FakeNotionClient)."""

from __future__ import annotations

import httpx
from fastapi.testclient import TestClient

from hermes_api.integrations.notion.client import FakeNotionClient

WEBHOOK_SECRET = "hook-secret"
DATABASES = {"projects": "db_projects", "tasks": "db_tasks"}


def _connect(client: TestClient, workspace_id: str, *, secret: str | None = WEBHOOK_SECRET) -> None:
    resp = client.post(
        f"/api/v1/workspaces/{workspace_id}/integrations/notion/connect",
        json={"token": "secret-token", "databases": DATABASES, "webhook_secret": secret},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["connected"] is True


def _base(workspace_id: str) -> str:
    return f"/api/v1/workspaces/{workspace_id}/integrations/notion"


def _external_id_for(fake: FakeNotionClient, database_id: str, hermes_id: str) -> str:
    for page in fake.query_database(database_id):
        if page["properties"].get("hermes_id") == hermes_id:
            return str(page["id"])
    raise AssertionError("no Notion page found for hermes_id")


def test_connect_status_and_token_stored_encrypted(
    client: TestClient, workspace_id: str, fake_notion: FakeNotionClient
) -> None:
    _connect(client, workspace_id)
    status = client.get(_base(workspace_id)).json()
    assert status["connected"] is True
    assert status["databases"] == DATABASES
    # The token is stored as an encrypted secret (not exposed here); listing secrets shows
    # its name but never its value.
    secrets = client.get(f"/api/v1/workspaces/{workspace_id}/secrets").json()
    assert any(s["name"] == "notion_token" for s in secrets)
    assert all("value" not in s for s in secrets)


def test_sync_out_creates_then_is_idempotent(
    client: TestClient, workspace_id: str, project_id: str, fake_notion: FakeNotionClient
) -> None:
    client.post(
        f"/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks",
        json={"title": "First task"},
    )
    _connect(client, workspace_id)

    first = client.post(f"{_base(workspace_id)}/sync").json()
    assert first["created"] == 2  # one project + one task
    # The Notion side now has pages carrying the hermes_id binding.
    assert len(fake_notion.query_database("db_projects")) == 1
    assert len(fake_notion.query_database("db_tasks")) == 1

    second = client.post(f"{_base(workspace_id)}/sync").json()
    assert second == {"created": 0, "updated": 0, "unchanged": 2, "conflicts": 0}


def test_outbound_pushes_hermes_changes(
    client: TestClient, workspace_id: str, project_id: str, fake_notion: FakeNotionClient
) -> None:
    _connect(client, workspace_id)
    client.post(f"{_base(workspace_id)}/sync")
    external_id = _external_id_for(fake_notion, "db_projects", project_id)

    client.patch(
        f"/api/v1/workspaces/{workspace_id}/projects/{project_id}", json={"name": "Renamed"}
    )
    result = client.post(f"{_base(workspace_id)}/sync").json()
    assert result["updated"] == 1
    page = fake_notion.get_page(external_id)
    assert page is not None
    assert page["properties"]["Name"] == "Renamed"


def _webhook(
    client: TestClient,
    workspace_id: str,
    *,
    event_id: str,
    external_id: str,
    properties: dict[str, str],
    secret: str | None = WEBHOOK_SECRET,
) -> httpx.Response:
    headers = {"X-Hermes-Webhook-Secret": secret} if secret is not None else {}
    response: httpx.Response = client.post(
        f"/webhooks/notion/{workspace_id}",
        json={"event_id": event_id, "external_id": external_id, "properties": properties},
        headers=headers,
    )
    return response


def test_inbound_applies_notion_change(
    client: TestClient, workspace_id: str, project_id: str, fake_notion: FakeNotionClient
) -> None:
    _connect(client, workspace_id)
    client.post(f"{_base(workspace_id)}/sync")
    external_id = _external_id_for(fake_notion, "db_projects", project_id)

    resp = _webhook(
        client,
        workspace_id,
        event_id="evt-1",
        external_id=external_id,
        properties={"Name": "From Notion"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "applied"
    # Hermes (source of record) now reflects the Notion edit.
    project = client.get(f"/api/v1/workspaces/{workspace_id}/projects/{project_id}").json()
    assert project["name"] == "From Notion"


def test_inbound_conflict_hermes_wins(
    client: TestClient, workspace_id: str, project_id: str, fake_notion: FakeNotionClient
) -> None:
    _connect(client, workspace_id)
    client.post(f"{_base(workspace_id)}/sync")
    external_id = _external_id_for(fake_notion, "db_projects", project_id)

    # Hermes changes after the last sync → Hermes must win over an inbound edit.
    client.patch(
        f"/api/v1/workspaces/{workspace_id}/projects/{project_id}", json={"name": "Hermes Wins"}
    )
    resp = _webhook(
        client,
        workspace_id,
        event_id="evt-2",
        external_id=external_id,
        properties={"Name": "Notion Loses"},
    )
    assert resp.json()["status"] == "conflict"
    project = client.get(f"/api/v1/workspaces/{workspace_id}/projects/{project_id}").json()
    assert project["name"] == "Hermes Wins"


def test_webhook_is_idempotent(
    client: TestClient, workspace_id: str, project_id: str, fake_notion: FakeNotionClient
) -> None:
    _connect(client, workspace_id)
    client.post(f"{_base(workspace_id)}/sync")
    external_id = _external_id_for(fake_notion, "db_projects", project_id)

    first = _webhook(
        client, workspace_id, event_id="dup", external_id=external_id, properties={"Name": "X"}
    )
    assert first.json()["status"] == "applied"
    second = _webhook(
        client, workspace_id, event_id="dup", external_id=external_id, properties={"Name": "Y"}
    )
    assert second.json()["status"] == "duplicate"


def test_webhook_rejects_bad_secret(
    client: TestClient, workspace_id: str, project_id: str, fake_notion: FakeNotionClient
) -> None:
    _connect(client, workspace_id)
    client.post(f"{_base(workspace_id)}/sync")
    external_id = _external_id_for(fake_notion, "db_projects", project_id)
    resp = _webhook(
        client,
        workspace_id,
        event_id="evt-3",
        external_id=external_id,
        properties={"Name": "Z"},
        secret="wrong",
    )
    assert resp.status_code == 401
