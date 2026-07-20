"""Celery application and a minimal health task.

Milestone 1 provides a real, configured Celery app plus a ``ping`` task so the worker
is verifiably wired up. Task modules for ingestion/sync/indexing are registered from
Milestone 6 onward. See ``docs/PROJECT_BIBLE/03_Core_Systems/*``.
"""

from __future__ import annotations

from celery import Celery

from hermes_worker.config import get_worker_settings


def create_celery() -> Celery:
    """Create and configure the Celery application."""
    settings = get_worker_settings()
    app = Celery(
        "hermes",
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
    )
    app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        task_track_started=True,
        timezone="UTC",
        enable_utc=True,
    )
    return app


app = create_celery()


@app.task(name="hermes.ping")
def ping() -> str:
    """Health task: returns ``"pong"``. Used to verify the worker is processing tasks."""
    return "pong"
