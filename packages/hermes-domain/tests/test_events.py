"""Tests for the domain event primitives."""

from __future__ import annotations

from datetime import UTC, datetime

from hermes_domain.events import DomainEvent, EventEnvelope


def test_domain_event_defaults() -> None:
    event = DomainEvent(type="project.created")
    assert event.type == "project.created"
    assert event.payload == {}


def test_envelope_wrap_copies_payload_and_sets_metadata() -> None:
    event = DomainEvent(type="task.created", payload={"task_id": "t1"})
    envelope = EventEnvelope.wrap(event, workspace_id="ws1", actor="user:1", trace_id="tr1")

    assert envelope.type == "task.created"
    assert envelope.payload == {"task_id": "t1"}
    assert envelope.workspace_id == "ws1"
    assert envelope.actor == "user:1"
    assert envelope.trace_id == "tr1"
    # A fresh id and timestamp are generated.
    assert envelope.id
    assert envelope.occurred_at.tzinfo == UTC
    assert isinstance(envelope.occurred_at, datetime)


def test_envelope_ids_are_unique() -> None:
    event = DomainEvent(type="asset.uploaded")
    first = EventEnvelope.wrap(event)
    second = EventEnvelope.wrap(event)
    assert first.id != second.id


def test_envelope_payload_is_decoupled_from_event() -> None:
    event = DomainEvent(type="doc.created", payload={"k": "v"})
    envelope = EventEnvelope.wrap(event)
    envelope.payload["k"] = "mutated"
    # Mutating the envelope payload must not affect the original event payload.
    assert event.payload["k"] == "v"
