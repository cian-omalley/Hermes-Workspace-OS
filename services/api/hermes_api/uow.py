"""Unit of Work: the transaction boundary that groups repositories.

A UoW owns a single session/transaction and exposes the repositories that participate in
it. Services perform work through the UoW and the caller commits once at the end, so a
request is atomic. See ``docs/PROJECT_BIBLE/02_Architecture/Technical_Architecture.md``.
"""

from __future__ import annotations

from collections.abc import Iterator
from types import TracebackType

from sqlalchemy.orm import Session, sessionmaker

from hermes_api.db import Base, SessionLocal
from hermes_api.repositories import ProjectRepository, TaskRepository, WorkspaceRepository
from hermes_api.repositories.base import Repository


class UnitOfWork:
    """Groups repositories under one session/transaction."""

    session: Session
    workspaces: WorkspaceRepository
    projects: ProjectRepository
    tasks: TaskRepository

    def __init__(self, session_factory: sessionmaker[Session] = SessionLocal) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> UnitOfWork:
        self.session = self._session_factory()
        self.workspaces = WorkspaceRepository(self.session)
        self.projects = ProjectRepository(self.session)
        self.tasks = TaskRepository(self.session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        # Roll back on error, then always close. Callers commit explicitly on success.
        if exc_type is not None:
            self.session.rollback()
        self.session.close()

    def repo_for[M: Base](self, model: type[M]) -> Repository[M]:
        """Return a generic repository bound to ``model`` on this UoW's session.

        Used by the generic ``CrudService`` for entities that don't need a bespoke
        repository subclass.
        """
        return Repository(self.session, model)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()


def get_uow() -> Iterator[UnitOfWork]:
    """FastAPI dependency yielding a UoW and committing on success.

    Tests override this dependency to bind the UoW to a SQLite session factory.
    """
    with UnitOfWork() as uow:
        yield uow
        uow.commit()
