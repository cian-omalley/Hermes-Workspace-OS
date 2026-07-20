"""Database engine, session factory, and the declarative base.

Uses SQLAlchemy 2.0 with **portable column types** (see ``models/base.py``) so the same
models run on SQLite (tests / zero-config dev) and PostgreSQL (the production source of
record). The engine URL comes from settings (``DATABASE_URL``). See
``docs/PROJECT_BIBLE/05_Data/Database_Architecture.md``.
"""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from hermes_api.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def build_engine(url: str | None = None) -> Engine:
    """Create a SQLAlchemy engine for the given (or configured) database URL."""
    url = url or get_settings().database_url
    # ``check_same_thread`` is a SQLite-only concern (FastAPI's threadpool).
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, future=True, connect_args=connect_args)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a session factory bound to ``engine``."""
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


# Module-level engine/session factory used by the running application. Tests build their
# own SQLite engine and override the ``get_uow`` dependency instead of using these.
engine: Engine = build_engine()
SessionLocal: sessionmaker[Session] = build_session_factory(engine)


def get_session() -> Iterator[Session]:
    """Yield a database session (FastAPI dependency); always closed afterwards."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
