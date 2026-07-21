"""Encrypted secret vault + workspace secret use-cases.

Provider credentials are envelope-encrypted with a key derived from
``HERMES_ENCRYPTION_KEY``; plaintext is never persisted and is only returned through an
explicit, admin-guarded read endpoint. See Security_Model.md.
"""

from __future__ import annotations

import base64
import hashlib
import uuid

from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import select

from hermes_api.config import get_settings
from hermes_api.models.secret import Secret
from hermes_api.services.errors import ConflictError, NotFoundError
from hermes_api.uow import UnitOfWork


class SecretVault:
    """Symmetric encryption for secret values, keyed off the app encryption key."""

    def __init__(self, key_material: str | None = None) -> None:
        material = key_material or get_settings().hermes_encryption_key
        derived = base64.urlsafe_b64encode(hashlib.sha256(material.encode("utf-8")).digest())
        self._fernet = Fernet(derived)

    def encrypt(self, plaintext: str) -> bytes:
        return self._fernet.encrypt(plaintext.encode("utf-8"))

    def decrypt(self, ciphertext: bytes) -> str:
        try:
            return self._fernet.decrypt(ciphertext).decode("utf-8")
        except InvalidToken as exc:  # pragma: no cover - defensive
            raise ValueError("Secret could not be decrypted") from exc


class SecretService:
    def __init__(self, uow: UnitOfWork, vault: SecretVault | None = None) -> None:
        self.uow = uow
        self.repo = uow.repo_for(Secret)
        self.vault = vault or SecretVault()

    def _by_name(self, workspace_id: uuid.UUID, name: str) -> Secret | None:
        stmt = select(Secret).where(Secret.workspace_id == workspace_id, Secret.name == name)
        return self.uow.session.scalars(stmt).first()

    def create(
        self, workspace_id: uuid.UUID, name: str, value: str, provider: str | None
    ) -> Secret:
        if self._by_name(workspace_id, name) is not None:
            raise ConflictError(f"Secret '{name}' already exists in this workspace")
        return self.repo.add(
            Secret(
                workspace_id=workspace_id,
                name=name,
                provider=provider,
                ciphertext=self.vault.encrypt(value),
            )
        )

    def list(self, workspace_id: uuid.UUID) -> list[Secret]:
        return self.repo.list(workspace_id=workspace_id)

    def get(self, workspace_id: uuid.UUID, secret_id: uuid.UUID) -> Secret:
        secret = self.repo.get(secret_id)
        if secret is None or secret.workspace_id != workspace_id:
            raise NotFoundError(f"Secret {secret_id} not found")
        return secret

    def reveal(self, workspace_id: uuid.UUID, secret_id: uuid.UUID) -> str:
        return self.vault.decrypt(self.get(workspace_id, secret_id).ciphertext)

    def delete(self, workspace_id: uuid.UUID, secret_id: uuid.UUID) -> None:
        self.repo.delete(self.get(workspace_id, secret_id))
