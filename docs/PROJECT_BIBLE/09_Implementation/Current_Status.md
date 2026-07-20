# Current Status

## Purpose
The single, honest, live snapshot of what exists **right now**. Update this at every
milestone gate and significant change. If in doubt about project state, this is the file to
trust.

## Current State (as of 2026-07-20)

### Stage
**Milestone 0 — Engineering Foundation: COMPLETE.**
**Milestone 1 — Project Foundation: COMPLETE** (skeleton, tooling, CI — verified).
**Milestone 2 — Database & API: IN PROGRESS.** The core domain model and a full layered
CRUD API now exist for the Workspace → Project → Task hierarchy, with Alembic migrations
and contract tests. Remaining core entities (Document, Repository, Asset, Agent, …) follow
the same pattern in subsequent PRs; auth (M3) is not yet applied.

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
- ✅ **Domain & API (M2):** SQLAlchemy 2.0 models (Workspace, Project, Task) with portable
  types; Alembic migration `0001` (up/down verified); Pydantic schemas; repository +
  unit-of-work; service layer; layered FastAPI routers with full CRUD; OpenAPI published;
  contract tests; `database/` migrations; seed script.
- ✅ **Verified locally:** 30 Python tests + 6 web tests pass; ruff, mypy strict, tsc,
  eslint clean; Next.js production build succeeds; Alembic upgrade/downgrade works;
  end-to-end workspace→project→task CRUD confirmed.

### What does NOT exist yet
- ❌ Remaining core entities (Document, Repository, Asset, Agent, join/tag tables) — same
  pattern, later PRs in M2.
- ❌ Auth, RBAC, secrets, audit (M3) — the API is currently unauthenticated.
- ❌ Integrations, ingestion, search, graph, agents, dashboard, automation (M4–M11).
- ❌ Running services verified via full `docker compose up` in CI (images build locally;
  end-to-end compose bring-up is a manual/CI step to add).

### System-by-system status
| System | Status | Milestone |
|--------|--------|-----------|
| Project foundation / tooling / CI | ✅ Done | M1 |
| Database & API | 🟡 In progress | M2 |
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
Continue **Milestone 2**: add the remaining core entities (Document, Repository, Asset,
Agent, join/tag tables) following the Workspace/Project/Task reference pattern, and generate
the TypeScript client from the OpenAPI schema (the frontend contract seam). Then **Milestone
3 — Authentication** (Auth.js/JWT, RBAC, encrypted secret vault, audit) before exposing sync.

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
