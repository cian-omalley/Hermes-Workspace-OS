"""Tag use-cases: workspace tags + polymorphic attachment to entities."""

from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import select

from hermes_api.models.tag import Tag, TagLink
from hermes_api.schemas.tag import TagAttach, TagCreate, TagUpdate
from hermes_api.services.errors import ConflictError, NotFoundError
from hermes_api.uow import UnitOfWork


class TagService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.tags = uow.repo_for(Tag)
        self.links = uow.repo_for(TagLink)

    def _ensure_workspace(self, workspace_id: uuid.UUID) -> None:
        if self.uow.workspaces.get(workspace_id) is None:
            raise NotFoundError(f"Workspace {workspace_id} not found")

    def _by_name(self, workspace_id: uuid.UUID, name: str) -> Tag | None:
        stmt = select(Tag).where(Tag.workspace_id == workspace_id, Tag.name == name)
        return self.uow.session.scalars(stmt).first()

    def create(self, workspace_id: uuid.UUID, data: TagCreate) -> Tag:
        self._ensure_workspace(workspace_id)
        if self._by_name(workspace_id, data.name) is not None:
            raise ConflictError(f"Tag '{data.name}' already exists in this workspace")
        return self.tags.add(Tag(workspace_id=workspace_id, name=data.name, color=data.color))

    def get(self, workspace_id: uuid.UUID, tag_id: uuid.UUID) -> Tag:
        tag = self.tags.get(tag_id)
        if tag is None or tag.workspace_id != workspace_id:
            raise NotFoundError(f"Tag {tag_id} not found")
        return tag

    def list(self, workspace_id: uuid.UUID) -> list[Tag]:
        self._ensure_workspace(workspace_id)
        return self.tags.list(workspace_id=workspace_id)

    def update(self, workspace_id: uuid.UUID, tag_id: uuid.UUID, data: TagUpdate) -> Tag:
        tag = self.get(workspace_id, tag_id)
        if data.name is not None and data.name != tag.name:
            if self._by_name(workspace_id, data.name) is not None:
                raise ConflictError(f"Tag '{data.name}' already exists in this workspace")
            tag.name = data.name
        if data.color is not None:
            tag.color = data.color
        return self.tags.add(tag)

    def delete(self, workspace_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        self.tags.delete(self.get(workspace_id, tag_id))

    def attach(self, workspace_id: uuid.UUID, tag_id: uuid.UUID, data: TagAttach) -> TagLink:
        self.get(workspace_id, tag_id)  # ensures the tag exists in this workspace
        existing = self.uow.session.scalars(
            select(TagLink).where(
                TagLink.tag_id == tag_id,
                TagLink.entity_type == data.entity_type,
                TagLink.entity_id == data.entity_id,
            )
        ).first()
        if existing is not None:
            return existing
        return self.links.add(
            TagLink(tag_id=tag_id, entity_type=data.entity_type, entity_id=data.entity_id)
        )

    def list_links(self, workspace_id: uuid.UUID, tag_id: uuid.UUID) -> Sequence[TagLink]:
        # Sequence (not list[...]) avoids the name colliding with the `list` method above.
        self.get(workspace_id, tag_id)
        return self.links.list(tag_id=tag_id)

    def detach(self, workspace_id: uuid.UUID, tag_id: uuid.UUID, link_id: uuid.UUID) -> None:
        self.get(workspace_id, tag_id)
        link = self.links.get(link_id)
        if link is None or link.tag_id != tag_id:
            raise NotFoundError(f"Tag link {link_id} not found")
        self.links.delete(link)
