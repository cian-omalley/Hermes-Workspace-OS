"""Authentication use-cases: registration, login, and membership lookups."""

from __future__ import annotations

import uuid

from sqlalchemy import select

from hermes_api.auth.roles import Role
from hermes_api.auth.security import hash_password, verify_password
from hermes_api.models.membership import Membership
from hermes_api.models.user import User
from hermes_api.services.errors import ConflictError
from hermes_api.uow import UnitOfWork


class AuthService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.users = uow.repo_for(User)
        self.memberships = uow.repo_for(Membership)

    def user_by_email(self, email: str) -> User | None:
        return self.uow.session.scalars(select(User).where(User.email == email)).first()

    def register(self, email: str, name: str, password: str) -> User:
        if self.user_by_email(email) is not None:
            raise ConflictError(f"User with email '{email}' already exists")
        return self.users.add(User(email=email, name=name, password_hash=hash_password(password)))

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.user_by_email(email)
        if user is None or user.password_hash is None:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def get_membership(self, workspace_id: uuid.UUID, user_id: uuid.UUID) -> Membership | None:
        stmt = select(Membership).where(
            Membership.workspace_id == workspace_id, Membership.user_id == user_id
        )
        return self.uow.session.scalars(stmt).first()

    def add_membership(self, workspace_id: uuid.UUID, user_id: uuid.UUID, role: Role) -> Membership:
        return self.memberships.add(
            Membership(workspace_id=workspace_id, user_id=user_id, role=role.value)
        )
