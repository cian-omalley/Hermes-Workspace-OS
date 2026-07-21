# Security Model

## Purpose
Define how Hermes protects data, controls access, manages secrets, and constrains agents.
Security is a design strength that must become an implemented reality.

## Current State
**Implemented (Milestone 3).** The API is authenticated and RBAC-enforced:
- **AuthN:** local credential auth (bcrypt password hashing) issuing signed **JWT** access
  tokens verified at the gateway (`HTTPBearer`); the same seam accepts an external IdP's
  token (Auth.js / Authentik OIDC) later.
- **AuthZ / RBAC:** workspace **memberships** with roles owner/admin/editor/viewer; a
  method-based `workspace_guard` (read→viewer, write→editor) plus fixed-role guards
  (admin for secrets/members, owner to delete a workspace). Non-members get 404 (existence
  not leaked).
- **Secret vault:** provider values are **envelope-encrypted** (Fernet keyed off
  `HERMES_ENCRYPTION_KEY`); only ciphertext is stored, list/read never expose plaintext,
  and reveal is admin-only.
- **Audit log:** mutating actions are recorded in `audit_log` **within the request's unit
  of work** (atomic with the action).
No secrets are committed (verified). The Next.js Auth.js login UI lands with the dashboard
(M10); the backend JWT contract it will consume exists now.

## Layers
| Layer | Control |
|-------|---------|
| **AuthN** | Auth.js (web) + gateway JWT/session verification; optional Authentik OIDC. |
| **AuthZ** | RBAC: workspace/project roles (owner/admin/editor/viewer) + resource-level checks in services. |
| **Multi-tenancy** | Every row scoped by `workspace_id`; optional Postgres RLS for hard isolation (D9). |
| **Secrets** | Provider keys envelope-encrypted at rest (KMS/`age` key); never returned in plaintext. |
| **Agent least privilege** | Per-run tool + permission scope; mutating/external actions can require human approval; sandboxed code execution. |
| **Audit** | Append-only `audit_log` for every sensitive mutation (user/agent/system/integration). |
| **Transport** | TLS everywhere; signed inbound webhooks; gateway rate limiting. |
| **Ingestion safety** | Untrusted files sandboxed; size/type guards; archive-bomb protection; optional AV scan. |

## Threat model (high level)
- **Tenant data leakage** → workspace scoping + ACL-filtered search/RAG + resource checks.
- **Secret exposure** → encrypted vault, no plaintext in API/metadata/logs, rotation.
- **Malicious agent action** → scoped permissions, approval gates, sandbox, audit.
- **Hostile uploads/webhooks** → sandboxing, guards, signature verification, idempotency.
- **Supply chain** → pinned deps, secret scanning, dependency review, `SECURITY.md`.

## Architecture Decisions
1. **Defense in depth for retrieval:** ACLs enforced at the index level *and* re-checked
   after fusion, so search can never leak across tenants/roles.
2. **Secrets are envelope-encrypted**, decrypted only in-process when needed by a provider
   adapter; the model never sees raw secrets.
3. **Agents run with explicit least privilege**, not ambient credentials.
4. **Everything sensitive is audited**, including agent and workflow actions.

## Alternatives Considered
- **Storing provider keys in plaintext config** — rejected outright.
- **Trusting index-level ACLs alone** — rejected in favor of post-fusion re-checks.
- **Giving agents broad tool access** — rejected; scoped per run.

## Future Improvements
Secret rotation automation, per-workspace KMS keys, RLS rollout, anomaly detection on
audit logs, SSO policy controls, signed artifact provenance, and a formal security review
+ `SECURITY.md` before public release (M12).

## Implementation Notes
- Build the secret vault and audit middleware first in M3; wire RBAC into the service layer
  (not just routers).
- Add `SECURITY.md` and enable GitHub secret scanning/dependency review with the first code.
- Sandboxing for the Developer agent's code execution uses isolated containers, never the
  host (`03_Core_Systems/Agent_System.md`).
