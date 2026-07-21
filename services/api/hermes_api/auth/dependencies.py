"""FastAPI auth dependencies: current user + workspace RBAC guards."""

from __future__ import annotations

import uuid
from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from hermes_api.audit import audit
from hermes_api.auth.roles import Role, role_rank
from hermes_api.auth.security import decode_access_token
from hermes_api.auth.service import AuthService
from hermes_api.models.membership import Membership
from hermes_api.models.user import User
from hermes_api.uow import UnitOfWork, get_uow

_bearer = HTTPBearer(auto_error=True)

_UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    uow: UnitOfWork = Depends(get_uow),
) -> User:
    """Resolve the authenticated user from a Bearer JWT, or raise 401."""
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    user = uow.repo_for(User).get(user_id)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unknown user")
    return user


def _require(
    request: Request, workspace_id: uuid.UUID, user: User, uow: UnitOfWork, min_rank: int
) -> Membership:
    membership = AuthService(uow).get_membership(workspace_id, user.id)
    if membership is None:
        # 404 (not 403) so membership existence isn't leaked to non-members.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Workspace not found")
    if role_rank(membership.role) < min_rank:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient role for this action")
    # Audit mutating actions within the request's unit of work (commits with the action,
    # rolls back if the endpoint fails).
    if request.method in _UNSAFE_METHODS:
        audit(
            uow.session,
            actor_id=user.id,
            workspace_id=workspace_id,
            action=f"{request.method} {request.url.path}",
            method=request.method,
            path=request.url.path,
        )
    return membership


def workspace_guard(
    request: Request,
    workspace_id: uuid.UUID,
    user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
) -> Membership:
    """Method-based guard: reads need viewer, writes need editor."""
    min_rank = (
        role_rank(Role.EDITOR) if request.method in _UNSAFE_METHODS else role_rank(Role.VIEWER)
    )
    return _require(request, workspace_id, user, uow, min_rank)


def require_workspace_role(min_role: Role) -> Callable[..., Membership]:
    """Dependency factory enforcing a fixed minimum role regardless of method."""

    def dependency(
        request: Request,
        workspace_id: uuid.UUID,
        user: User = Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow),
    ) -> Membership:
        return _require(request, workspace_id, user, uow, role_rank(min_role))

    return dependency
