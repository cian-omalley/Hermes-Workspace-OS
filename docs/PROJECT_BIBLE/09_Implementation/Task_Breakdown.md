# Task Breakdown

## Purpose
Turn the next milestone into a concrete, actionable task list so implementation can start
immediately once approved. Focused on **Milestone 1** (the next step); later milestones are
summarized.

## Current State
No tasks executed (still M0). This is the ready-to-go backlog for M1, plus pointers for
M2–M3.

## Pre-M1 (housekeeping / decisions)
- [ ] **D10:** create `main` base branch from the foundation; set default + protection.
- [ ] Resolve/confirm **D1** (embedding model) and **D5** (default AI provider) enough to
  write `.env.example`.
- [ ] Add `.github/` issue + PR templates and `CODEOWNERS`.

## Milestone 1 — Project Foundation
### Monorepo & tooling
- [ ] Create monorepo layout **with real content** (`apps/web`, `services/api`,
  `services/worker`, `packages/hermes-domain`, `packages/hermes-core`,
  `packages/hermes-plugins`, `infrastructure/`, `config/`, `scripts/`, `tests/`).
- [ ] Python: `pyproject.toml` (uv), ruff + mypy(strict) + pytest configured.
- [ ] TS: `pnpm` workspace, Next.js app, eslint + prettier + tsc(strict) + vitest.
- [ ] `just`/Makefile with `check`, `test`, `e2e`, `migrate`, `api`, `web`, `worker`.

### Local stack
- [ ] `infrastructure/compose/docker-compose.yml`: Postgres, Redis, Neo4j, Qdrant,
  Meilisearch, MinIO (+ placeholders for api/web/worker).
- [ ] `config/.env.example` documenting all required config/secrets.
- [ ] Health-check endpoints (api, web) + aggregated stack health.

### CI
- [ ] GitHub Actions: lint → type-check → test → build; secret scanning + dependency review.
- [ ] "Hello world" smoke e2e proving the stack starts.

### Docs
- [ ] Update `Current_Status.md`, `CHANGELOG.md`, and affected Bible "Current State"
  sections at the gate.

**Exit:** `docker compose up` → green health dashboard; CI green.

## Milestone 2 — Database & API (summary)
- Alembic + SQLAlchemy models (start with Projects/Tasks reference module) → all core
  entities (`05_Data/Data_Models.md`).
- FastAPI layered modules; Pydantic schemas; OpenAPI; generated TS client.
- Repository + unit-of-work; outbox table; seed data + factories; contract tests.

## Milestone 3 — Authentication (summary)
- Auth.js/JWT verification; optional Authentik OIDC; RBAC in the service layer; encrypted
  secret vault; audit-log middleware.

## Architecture Decisions
1. **No empty scaffolding** — every folder created in M1 contains real, working content.
2. **Reference module first** (Projects/Tasks) to set the pattern others copy.
3. **CI from day one** so quality gates exist before feature code.

## Alternatives Considered
Scaffolding all directories up front (empty) — rejected (violates the no-empty-folders
rule and the audit's guidance).

## Future Improvements
Convert these checklists into tracked issues (US-n / milestone labels) once `main` and
`.github/` templates exist.

## Implementation Notes
Work the M1 list top-to-bottom; keep PRs small and vertical. Update `Current_Status.md` as
items complete. Do not begin M2 until M1's exit criteria are accepted.
