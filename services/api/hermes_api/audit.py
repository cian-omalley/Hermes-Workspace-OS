"""Audit logging.

Audit records are written **into the request's own unit-of-work session** so they commit
atomically with the action they describe (and roll back if the action fails). This is
more reliable than a response middleware, which would write from a separate connection
while the request transaction is still open (causing lock conflicts). See
``docs/PROJECT_BIBLE/02_Architecture/Security_Model.md``.
"""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from hermes_api.models.audit import AuditLog


def audit(
    session: Session,
    *,
    actor_id: uuid.UUID | None,
    action: str,
    workspace_id: uuid.UUID | None = None,
    method: str | None = None,
    path: str | None = None,
    actor_type: str = "user",
) -> None:
    """Stage an audit record on ``session`` (committed by the caller's unit of work)."""
    session.add(
        AuditLog(
            actor_type=actor_type,
            actor_id=actor_id,
            workspace_id=workspace_id,
            action=action,
            method=method,
            path=path,
        )
    )
