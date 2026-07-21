"""Secret vault tests: encrypted storage + admin reveal."""

from __future__ import annotations

from fastapi.testclient import TestClient

from hermes_api.services.secret import SecretVault


def _secrets(workspace_id: str) -> str:
    return f"/api/v1/workspaces/{workspace_id}/secrets"


def test_secret_value_is_not_returned_on_create_or_list(
    client: TestClient, workspace_id: str
) -> None:
    created = client.post(
        _secrets(workspace_id),
        json={"name": "OPENAI_API_KEY", "value": "sk-supersecret", "provider": "openai"},
    )
    assert created.status_code == 201
    body = created.json()
    assert "value" not in body
    assert "ciphertext" not in body
    assert body["name"] == "OPENAI_API_KEY"

    listed = client.get(_secrets(workspace_id)).json()
    assert all("value" not in s for s in listed)


def test_secret_is_stored_encrypted_and_can_be_revealed(
    client: TestClient, workspace_id: str
) -> None:
    plaintext = "sk-supersecret-value"
    created = client.post(_secrets(workspace_id), json={"name": "KEY", "value": plaintext}).json()

    # Admin reveal returns the decrypted value.
    revealed = client.get(f"{_secrets(workspace_id)}/{created['id']}/reveal")
    assert revealed.status_code == 200
    assert revealed.json()["value"] == plaintext


def test_duplicate_secret_name_conflicts(client: TestClient, workspace_id: str) -> None:
    client.post(_secrets(workspace_id), json={"name": "DUP", "value": "a"})
    dup = client.post(_secrets(workspace_id), json={"name": "DUP", "value": "b"})
    assert dup.status_code == 409


def test_vault_roundtrip_and_ciphertext_differs_from_plaintext() -> None:
    vault = SecretVault(key_material="unit-test-key")
    token = vault.encrypt("hello-world")
    assert b"hello-world" not in token
    assert vault.decrypt(token) == "hello-world"
