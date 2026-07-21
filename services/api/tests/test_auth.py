"""Authentication tests: register, login, protected endpoints, audit."""

from __future__ import annotations

from collections.abc import Callable

from fastapi.testclient import TestClient

DEFAULT_PASSWORD = "sup3rsecret"


def test_register_login_and_me(unauth_client: TestClient) -> None:
    reg = unauth_client.post(
        "/api/v1/auth/register",
        json={"email": "a@example.com", "name": "Ada", "password": DEFAULT_PASSWORD},
    )
    assert reg.status_code == 201
    assert "password" not in reg.json()
    assert "password_hash" not in reg.json()

    login = unauth_client.post(
        "/api/v1/auth/login", json={"email": "a@example.com", "password": DEFAULT_PASSWORD}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = unauth_client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "a@example.com"


def test_login_with_wrong_password_fails(unauth_client: TestClient) -> None:
    unauth_client.post(
        "/api/v1/auth/register",
        json={"email": "b@example.com", "name": "B", "password": DEFAULT_PASSWORD},
    )
    resp = unauth_client.post(
        "/api/v1/auth/login", json={"email": "b@example.com", "password": "wrong-password"}
    )
    assert resp.status_code == 401


def test_protected_endpoint_requires_token(unauth_client: TestClient) -> None:
    # No Authorization header → 401/403 from the bearer scheme.
    resp = unauth_client.get("/api/v1/workspaces")
    assert resp.status_code in (401, 403)


def test_invalid_token_rejected(unauth_client: TestClient) -> None:
    resp = unauth_client.get("/api/v1/workspaces", headers={"Authorization": "Bearer not.a.jwt"})
    assert resp.status_code == 401


def test_mutations_are_audited(
    client: TestClient, make_user: Callable[[str], str], workspace_id: str
) -> None:
    # The owner created a workspace (a mutation); confirm it produced an audit record.
    # Read the audit rows through a members-admin-only lens is overkill, so assert via a
    # fresh mutation and the audit table using the app's session factory.
    from sqlalchemy import select

    from hermes_api.models.audit import AuditLog

    factory = client.app.state.session_factory  # type: ignore[attr-defined]
    with factory() as session:
        actions = [row.action for row in session.scalars(select(AuditLog)).all()]
    assert any("/api/v1/workspaces" in a for a in actions)
