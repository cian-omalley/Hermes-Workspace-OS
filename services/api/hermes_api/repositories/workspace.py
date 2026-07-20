"""Workspace repository."""

from __future__ import annotations

from sqlalchemy import select

from hermes_api.models.workspace import Workspace
from hermes_api.repositories.base import Repository


class WorkspaceRepository(Repository[Workspace]):
    model = Workspace

    def get_by_slug(self, slug: str) -> Workspace | None:
        return self.session.scalars(select(Workspace).where(Workspace.slug == slug)).first()
