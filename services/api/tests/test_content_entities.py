"""Data-driven CRUD tests for the workspace-scoped content entities.

Documents, research, repositories, assets, and agents share an identical CRUD surface
(via the generic CrudService), so one parametrized suite covers them all.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest
from fastapi.testclient import TestClient


@dataclass(frozen=True)
class EntityCase:
    segment: str
    create: dict[str, Any]
    update: dict[str, Any]
    update_field: str
    update_expected: Any
    id_key: str = field(default="id")


CASES = [
    EntityCase("documents", {"title": "Spec"}, {"status": "published"}, "status", "published"),
    EntityCase("research", {"title": "Topic"}, {"status": "done"}, "status", "done"),
    EntityCase(
        "repositories",
        {"full_name": "acme/api", "url": "https://github.com/acme/api"},
        {"private": True},
        "private",
        True,
    ),
    EntityCase("assets", {"filename": "report.pdf"}, {"status": "ready"}, "status", "ready"),
    EntityCase("agents", {"name": "PM"}, {"status": "running"}, "status", "running"),
]
IDS = [c.segment for c in CASES]


def _base(workspace_id: str, segment: str) -> str:
    return f"/api/v1/workspaces/{workspace_id}/{segment}"


@pytest.mark.parametrize("case", CASES, ids=IDS)
def test_entity_crud(client: TestClient, workspace_id: str, case: EntityCase) -> None:
    base = _base(workspace_id, case.segment)

    created = client.post(base, json=case.create)
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["workspace_id"] == workspace_id
    entity_id = body[case.id_key]

    assert client.get(base).json()  # list is non-empty
    assert client.get(f"{base}/{entity_id}").status_code == 200

    updated = client.patch(f"{base}/{entity_id}", json=case.update)
    assert updated.status_code == 200
    assert updated.json()[case.update_field] == case.update_expected

    assert client.delete(f"{base}/{entity_id}").status_code == 204
    assert client.get(f"{base}/{entity_id}").status_code == 404


@pytest.mark.parametrize("case", CASES, ids=IDS)
def test_entity_requires_existing_workspace(client: TestClient, case: EntityCase) -> None:
    missing = "00000000-0000-0000-0000-000000000000"
    resp = client.post(_base(missing, case.segment), json=case.create)
    assert resp.status_code == 404


@pytest.mark.parametrize("case", CASES, ids=IDS)
def test_entity_scoped_to_workspace(
    client: TestClient, workspace_id: str, case: EntityCase
) -> None:
    # Create in workspace A, then confirm a second workspace cannot access it.
    entity = client.post(_base(workspace_id, case.segment), json=case.create).json()
    other = client.post("/api/v1/workspaces", json={"name": "Other", "slug": "other"}).json()
    resp = client.get(f"{_base(other['id'], case.segment)}/{entity['id']}")
    assert resp.status_code == 404


def test_content_can_link_to_project(
    client: TestClient, workspace_id: str, project_id: str
) -> None:
    resp = client.post(
        _base(workspace_id, "documents"),
        json={"title": "Linked", "project_id": project_id},
    )
    assert resp.status_code == 201
    assert resp.json()["project_id"] == project_id


def test_content_rejects_foreign_project(client: TestClient, workspace_id: str) -> None:
    missing_project = "00000000-0000-0000-0000-000000000000"
    resp = client.post(
        _base(workspace_id, "documents"),
        json={"title": "Bad", "project_id": missing_project},
    )
    assert resp.status_code == 404
