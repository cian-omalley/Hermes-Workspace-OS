"""Workspace roles and their ordering for RBAC checks."""

from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


# Higher rank = more privilege. A check passes when the member's rank >= the required rank.
_RANK: dict[Role, int] = {
    Role.VIEWER: 1,
    Role.EDITOR: 2,
    Role.ADMIN: 3,
    Role.OWNER: 4,
}


def role_rank(role: str) -> int:
    """Return the privilege rank for a role string (unknown roles rank lowest)."""
    try:
        return _RANK[Role(role)]
    except ValueError:
        return 0
