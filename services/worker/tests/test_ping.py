"""Tests for the worker skeleton."""

from __future__ import annotations

from hermes_worker.app import app, create_celery, ping


def test_ping_returns_pong() -> None:
    # Call the task body directly (no broker needed) to verify wiring.
    assert ping() == "pong"


def test_celery_app_is_configured() -> None:
    celery_app = create_celery()
    assert celery_app.main == "hermes"
    assert celery_app.conf.task_serializer == "json"
    assert celery_app.conf.enable_utc is True


def test_ping_task_is_registered() -> None:
    assert "hermes.ping" in app.tasks
