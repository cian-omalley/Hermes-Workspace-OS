"""Integration management: connect/disconnect + status, backed by the secret vault."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import Any

from sqlalchemy import select

from hermes_api.enums import IntegrationProvider, IntegrationStatus
from hermes_api.integrations.notion.client import NotionClient
from hermes_api.integrations.notion.engine import NotionSyncEngine
from hermes_api.models.integration import Integration
from hermes_api.services.errors import NotFoundError
from hermes_api.services.secret import SecretService
from hermes_api.uow import UnitOfWork

NotionClientFactory = Callable[[str], NotionClient]

NOTION_TOKEN_SECRET = "notion_token"


class IntegrationService:
    def __init__(self, uow: UnitOfWork, secrets: SecretService | None = None) -> None:
        self.uow = uow
        self.repo = uow.repo_for(Integration)
        self.secrets = secrets or SecretService(uow)

    def get(self, workspace_id: uuid.UUID, provider: IntegrationProvider) -> Integration | None:
        stmt = select(Integration).where(
            Integration.workspace_id == workspace_id, Integration.provider == provider.value
        )
        return self.uow.session.scalars(stmt).first()

    def connect_notion(
        self,
        workspace_id: uuid.UUID,
        token: str,
        databases: dict[str, str],
        webhook_secret: str | None,
    ) -> Integration:
        # Store the token in the encrypted vault (replace any prior value).
        existing_secret = self.secrets._by_name(workspace_id, NOTION_TOKEN_SECRET)
        if existing_secret is not None:
            self.secrets.delete(workspace_id, existing_secret.id)
        self.secrets.create(workspace_id, NOTION_TOKEN_SECRET, token, provider="notion")

        config: dict[str, Any] = {"databases": dict(databases)}
        if webhook_secret is not None:
            config["webhook_secret"] = webhook_secret

        integration = self.get(workspace_id, IntegrationProvider.NOTION)
        if integration is None:
            integration = self.repo.add(
                Integration(
                    workspace_id=workspace_id,
                    provider=IntegrationProvider.NOTION.value,
                    status=IntegrationStatus.CONNECTED.value,
                    secret_name=NOTION_TOKEN_SECRET,
                    config=config,
                )
            )
        else:
            integration.status = IntegrationStatus.CONNECTED.value
            integration.secret_name = NOTION_TOKEN_SECRET
            integration.config = config
            self.repo.add(integration)
        return integration

    def disconnect_notion(self, workspace_id: uuid.UUID) -> Integration:
        integration = self.get(workspace_id, IntegrationProvider.NOTION)
        if integration is None:
            raise NotFoundError("Notion is not connected")
        integration.status = IntegrationStatus.DISCONNECTED.value
        self.repo.add(integration)
        return integration

    def notion_token(self, workspace_id: uuid.UUID, integration: Integration) -> str:
        secret = self.secrets._by_name(workspace_id, integration.secret_name or NOTION_TOKEN_SECRET)
        if secret is None:
            raise NotFoundError("Notion token is missing from the vault")
        return self.secrets.vault.decrypt(secret.ciphertext)

    def build_notion_engine(
        self, workspace_id: uuid.UUID, client_factory: NotionClientFactory
    ) -> NotionSyncEngine | None:
        """Return a ready sync engine, or None if Notion is not connected."""
        integration = self.get(workspace_id, IntegrationProvider.NOTION)
        if integration is None or integration.status != IntegrationStatus.CONNECTED.value:
            return None
        client = client_factory(self.notion_token(workspace_id, integration))
        return NotionSyncEngine(self.uow, client, integration)
