"""Tag routes: workspace tags plus attach/detach to arbitrary entities."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.schemas.tag import (
    TagAttach,
    TagCreate,
    TagLinkRead,
    TagRead,
    TagUpdate,
)
from hermes_api.services import ConflictError, NotFoundError, TagService
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/tags", tags=["tags"])


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    workspace_id: uuid.UUID, data: TagCreate, uow: UnitOfWork = Depends(get_uow)
) -> TagRead:
    try:
        tag = TagService(uow).create(workspace_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return TagRead.model_validate(tag)


@router.get("", response_model=list[TagRead])
def list_tags(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> list[TagRead]:
    try:
        tags = TagService(uow).list(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [TagRead.model_validate(t) for t in tags]


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(
    workspace_id: uuid.UUID, tag_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> TagRead:
    try:
        tag = TagService(uow).get(workspace_id, tag_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return TagRead.model_validate(tag)


@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(
    workspace_id: uuid.UUID,
    tag_id: uuid.UUID,
    data: TagUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> TagRead:
    try:
        tag = TagService(uow).update(workspace_id, tag_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return TagRead.model_validate(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    workspace_id: uuid.UUID, tag_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> None:
    try:
        TagService(uow).delete(workspace_id, tag_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/{tag_id}/links", response_model=TagLinkRead, status_code=status.HTTP_201_CREATED)
def attach_tag(
    workspace_id: uuid.UUID,
    tag_id: uuid.UUID,
    data: TagAttach,
    uow: UnitOfWork = Depends(get_uow),
) -> TagLinkRead:
    try:
        link = TagService(uow).attach(workspace_id, tag_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return TagLinkRead.model_validate(link)


@router.get("/{tag_id}/links", response_model=list[TagLinkRead])
def list_tag_links(
    workspace_id: uuid.UUID, tag_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> list[TagLinkRead]:
    try:
        links = TagService(uow).list_links(workspace_id, tag_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [TagLinkRead.model_validate(link) for link in links]


@router.delete("/{tag_id}/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def detach_tag(
    workspace_id: uuid.UUID,
    tag_id: uuid.UUID,
    link_id: uuid.UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> None:
    try:
        TagService(uow).detach(workspace_id, tag_id, link_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
