"""Service-layer errors, mapped to HTTP responses by the routers.

Keeping these framework-independent lets services stay decoupled from FastAPI.
"""

from __future__ import annotations


class ServiceError(Exception):
    """Base class for service-layer errors."""


class NotFoundError(ServiceError):
    """A requested entity does not exist."""


class ConflictError(ServiceError):
    """The operation conflicts with existing state (e.g. duplicate slug)."""
