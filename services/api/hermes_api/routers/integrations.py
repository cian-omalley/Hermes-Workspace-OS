"""Notion integration management routes (admin-only; guard applied in main.py)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.enums import IntegrationProvider
from hermes_api.integrations.deps import NotionClientFactory, get_notion_client_factory
from hermes_api.schemas.integration import (
    IntegrationStatusRead,
    NotionConnectRequest,
    SyncResultRead,
)
from hermes_api.services import IntegrationService, NotFoundError
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(
    prefix="/api/v1/workspaces/{workspace_id}/integrations/notion", tags=["integrations"]
)


def _status(integration: object | None) -> IntegrationStatusRead:
    from hermes_api.models.integration import Integration

    if not isinstance(integration, Integration):
        return IntegrationStatusRead(
            provider="notion", status="disconnected", connected=False, databases={}
        )
    return IntegrationStatusRead(
        provider=integration.provider,
        status=integration.status,
        connected=integration.status == "connected",
        databases=integration.config.get("databases", {}),
    )


@router.get("", response_model=IntegrationStatusRead)
def get_status(
    workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> IntegrationStatusRead:
    integration = IntegrationService(uow).get(workspace_id, IntegrationProvider.NOTION)
    return _status(integration)


@router.post("/connect", response_model=IntegrationStatusRead)
def connect(
    workspace_id: uuid.UUID, data: NotionConnectRequest, uow: UnitOfWork = Depends(get_uow)
) -> IntegrationStatusRead:
    integration = IntegrationService(uow).connect_notion(
        workspace_id, data.token, data.databases, data.webhook_secret
    )
    return _status(integration)


@router.delete("", response_model=IntegrationStatusRead)
def disconnect(
    workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> IntegrationStatusRead:
    try:
        integration = IntegrationService(uow).disconnect_notion(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return _status(integration)


@router.post("/sync", response_model=SyncResultRead)
def sync_outbound(
    workspace_id: uuid.UUID,
    uow: UnitOfWork = Depends(get_uow),
    client_factory: NotionClientFactory = Depends(get_notion_client_factory),
) -> SyncResultRead:
    engine = IntegrationService(uow).build_notion_engine(workspace_id, client_factory)
    if engine is None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Notion is not connected")
    summary = engine.sync_all_out(workspace_id)
    return SyncResultRead(
        created=summary.created,
        updated=summary.updated,
        unchanged=summary.unchanged,
        conflicts=summary.conflicts,
    )
