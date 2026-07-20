"""Domain events and the transport envelope used across Hermes.

Events are named ``domain.entity.action`` (e.g. ``project.created``). The
:class:`EventEnvelope` is the on-the-wire shape published to the event bus; the
consistency mechanism (transactional outbox) is described in
``docs/PROJECT_BIBLE/02_Architecture/Data_Flow.md``.

This module uses only the standard library to keep the domain layer dependency-free.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def _new_id() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base class for domain events.

    Concrete events (added from Milestone 2) subclass this and set ``type`` to their
    canonical ``domain.entity.action`` name.
    """

    type: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """The durable, transport-level wrapper around a :class:`DomainEvent`.

    ``id`` is used by consumers for idempotency (dedupe on redelivery), and
    ``trace_id`` correlates work across services.
    """

    type: str
    payload: dict[str, Any]
    workspace_id: str | None = None
    actor: str | None = None
    id: str = field(default_factory=_new_id)
    occurred_at: datetime = field(default_factory=_now)
    trace_id: str | None = None

    @classmethod
    def wrap(
        cls,
        event: DomainEvent,
        *,
        workspace_id: str | None = None,
        actor: str | None = None,
        trace_id: str | None = None,
    ) -> EventEnvelope:
        """Create an envelope from a :class:`DomainEvent`."""
        return cls(
            type=event.type,
            payload=dict(event.payload),
            workspace_id=workspace_id,
            actor=actor,
            trace_id=trace_id,
        )
