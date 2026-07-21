"""Secret routes (admin-only; guard applied at include time in main.py)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.schemas.secret import SecretCreate, SecretRead, SecretValueRead
from hermes_api.services import ConflictError, NotFoundError, SecretService
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/secrets", tags=["secrets"])


@router.post("", response_model=SecretRead, status_code=status.HTTP_201_CREATED)
def create_secret(
    workspace_id: uuid.UUID, data: SecretCreate, uow: UnitOfWork = Depends(get_uow)
) -> SecretRead:
    try:
        secret = SecretService(uow).create(workspace_id, data.name, data.value, data.provider)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return SecretRead.model_validate(secret)


@router.get("", response_model=list[SecretRead])
def list_secrets(workspace_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> list[SecretRead]:
    return [SecretRead.model_validate(s) for s in SecretService(uow).list(workspace_id)]


@router.get("/{secret_id}/reveal", response_model=SecretValueRead)
def reveal_secret(
    workspace_id: uuid.UUID, secret_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> SecretValueRead:
    service = SecretService(uow)
    try:
        secret = service.get(workspace_id, secret_id)
        value = service.reveal(workspace_id, secret_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return SecretValueRead(id=secret.id, name=secret.name, value=value)


@router.delete("/{secret_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_secret(
    workspace_id: uuid.UUID, secret_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)
) -> None:
    try:
        SecretService(uow).delete(workspace_id, secret_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
