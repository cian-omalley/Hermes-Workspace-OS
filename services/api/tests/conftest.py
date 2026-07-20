"""Shared test fixtures.

Tests run against an in-memory SQLite database (portable models) so no external services
are needed in CI. The ``get_uow`` dependency is overridden to bind to the test session
factory, and tables are created directly from the ORM metadata.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from hermes_api.db import Base
from hermes_api.main import create_app
from hermes_api.uow import UnitOfWork, get_uow


@pytest.fixture
def session_factory() -> Iterator[sessionmaker[Session]]:
    # A single shared in-memory database for the duration of a test.
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, expire_on_commit=False, future=True)
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(session_factory: sessionmaker[Session]) -> Iterator[TestClient]:
    app = create_app()

    def override_get_uow() -> Iterator[UnitOfWork]:
        with UnitOfWork(session_factory) as uow:
            yield uow
            uow.commit()

    app.dependency_overrides[get_uow] = override_get_uow
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def workspace_id(client: TestClient) -> str:
    resp = client.post("/api/v1/workspaces", json={"name": "Acme", "slug": "acme"})
    assert resp.status_code == 201
    return str(resp.json()["id"])


@pytest.fixture
def project_id(client: TestClient, workspace_id: str) -> str:
    resp = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects",
        json={"key": "ACME", "name": "First Project"},
    )
    assert resp.status_code == 201
    return str(resp.json()["id"])
