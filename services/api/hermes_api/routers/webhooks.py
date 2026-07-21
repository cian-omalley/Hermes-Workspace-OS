"""Inbound webhook receivers (public, signature-verified — not behind auth).

The Notion receiver uses a simplified event contract and is idempotent via the
``webhook_events`` table. A production receiver translates Notion's native webhook payload
into this contract. See ``docs/07-NOTION_INTEGRATION.md``.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select

from hermes_api.enums import IntegrationProvider
from hermes_api.integrations.deps import NotionClientFactory, get_notion_client_factory
from hermes_api.models.sync import WebhookEvent
from hermes_api.schemas.integration import NotionWebhookEvent
from hermes_api.services import IntegrationService
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/notion/{workspace_id}")
def notion_webhook(
    workspace_id: uuid.UUID,
    data: NotionWebhookEvent,
    uow: UnitOfWork = Depends(get_uow),
    client_factory: NotionClientFactory = Depends(get_notion_client_factory),
    x_hermes_webhook_secret: str | None = Header(default=None),
) -> dict[str, str]:
    service = IntegrationService(uow)
    integration = service.get(workspace_id, IntegrationProvider.NOTION)
    if integration is None or integration.status != "connected":
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Notion is not connected")

    # Verify the shared secret if one was configured at connect time.
    expected = integration.config.get("webhook_secret")
    if expected is not None and x_hermes_webhook_secret != expected:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid webhook signature")

    # Idempotency: dedupe on the event id.
    existing = uow.session.scalars(
        select(WebhookEvent).where(
            WebhookEvent.provider == IntegrationProvider.NOTION.value,
            WebhookEvent.external_id == data.event_id,
        )
    ).first()
    if existing is not None and existing.processed:
        return {"status": "duplicate"}
    if existing is None:
        existing = uow.repo_for(WebhookEvent).add(
            WebhookEvent(
                provider=IntegrationProvider.NOTION.value,
                external_id=data.event_id,
                payload={"external_id": data.external_id, "properties": data.properties},
                processed=False,
            )
        )

    engine = service.build_notion_engine(workspace_id, client_factory)
    assert engine is not None  # integration is connected (checked above)
    action = engine.apply_inbound(data.external_id, data.properties)

    existing.processed = True
    uow.repo_for(WebhookEvent).add(existing)
    return {"status": action}
