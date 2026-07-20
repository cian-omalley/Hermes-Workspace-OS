"""CRUD tests for the users API."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_and_get_user(client: TestClient) -> None:
    created = client.post("/api/v1/users", json={"email": "a@example.com", "name": "Ada"})
    assert created.status_code == 201
    body = created.json()
    assert body["email"] == "a@example.com"
    assert client.get(f"/api/v1/users/{body['id']}").status_code == 200


def test_duplicate_email_conflicts(client: TestClient) -> None:
    client.post("/api/v1/users", json={"email": "dup@example.com", "name": "One"})
    dup = client.post("/api/v1/users", json={"email": "dup@example.com", "name": "Two"})
    assert dup.status_code == 409


def test_invalid_email_rejected(client: TestClient) -> None:
    resp = client.post("/api/v1/users", json={"email": "not-an-email", "name": "X"})
    assert resp.status_code == 422


def test_update_and_delete_user(client: TestClient) -> None:
    user = client.post("/api/v1/users", json={"email": "u@example.com", "name": "U"}).json()
    updated = client.patch(f"/api/v1/users/{user['id']}", json={"name": "Updated"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Updated"
    assert client.delete(f"/api/v1/users/{user['id']}").status_code == 204
    assert client.get(f"/api/v1/users/{user['id']}").status_code == 404
