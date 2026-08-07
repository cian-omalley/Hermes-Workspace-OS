"""Integration & sync schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class NotionConnectRequest(BaseModel):
    token: str = Field(min_length=1, description="Notion integration token (stored encrypted).")
    databases: dict[str, str] = Field(
        default_factory=dict,
        description="Map of database key ('projects','tasks',…) to Notion database id.",
    )
    webhook_secret: str | None = Field(
        default=None, description="Optional shared secret verified on inbound webhooks."
    )


class IntegrationStatusRead(BaseModel):
    provider: str
    status: str
    connected: bool
    databases: dict[str, str] = Field(default_factory=dict)


class SyncResultRead(BaseModel):
    created: int
    updated: int
    unchanged: int
    conflicts: int


class NotionWebhookEvent(BaseModel):
    """Simplified inbound webhook contract (a real receiver translates Notion's payload)."""

    event_id: str = Field(min_length=1)
    external_id: str = Field(min_length=1)
    properties: dict[str, str] = Field(default_factory=dict)
