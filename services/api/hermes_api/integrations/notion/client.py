"""Notion client abstraction.

The sync engine depends only on the :class:`NotionClient` protocol (flat string
properties), so it is fully testable against :class:`FakeNotionClient` with no network.
:class:`HttpNotionClient` is the real adapter over Notion's REST API; it translates the
flat properties to Notion's property objects and is exercised via mocked-transport tests
plus a live smoke test (not run in CI).
"""

from __future__ import annotations

import uuid
from typing import Any, Protocol

import httpx

# A Notion "page" in this abstraction: {"id": str, "properties": {name: str-value}}.
NotionPage = dict[str, Any]
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


class NotionClient(Protocol):
    """Minimal page-level Notion operations used by the sync engine."""

    def create_page(self, database_id: str, title_property: str, properties: dict[str, str]) -> str:
        """Create a page in a database; return its external id."""
        ...

    def update_page(self, page_id: str, title_property: str, properties: dict[str, str]) -> None:
        """Update a page's properties."""
        ...

    def get_page(self, page_id: str) -> NotionPage | None:
        """Return a page's flat properties, or None if it doesn't exist."""
        ...

    def query_database(self, database_id: str) -> list[NotionPage]:
        """Return all pages (flat) in a database."""
        ...


class FakeNotionClient:
    """In-memory Notion used by tests and local development.

    Stores flat properties so it round-trips cleanly with the sync engine and lets tests
    simulate external edits via :meth:`update_page`.
    """

    def __init__(self) -> None:
        self._pages: dict[str, NotionPage] = {}

    def create_page(self, database_id: str, title_property: str, properties: dict[str, str]) -> str:
        page_id = str(uuid.uuid4())
        self._pages[page_id] = {
            "id": page_id,
            "database_id": database_id,
            "properties": dict(properties),
        }
        return page_id

    def update_page(self, page_id: str, title_property: str, properties: dict[str, str]) -> None:
        page = self._pages.get(page_id)
        if page is None:
            raise KeyError(page_id)
        page["properties"].update(properties)

    def get_page(self, page_id: str) -> NotionPage | None:
        return self._pages.get(page_id)

    def query_database(self, database_id: str) -> list[NotionPage]:
        return [p for p in self._pages.values() if p.get("database_id") == database_id]

    # Test helper (not part of the protocol).
    def edit_property(self, page_id: str, prop: str, value: str) -> None:
        self._pages[page_id]["properties"][prop] = value


def _to_notion_properties(title_property: str, properties: dict[str, str]) -> dict[str, Any]:
    """Translate flat string properties into Notion's property objects."""
    out: dict[str, Any] = {}
    for name, value in properties.items():
        if name == title_property:
            out[name] = {"title": [{"text": {"content": value}}]}
        else:
            out[name] = {"rich_text": [{"text": {"content": value}}]}
    return out


def _from_notion_properties(properties: dict[str, Any]) -> dict[str, str]:
    """Best-effort flatten of Notion property objects back to strings."""
    flat: dict[str, str] = {}
    for name, prop in properties.items():
        if not isinstance(prop, dict):
            continue
        if "title" in prop:
            flat[name] = "".join(
                part.get("plain_text", part.get("text", {}).get("content", ""))
                for part in prop["title"]
            )
        elif "rich_text" in prop:
            flat[name] = "".join(
                part.get("plain_text", part.get("text", {}).get("content", ""))
                for part in prop["rich_text"]
            )
        elif prop.get("select"):
            flat[name] = str(prop["select"].get("name", ""))
    return flat


class HttpNotionClient:
    """Real Notion REST client. Requires a live smoke test; not run in CI."""

    def __init__(self, token: str, *, http: httpx.Client | None = None) -> None:
        self._http = http or httpx.Client(base_url=NOTION_API, timeout=30.0)
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def create_page(self, database_id: str, title_property: str, properties: dict[str, str]) -> str:
        body = {
            "parent": {"database_id": database_id},
            "properties": _to_notion_properties(title_property, properties),
        }
        resp = self._http.post("/pages", json=body, headers=self._headers)
        resp.raise_for_status()
        return str(resp.json()["id"])

    def update_page(self, page_id: str, title_property: str, properties: dict[str, str]) -> None:
        body = {"properties": _to_notion_properties(title_property, properties)}
        resp = self._http.patch(f"/pages/{page_id}", json=body, headers=self._headers)
        resp.raise_for_status()

    def get_page(self, page_id: str) -> NotionPage | None:
        resp = self._http.get(f"/pages/{page_id}", headers=self._headers)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()
        return {"id": data["id"], "properties": _from_notion_properties(data.get("properties", {}))}

    def query_database(self, database_id: str) -> list[NotionPage]:
        resp = self._http.post(f"/databases/{database_id}/query", json={}, headers=self._headers)
        resp.raise_for_status()
        return [
            {"id": row["id"], "properties": _from_notion_properties(row.get("properties", {}))}
            for row in resp.json().get("results", [])
        ]
