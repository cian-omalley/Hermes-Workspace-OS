"""End-to-end smoke test: verify the running stack's health endpoints.

Marked ``smoke`` and skipped unless ``HERMES_SMOKE=1`` so it never runs (and fails) in
plain unit-test CI where the stack isn't up. Run it with the stack running:

    just up && HERMES_SMOKE=1 just e2e

This is the Milestone 1 "hello world" e2e that proves the stack is reachable.
"""

from __future__ import annotations

import os
import urllib.request

import pytest

pytestmark = pytest.mark.smoke

API_URL = os.environ.get("HERMES_API_URL", "http://localhost:8000")
WEB_URL = os.environ.get("HERMES_WEB_URL", "http://localhost:3000")

_enabled = os.environ.get("HERMES_SMOKE") == "1"


@pytest.mark.skipif(not _enabled, reason="set HERMES_SMOKE=1 with the stack running")
def test_api_health_is_ok() -> None:
    with urllib.request.urlopen(f"{API_URL}/health", timeout=10) as resp:
        assert resp.status == 200


@pytest.mark.skipif(not _enabled, reason="set HERMES_SMOKE=1 with the stack running")
def test_web_health_is_ok() -> None:
    with urllib.request.urlopen(f"{WEB_URL}/health", timeout=10) as resp:
        assert resp.status == 200
