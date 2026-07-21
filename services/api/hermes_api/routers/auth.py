"""Authentication routes: register, login, and current-user."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hermes_api.audit import audit
from hermes_api.auth.dependencies import get_current_user
from hermes_api.auth.security import create_access_token
from hermes_api.auth.service import AuthService
from hermes_api.models.user import User
from hermes_api.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from hermes_api.schemas.user import UserRead
from hermes_api.services import ConflictError
from hermes_api.uow import UnitOfWork, get_uow

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, uow: UnitOfWork = Depends(get_uow)) -> UserRead:
    try:
        user = AuthService(uow).register(str(data.email), data.name, data.password)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    audit(uow.session, actor_id=user.id, action="auth.register")
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, uow: UnitOfWork = Depends(get_uow)) -> TokenResponse:
    user = AuthService(uow).authenticate(str(data.email), data.password)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    audit(uow.session, actor_id=user.id, action="auth.login")
    return TokenResponse(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)
