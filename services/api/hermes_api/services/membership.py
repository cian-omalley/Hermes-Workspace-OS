"""Workspace membership management (RBAC administration)."""

from __future__ import annotations

import uuid

from sqlalchemy import select

from hermes_api.auth.roles import Role
from hermes_api.models.membership import Membership
from hermes_api.models.user import User
from hermes_api.services.errors import ConflictError, NotFoundError
from hermes_api.uow import UnitOfWork


class MembershipService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.repo = uow.repo_for(Membership)

    def list(self, workspace_id: uuid.UUID) -> list[tuple[Membership, User]]:
        stmt = (
            select(Membership, User)
            .join(User, User.id == Membership.user_id)
            .where(Membership.workspace_id == workspace_id)
        )
        return [(row[0], row[1]) for row in self.uow.session.execute(stmt).all()]

    def add(self, workspace_id: uuid.UUID, email: str, role: Role) -> tuple[Membership, User]:
        user = self.uow.session.scalars(select(User).where(User.email == email)).first()
        if user is None:
            raise NotFoundError(f"No user with email '{email}'")
        existing = self.uow.session.scalars(
            select(Membership).where(
                Membership.workspace_id == workspace_id, Membership.user_id == user.id
            )
        ).first()
        if existing is not None:
            raise ConflictError("User is already a member of this workspace")
        membership = self.repo.add(
            Membership(workspace_id=workspace_id, user_id=user.id, role=role.value)
        )
        return membership, user

    def _get(self, workspace_id: uuid.UUID, membership_id: uuid.UUID) -> Membership:
        membership = self.repo.get(membership_id)
        if membership is None or membership.workspace_id != workspace_id:
            raise NotFoundError(f"Membership {membership_id} not found")
        return membership

    def update_role(
        self, workspace_id: uuid.UUID, membership_id: uuid.UUID, role: Role
    ) -> tuple[Membership, User]:
        membership = self._get(workspace_id, membership_id)
        membership.role = role.value
        membership = self.repo.add(membership)
        user = self.uow.repo_for(User).get(membership.user_id)
        assert user is not None  # FK guarantees the user exists
        return membership, user

    def remove(self, workspace_id: uuid.UUID, membership_id: uuid.UUID) -> None:
        self.repo.delete(self._get(workspace_id, membership_id))
