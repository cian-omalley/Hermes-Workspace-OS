"""Dependency for resolving the Notion client factory.

Defaults to the real HTTP client (see ``create_app``); tests set
``app.state.notion_client_factory`` to a factory returning a ``FakeNotionClient`` so sync
runs entirely in-memory.
"""

from __future__ import annotations

from collections.abc import Callable

from fastapi import Request

from hermes_api.integrations.notion.client import HttpNotionClient, NotionClient

NotionClientFactory = Callable[[str], NotionClient]


def default_notion_client_factory(token: str) -> NotionClient:
    return HttpNotionClient(token)


def get_notion_client_factory(request: Request) -> NotionClientFactory:
    factory: NotionClientFactory = request.app.state.notion_client_factory
    return factory
