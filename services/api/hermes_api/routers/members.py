"""Workspace member management routes (admin-only; guard applied in main.py)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.models.membership import Membership
from hermes_api.models.user import User
from hermes_api.schemas.membership import MemberAdd, MemberRead, MemberRoleUpdate
from hermes_api.services import ConflictError, MembershipService, NotFoundError
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/members", tags=["members"])


def _to_read(membership: Membership, user: User) -> MemberRead:
    return MemberRead(
        id=membership.id,
        user_id=user.id,
        email=user.email,
        name=user.name,
        role=membership.role,
        created_at=membership.created_at,
    )


@router.get("", response_model=list[MemberRead])
def list_members(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> list[MemberRead]:
    return [_to_read(m, u) for m, u in MembershipService(uow).list(workspace_id)]


@router.post("", response_model=MemberRead, status_code=status.HTTP_201_CREATED)
def add_member(
    workspace_id: uuid.UUID, data: MemberAdd, uow: UnitOfWork = Depends(get_uow)
) -> MemberRead:
    try:
        membership, user = MembershipService(uow).add(workspace_id, str(data.email), data.role)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return _to_read(membership, user)


@router.patch("/{membership_id}", response_model=MemberRead)
def update_member_role(
    workspace_id: uuid.UUID,
    membership_id: uuid.UUID,
    data: MemberRoleUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> MemberRead:
    try:
        membership, user = MembershipService(uow).update_role(
            workspace_id, membership_id, data.role
        )
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return _to_read(membership, user)


@router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    workspace_id: uuid.UUID, membership_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> None:
    try:
        MembershipService(uow).remove(workspace_id, membership_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
