# Current Status

## Purpose
The single, honest, live snapshot of what exists **right now**. Update this at every
milestone gate and significant change. If in doubt about project state, this is the file to
trust.

## Current State (as of 2026-07-20)

### Stage
**Milestone 0 — Engineering Foundation: COMPLETE.**
**Milestone 1 — Project Foundation: COMPLETE** (skeleton, tooling, CI — verified).
**Milestone 2 — Database & API: COMPLETE.** The core domain model and a full layered CRUD
API exist for all core entities (Workspace, Project, Task, User, Document, Research,
Repository, Asset, Agent, Tags + tag links), with Alembic migrations, contract tests, and a
**generated TypeScript client** (the frontend/backend contract seam, drift-checked in CI).
Authentication (M3) is the next step — the API is currently unauthenticated.

### What exists
- ✅ 16 numbered design specifications (`docs/00-ROADMAP` … `docs/15-UI_DESIGN`).
- ✅ Complete **Project Bible** (`docs/PROJECT_BIBLE/`, 11 sections, 50+ documents).
- ✅ Audit, Project Map, and Missing Information reports (`docs/`).
- ✅ Repo governance: `README.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`,
  Apache-2.0 `LICENSE`, `.gitignore`, `.github/` templates + CODEOWNERS.
- ✅ **`main` base branch created** (D10 resolved).
- ✅ **Monorepo skeleton (M1):** `services/api` (FastAPI + `/health`, 3 tests),
  `services/worker` (Celery + `ping`, 3 tests), `apps/web` (Next.js shell + health
  dashboard + `/health`, 6 tests), `packages/hermes-domain` (domain events, 4 tests).
- ✅ **Local stack:** `infrastructure/compose/docker-compose.yml` (Postgres, Redis, Neo4j,
  Qdrant, Meilisearch, MinIO + api/web/worker) with health checks; per-service Dockerfiles.
- ✅ **Tooling:** `pyproject.toml` (uv workspace, ruff, mypy strict, pytest), `pnpm`
  workspace, `justfile`, `config/.env.example`.
- ✅ **CI:** GitHub Actions (Python lint/types/tests, web lint/types/tests, secret scan).
- ✅ **Domain & API (M2):** SQLAlchemy 2.0 models for all core entities (Workspace, Project,
  Task, User, Document, ResearchItem, Repository, Asset, Agent, Tag, TagLink) with portable
  types; Alembic migrations `0001`+`0002` (up/down verified); Pydantic schemas; repository +
  unit-of-work; a generic `CrudService` base + bespoke services; 22 layered `/api/v1`
  endpoints with full CRUD (+ tag attach/detach); OpenAPI published; contract tests; seed.
- ✅ **Generated TS client (`packages/ts-client`):** `openapi.json` + `schema.d.ts` generated
  from the API via `openapi-typescript`, a typed `openapi-fetch` wrapper, and a **CI drift
  check** that fails if the committed client diverges from the API.
- ✅ **Verified locally:** 55 Python tests + 6 web tests + 1 client test pass; ruff, mypy
  strict, tsc, eslint clean; Alembic up/down works; client regeneration is deterministic
  (no drift); end-to-end CRUD confirmed.

### What does NOT exist yet
- ❌ Auth, RBAC, secrets, audit (M3) — the API is currently unauthenticated.
- ❌ Postgres-specific features (JSONB/arrays/RLS), document version history, richer agent
  tables — layered in later milestones.
- ❌ The web app does not yet consume `@hermes/ts-client` (wired up in the M10 dashboard).
- ❌ Integrations, ingestion, search, graph, agents, dashboard, automation (M4–M11).
- ❌ Running services verified via full `docker compose up` in CI (images build locally;
  end-to-end compose bring-up is a manual/CI step to add).

### System-by-system status
| System | Status | Milestone |
|--------|--------|-----------|
| Project foundation / tooling / CI | ✅ Done | M1 |
| Database & API (+ TS client) | ✅ Done | M2 |
| Auth / RBAC / secrets / audit | ⏳ Planned | M3 |
| Notion integration | ⏳ Planned | M4 |
| GitHub integration | ⏳ Planned | M5 |
| File ingestion | ⏳ Planned | M6 |
| Search | ⏳ Planned | M7 |
| Knowledge graph / GraphRAG | ⏳ Planned | M8 |
| AI agents | ⏳ Planned | M9 |
| Dashboard | ⏳ Planned | M10 |
| Automation | ⏳ Planned | M11 |
| Deployment / hardening | ⏳ Planned | M12 |

### Open decisions blocking or shaping next steps
See `docs/MISSING_INFORMATION.md`. **D10 (create `main`) is resolved.** Highest remaining:
**D1** (embedding model) and **D5** (default AI provider) — needed before ingestion/AI
work (M6+); `.env.example` currently proposes local (Ollama) defaults.

### Next step
**Milestone 3 — Authentication**: Auth.js/JWT verification at the gateway, optional
Authentik OIDC, RBAC in the service layer (workspace/project roles), an encrypted secret
vault, and audit logging — applied before any external sync (M4/M5).

## Architecture Decisions
This file exists to counter the "documentation implies implementation" risk noted in the
audit — status is stated plainly and kept current.

## Alternatives Considered
Tracking status only in the roadmap — rejected; a dedicated, honest status file is less
likely to be missed.

## Future Improvements
Auto-generate parts of this from CI/coverage/build badges once code exists.

## Implementation Notes
Update this file in the same PR that changes project state; keep it consistent with
`Milestones.md`, `01_Product/Features.md`, and `CHANGELOG.md`.
