"""Unit tests for the real HttpNotionClient request/response translation (mocked HTTP)."""

from __future__ import annotations

import httpx

from hermes_api.integrations.notion.client import HttpNotionClient


def test_create_page_builds_notion_request_and_returns_id() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["auth"] = request.headers.get("Authorization")
        captured["body"] = httpx.Response(200).json if False else request.content
        return httpx.Response(200, json={"id": "page-123"})

    transport = httpx.MockTransport(handler)
    http = httpx.Client(base_url="https://api.notion.com/v1", transport=transport)
    client = HttpNotionClient("tok-abc", http=http)

    page_id = client.create_page("db-1", "Name", {"Name": "Hello", "hermes_id": "u-1"})

    assert page_id == "page-123"
    assert captured["url"] == "https://api.notion.com/v1/pages"
    assert captured["auth"] == "Bearer tok-abc"
    # The flat "Name" became a Notion title property.
    body = captured["body"]
    assert isinstance(body, bytes)
    assert b'"title"' in body
    assert b"Hello" in body


def test_get_page_flattens_properties() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "id": "p1",
                "properties": {
                    "Name": {"title": [{"plain_text": "Proj"}]},
                    "Status": {"rich_text": [{"plain_text": "active"}]},
                },
            },
        )

    http = httpx.Client(
        base_url="https://api.notion.com/v1", transport=httpx.MockTransport(handler)
    )
    client = HttpNotionClient("t", http=http)
    page = client.get_page("p1")
    assert page is not None
    assert page["properties"] == {"Name": "Proj", "Status": "active"}
