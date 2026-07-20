"""Generic repository providing typed CRUD over a SQLAlchemy model."""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from hermes_api.db import Base


class Repository[ModelT: Base]:
    """CRUD operations for a single model type, scoped to a session.

    Subclasses set ``model`` as a class attribute. For ad-hoc use (see
    ``UnitOfWork.repo_for``) the model can be passed to the constructor instead.
    """

    model: type[ModelT]

    def __init__(self, session: Session, model: type[ModelT] | None = None) -> None:
        self.session = session
        if model is not None:
            self.model = model

    def get(self, entity_id: uuid.UUID) -> ModelT | None:
        return self.session.get(self.model, entity_id)

    def list(self, **filters: Any) -> list[ModelT]:
        stmt = select(self.model).filter_by(**filters)
        return list(self.session.scalars(stmt).all())

    def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        # Flush (not commit) so the entity gets its server/default values and is usable
        # within the same unit of work; the UoW owns the commit boundary.
        self.session.flush()
        return entity

    def delete(self, entity: ModelT) -> None:
        self.session.delete(entity)
        self.session.flush()
