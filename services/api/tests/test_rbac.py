"""Role-based access control enforcement tests."""

from __future__ import annotations

from collections.abc import Callable

from fastapi.testclient import TestClient


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _add_member(client: TestClient, workspace_id: str, email: str, role: str) -> None:
    resp = client.post(
        f"/api/v1/workspaces/{workspace_id}/members",
        json={"email": email, "role": role},
    )
    assert resp.status_code == 201, resp.text


def test_non_member_cannot_access_workspace(
    client: TestClient, make_user: Callable[[str], str], workspace_id: str
) -> None:
    outsider = make_user("outsider@example.com")
    # Not a member → workspace is invisible (404, not 403, to avoid leaking existence).
    resp = client.get(f"/api/v1/workspaces/{workspace_id}", headers=_auth(outsider))
    assert resp.status_code == 404


def test_viewer_can_read_but_not_write(
    client: TestClient, make_user: Callable[[str], str], workspace_id: str
) -> None:
    viewer = make_user("viewer@example.com")
    _add_member(client, workspace_id, "viewer@example.com", "viewer")

    projects_url = f"/api/v1/workspaces/{workspace_id}/projects"
    assert client.get(projects_url, headers=_auth(viewer)).status_code == 200
    write = client.post(projects_url, json={"key": "V", "name": "Nope"}, headers=_auth(viewer))
    assert write.status_code == 403


def test_editor_can_write(
    client: TestClient, make_user: Callable[[str], str], workspace_id: str
) -> None:
    editor = make_user("editor@example.com")
    _add_member(client, workspace_id, "editor@example.com", "editor")

    resp = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects",
        json={"key": "ED", "name": "Editor Project"},
        headers=_auth(editor),
    )
    assert resp.status_code == 201


def test_only_owner_can_delete_workspace(
    client: TestClient, make_user: Callable[[str], str], workspace_id: str
) -> None:
    admin = make_user("admin@example.com")
    _add_member(client, workspace_id, "admin@example.com", "admin")
    # Admin can update but not delete.
    assert (
        client.patch(
            f"/api/v1/workspaces/{workspace_id}", json={"name": "Renamed"}, headers=_auth(admin)
        ).status_code
        == 200
    )
    assert (
        client.delete(f"/api/v1/workspaces/{workspace_id}", headers=_auth(admin)).status_code == 403
    )
    # The owner (default client) can delete.
    assert client.delete(f"/api/v1/workspaces/{workspace_id}").status_code == 204


def test_secrets_require_admin(
    client: TestClient, make_user: Callable[[str], str], workspace_id: str
) -> None:
    editor = make_user("ed2@example.com")
    _add_member(client, workspace_id, "ed2@example.com", "editor")
    secrets_url = f"/api/v1/workspaces/{workspace_id}/secrets"
    # Editor is below admin → forbidden.
    assert client.get(secrets_url, headers=_auth(editor)).status_code == 403
    # Owner (admin-rank) can manage secrets.
    assert client.get(secrets_url).status_code == 200
