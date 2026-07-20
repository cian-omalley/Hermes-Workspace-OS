"""User use-cases (top-level, not workspace-scoped)."""

from __future__ import annotations

import uuid

from sqlalchemy import select

from hermes_api.models.user import User
from hermes_api.schemas.user import UserCreate, UserUpdate
from hermes_api.services.errors import ConflictError, NotFoundError
from hermes_api.uow import UnitOfWork


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.repo = uow.repo_for(User)

    def _by_email(self, email: str) -> User | None:
        return self.uow.session.scalars(select(User).where(User.email == email)).first()

    def create(self, data: UserCreate) -> User:
        if self._by_email(str(data.email)) is not None:
            raise ConflictError(f"User with email '{data.email}' already exists")
        return self.repo.add(
            User(email=str(data.email), name=data.name, avatar_url=data.avatar_url)
        )

    def get(self, user_id: uuid.UUID) -> User:
        user = self.repo.get(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found")
        return user

    def list(self) -> list[User]:
        return self.repo.list()

    def update(self, user_id: uuid.UUID, data: UserUpdate) -> User:
        user = self.get(user_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        return self.repo.add(user)

    def delete(self, user_id: uuid.UUID) -> None:
        self.repo.delete(self.get(user_id))
