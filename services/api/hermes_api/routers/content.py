"""Routers for the workspace-scoped content entities.

These follow the same thin pattern as the Workspace/Project/Task routers but delegate to
the generic ``CrudService`` subclasses. Kept in one module because each is a short,
uniform CRUD surface.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.schemas.agent import AgentCreate, AgentRead, AgentUpdate
from hermes_api.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from hermes_api.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate
from hermes_api.schemas.repository import (
    RepositoryCreate,
    RepositoryRead,
    RepositoryUpdate,
)
from hermes_api.schemas.research import ResearchCreate, ResearchRead, ResearchUpdate
from hermes_api.services import (
    AgentService,
    AssetService,
    DocumentService,
    NotFoundError,
    RepositoryService,
    ResearchService,
)
from hermes_api.uow import UnitOfWork, get_uow

# --- Documents -------------------------------------------------------------------------

documents_router = APIRouter(
    prefix="/api/v1/workspaces/{workspace_id}/documents", tags=["documents"]
)


@documents_router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(
    workspace_id: uuid.UUID, data: DocumentCreate, uow: UnitOfWork = Depends(get_uow)
) -> DocumentRead:
    try:
        obj = DocumentService(uow).create(workspace_id, data.model_dump())
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return DocumentRead.model_validate(obj)


@documents_router.get("", response_model=list[DocumentRead])
def list_documents(
    workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> list[DocumentRead]:
    try:
        items = DocumentService(uow).list(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [DocumentRead.model_validate(o) for o in items]


@documents_router.get("/{document_id}", response_model=DocumentRead)
def get_document(
    workspace_id: uuid.UUID, document_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> DocumentRead:
    try:
        obj = DocumentService(uow).get(workspace_id, document_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return DocumentRead.model_validate(obj)


@documents_router.patch("/{document_id}", response_model=DocumentRead)
def update_document(
    workspace_id: uuid.UUID,
    document_id: uuid.UUID,
    data: DocumentUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> DocumentRead:
    try:
        obj = DocumentService(uow).update(
            workspace_id, document_id, data.model_dump(exclude_unset=True)
        )
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return DocumentRead.model_validate(obj)


@documents_router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    workspace_id: uuid.UUID, document_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> None:
    try:
        DocumentService(uow).delete(workspace_id, document_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


# --- Research --------------------------------------------------------------------------

research_router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/research", tags=["research"])


@research_router.post("", response_model=ResearchRead, status_code=status.HTTP_201_CREATED)
def create_research(
    workspace_id: uuid.UUID, data: ResearchCreate, uow: UnitOfWork = Depends(get_uow)
) -> ResearchRead:
    try:
        obj = ResearchService(uow).create(workspace_id, data.model_dump())
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return ResearchRead.model_validate(obj)


@research_router.get("", response_model=list[ResearchRead])
def list_research(
    workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> list[ResearchRead]:
    try:
        items = ResearchService(uow).list(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [ResearchRead.model_validate(o) for o in items]


@research_router.get("/{research_id}", response_model=ResearchRead)
def get_research(
    workspace_id: uuid.UUID, research_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> ResearchRead:
    try:
        obj = ResearchService(uow).get(workspace_id, research_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return ResearchRead.model_validate(obj)


@research_router.patch("/{research_id}", response_model=ResearchRead)
def update_research(
    workspace_id: uuid.UUID,
    research_id: uuid.UUID,
    data: ResearchUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> ResearchRead:
    try:
        obj = ResearchService(uow).update(
            workspace_id, research_id, data.model_dump(exclude_unset=True)
        )
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return ResearchRead.model_validate(obj)


@research_router.delete("/{research_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research(
    workspace_id: uuid.UUID, research_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> None:
    try:
        ResearchService(uow).delete(workspace_id, research_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


# --- Repositories ----------------------------------------------------------------------

repositories_router = APIRouter(
    prefix="/api/v1/workspaces/{workspace_id}/repositories", tags=["repositories"]
)


@repositories_router.post("", response_model=RepositoryRead, status_code=status.HTTP_201_CREATED)
def create_repository(
    workspace_id: uuid.UUID, data: RepositoryCreate, uow: UnitOfWork = Depends(get_uow)
) -> RepositoryRead:
    try:
        obj = RepositoryService(uow).create(workspace_id, data.model_dump())
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return RepositoryRead.model_validate(obj)


@repositories_router.get("", response_model=list[RepositoryRead])
def list_repositories(
    workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> list[RepositoryRead]:
    try:
        items = RepositoryService(uow).list(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [RepositoryRead.model_validate(o) for o in items]


@repositories_router.get("/{repository_id}", response_model=RepositoryRead)
def get_repository(
    workspace_id: uuid.UUID, repository_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> RepositoryRead:
    try:
        obj = RepositoryService(uow).get(workspace_id, repository_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return RepositoryRead.model_validate(obj)


@repositories_router.patch("/{repository_id}", response_model=RepositoryRead)
def update_repository(
    workspace_id: uuid.UUID,
    repository_id: uuid.UUID,
    data: RepositoryUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> RepositoryRead:
    try:
        obj = RepositoryService(uow).update(
            workspace_id, repository_id, data.model_dump(exclude_unset=True)
        )
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return RepositoryRead.model_validate(obj)


@repositories_router.delete("/{repository_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repository(
    workspace_id: uuid.UUID, repository_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> None:
    try:
        RepositoryService(uow).delete(workspace_id, repository_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


# --- Assets ----------------------------------------------------------------------------

assets_router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/assets", tags=["assets"])


@assets_router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset(
    workspace_id: uuid.UUID, data: AssetCreate, uow: UnitOfWork = Depends(get_uow)
) -> AssetRead:
    try:
        obj = AssetService(uow).create(workspace_id, data.model_dump())
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return AssetRead.model_validate(obj)


@assets_router.get("", response_model=list[AssetRead])
def list_assets(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> list[AssetRead]:
    try:
        items = AssetService(uow).list(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [AssetRead.model_validate(o) for o in items]


@assets_router.get("/{asset_id}", response_model=AssetRead)
def get_asset(
    workspace_id: uuid.UUID, asset_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> AssetRead:
    try:
        obj = AssetService(uow).get(workspace_id, asset_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return AssetRead.model_validate(obj)


@assets_router.patch("/{asset_id}", response_model=AssetRead)
def update_asset(
    workspace_id: uuid.UUID,
    asset_id: uuid.UUID,
    data: AssetUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> AssetRead:
    try:
        obj = AssetService(uow).update(workspace_id, asset_id, data.model_dump(exclude_unset=True))
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return AssetRead.model_validate(obj)


@assets_router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    workspace_id: uuid.UUID, asset_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> None:
    try:
        AssetService(uow).delete(workspace_id, asset_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


# --- Agents ----------------------------------------------------------------------------

agents_router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/agents", tags=["agents"])


@agents_router.post("", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(
    workspace_id: uuid.UUID, data: AgentCreate, uow: UnitOfWork = Depends(get_uow)
) -> AgentRead:
    try:
        obj = AgentService(uow).create(workspace_id, data.model_dump())
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return AgentRead.model_validate(obj)


@agents_router.get("", response_model=list[AgentRead])
def list_agents(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> list[AgentRead]:
    try:
        items = AgentService(uow).list(workspace_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return [AgentRead.model_validate(o) for o in items]


@agents_router.get("/{agent_id}", response_model=AgentRead)
def get_agent(
    workspace_id: uuid.UUID, agent_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> AgentRead:
    try:
        obj = AgentService(uow).get(workspace_id, agent_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return AgentRead.model_validate(obj)


@agents_router.patch("/{agent_id}", response_model=AgentRead)
def update_agent(
    workspace_id: uuid.UUID,
    agent_id: uuid.UUID,
    data: AgentUpdate,
    uow: UnitOfWork = Depends(get_uow),
) -> AgentRead:
    try:
        obj = AgentService(uow).update(workspace_id, agent_id, data.model_dump(exclude_unset=True))
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return AgentRead.model_validate(obj)


@agents_router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(
    workspace_id: uuid.UUID, agent_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> None:
    try:
        AgentService(uow).delete(workspace_id, agent_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


CONTENT_ROUTERS = [
    documents_router,
    research_router,
    repositories_router,
    assets_router,
    agents_router,
]
