"""Shared test fixtures.

Tests run against an in-memory SQLite database (portable models) so no external services
are needed in CI. The ``get_uow`` dependency is overridden to bind to the test session
factory, ``app.state.session_factory`` is set for the audit middleware, and tables are
created directly from the ORM metadata.

From Milestone 3 the API requires authentication, so the default ``client`` is
authenticated as a registered user who owns the workspaces they create.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from hermes_api.db import Base
from hermes_api.main import create_app
from hermes_api.uow import UnitOfWork, get_uow

DEFAULT_PASSWORD = "sup3rsecret"


@pytest.fixture
def session_factory() -> Iterator[sessionmaker[Session]]:
    # A shared-cache in-memory database: separate connections (like production) all see
    # the same data, so the audit middleware's own session works. A sentinel connection
    # keeps the in-memory database alive for the duration of the test.
    engine = create_engine(
        "sqlite+pysqlite:///file::memory:?cache=shared&uri=true",
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
        future=True,
    )
    sentinel = engine.connect()
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, expire_on_commit=False, future=True)
    sentinel.close()
    engine.dispose()


@pytest.fixture
def app_client(session_factory: sessionmaker[Session]) -> Iterator[TestClient]:
    """An *unauthenticated* TestClient wired to the test database."""
    app = create_app()
    app.state.session_factory = session_factory

    def override_get_uow() -> Iterator[UnitOfWork]:
        with UnitOfWork(session_factory) as uow:
            yield uow
            uow.commit()

    app.dependency_overrides[get_uow] = override_get_uow
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _register_and_login(client: TestClient, email: str, name: str) -> str:
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": name, "password": DEFAULT_PASSWORD},
    )
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": DEFAULT_PASSWORD})
    assert resp.status_code == 200, resp.text
    return str(resp.json()["access_token"])


@pytest.fixture
def unauth_client(app_client: TestClient) -> TestClient:
    return app_client


@pytest.fixture
def client(app_client: TestClient) -> TestClient:
    """Authenticated client (the default owner user)."""
    token = _register_and_login(app_client, "owner@example.com", "Owner")
    app_client.headers.update({"Authorization": f"Bearer {token}"})
    return app_client


@pytest.fixture
def make_user(app_client: TestClient) -> Callable[[str], str]:
    """Factory returning a bearer token for a freshly-registered user."""

    def _make(email: str) -> str:
        return _register_and_login(app_client, email, email.split("@")[0])

    return _make


@pytest.fixture
def workspace_id(client: TestClient) -> str:
    resp = client.post("/api/v1/workspaces", json={"name": "Acme", "slug": "acme"})
    assert resp.status_code == 201, resp.text
    return str(resp.json()["id"])


@pytest.fixture
def project_id(client: TestClient, workspace_id: str) -> str:
    resp = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects",
        json={"key": "ACME", "name": "First Project"},
    )
    assert resp.status_code == 201, resp.text
    return str(resp.json()["id"])
