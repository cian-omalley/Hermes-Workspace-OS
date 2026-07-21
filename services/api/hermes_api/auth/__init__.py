"""Authentication & authorization (Milestone 3).

Local credential auth issues signed JWTs that the gateway verifies; the same
verification seam accepts tokens from an external IdP (Auth.js / Authentik OIDC). RBAC is
enforced via workspace memberships. See ``docs/PROJECT_BIBLE/02_Architecture/Security_Model.md``.
"""

from hermes_api.auth.roles import Role, role_rank

__all__ = ["Role", "role_rank"]
