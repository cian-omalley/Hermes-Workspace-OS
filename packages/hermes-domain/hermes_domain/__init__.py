"""Hermes domain layer: framework-independent entities, value objects, and events.

This package intentionally has no third-party runtime dependencies. It defines the
vocabulary the rest of the system speaks. See
``docs/PROJECT_BIBLE/02_Architecture/Technical_Architecture.md``.
"""

from hermes_domain.events import DomainEvent, EventEnvelope

__all__ = ["DomainEvent", "EventEnvelope"]

__version__ = "0.1.0"
