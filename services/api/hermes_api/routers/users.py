"""User routes (top-level)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.schemas.user import UserCreate, UserRead, UserUpdate
from hermes_api.services import ConflictError, NotFoundError, UserService
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, uow: UnitOfWork = Depends(get_uow)) -> UserRead:
    try:
        user = UserService(uow).create(data)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return UserRead.model_validate(user)


@router.get("", response_model=list[UserRead])
def list_users(uow: UnitOfWork = Depends(get_uow)) -> list[UserRead]:
    return [UserRead.model_validate(u) for u in UserService(uow).list()]


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> UserRead:
    try:
        user = UserService(uow).get(user_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: uuid.UUID, data: UserUpdate, uow: UnitOfWork = Depends(get_uow)
) -> UserRead:
    try:
        user = UserService(uow).update(user_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return UserRead.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: uuid.UUID, uow: UnitOfWork = Depends(get_uow)) -> None:
    try:
        UserService(uow).delete(user_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
