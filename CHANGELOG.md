# Changelog

All notable changes to Hermes Workspace OS are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Until the
first release, changes are tracked under **Unreleased** and grouped by milestone.

## [Unreleased]

### Added — Milestone 2: remaining entities + TypeScript client (2026-07-20)
- **Remaining core entities** with full CRUD, following the reference pattern: `User`
  (top-level), and workspace-scoped `Document`, `ResearchItem`, `Repository`, `Asset`,
  `Agent`, plus `Tag`/`TagLink` (with attach/detach). A generic `CrudService` base and a
  `WorkspaceScopedMixin` keep the five content entities DRY.
- **Alembic migration `0002`** (up/down verified) creating the new tables.
- **Generated TypeScript client** (`packages/ts-client`): `openapi.json` + `schema.d.ts`
  generated from the API (`openapi-typescript`), a typed `openapi-fetch` wrapper, and a **CI
  drift check** that fails if the committed client diverges from the API. `just gen-client`
  regenerates both. Committed `uv.lock` for reproducible generation.
- **Verified locally:** 55 Python tests + 6 web tests + 1 client test pass; ruff, mypy
  strict, tsc, eslint clean; migrations up/down; client regeneration is deterministic.

### Added — Milestone 2: Database & API foundation (2026-07-20)
- **Domain model & layered CRUD API** for the core hierarchy Workspace → Project → Task:
  - SQLAlchemy 2.0 models with portable types (SQLite for tests/CI, PostgreSQL in prod).
  - Pydantic schemas, repository layer, unit-of-work, service layer, and thin FastAPI
    routers under `/api/v1` (full create/read/update/delete/list).
  - Alembic migrations in `database/` (`0001_initial_core_schema`, up/down verified);
    `just migrate` / `just makemigration` / `just seed`; example seed script.
  - OpenAPI schema published; contract tests assert the API surface.
- **Verified locally:** 30 Python tests pass; ruff, mypy strict clean; Alembic upgrade/
  downgrade works; end-to-end workspace→project→task CRUD confirmed.
- Docs updated (Current_Status, Milestones, Data_Models) per the docs-with-code rule.

### Fixed — CI pipeline (2026-07-20)
- Python job: declared ruff/mypy/pytest in a root dev group and switched to
  `uv sync --all-packages --all-extras` so workspace members' deps install.
- Web job: removed the duplicate pnpm version (kept `packageManager` as the source).

### Added — Milestone 1: Project Foundation (2026-07-20)
- **Monorepo skeleton** with real, tested content (no empty folders):
  - `services/api` — FastAPI app factory + `/health` + settings (3 tests).
  - `services/worker` — Celery app + `ping` health task (3 tests).
  - `apps/web` — Next.js App Router shell, landing page as a stack-health dashboard,
    `/health` route, health helpers (6 tests).
  - `packages/hermes-domain` — framework-independent domain events (4 tests).
- **Local stack:** `infrastructure/compose/docker-compose.yml` (Postgres, Redis, Neo4j,
  Qdrant, Meilisearch, MinIO + api/web/worker) with health checks; per-service Dockerfiles.
- **Tooling:** uv workspace + ruff + mypy(strict) + pytest; pnpm workspace + eslint +
  tsc(strict) + vitest; `justfile`; `config/.env.example`.
- **CI:** GitHub Actions (Python + web lint/types/tests, secret scanning) and `.github/`
  PR/issue templates + CODEOWNERS.
- **`main` base branch established** (resolves decision D10).
- **Verified locally:** 10 Python tests + 6 web tests pass; ruff, mypy strict, tsc, eslint
  clean; Next.js production build succeeds.

### Added — Repository Intelligence & Documentation Pass (2026-07-20)
- `CLAUDE.md` — entry point and operating rules pointer for Claude Code sessions.
- `CONTRIBUTING.md` — contribution guidelines.
- `CHANGELOG.md` — this file.
- `docs/AUDIT_REPORT.md` — full repository audit of commit `ff45a54`.
- `docs/PROJECT_MAP.md` — single-page orientation to the repo and system.
- `docs/MISSING_INFORMATION.md` — consolidated open decisions, gaps, and risks.
- `docs/PROJECT_BIBLE/` — complete Claude Code Project Bible (11 sections, 50+ documents)
  as the permanent source of truth: Overview, Product, Architecture, Core Systems,
  Integrations, Data, AI, Interface, Development, Implementation, and Claude Code rules.

### Notes
- **Non-destructive pass:** no files were deleted or moved — the existing tree contained
  no empty, duplicate, or deprecated files. Intended code directories were intentionally
  **not** scaffolded (to honor the "no empty folders" rule); they are documented in
  `docs/PROJECT_MAP.md` and created when real code lands.

### Added — Milestone 0: Engineering Foundation (commit `ff45a54`)
- 16 design specifications in `docs/` (`00-ROADMAP` … `15-UI_DESIGN`).
- `README.md`, Apache-2.0 `LICENSE`, `.gitignore`.
- Core architectural decision documented: Hermes' database is the source of record;
  Notion/GitHub are replaceable interfaces.

---

## Milestone tracking

| Milestone | Status | Summary |
|-----------|--------|---------|
| M0 — Engineering Foundation | ✅ Complete | Design docs + Project Bible + repo scaffolding |
| M1 — Project Foundation | ✅ Complete | Monorepo, tooling, compose stack, CI |
| M2 — Database & API | ✅ Complete | Domain model + FastAPI CRUD (all core entities) + generated TS client |
| M3 — Authentication | ⏳ Planned | Auth, RBAC, secrets, audit |
| M4 — Notion Integration | ⏳ Planned | Two-way sync; disconnect-safe |
| M5 — GitHub Integration | ⏳ Planned | Repo/commit/PR/issue sync |
| M6 — File Ingestion | ⏳ Planned | Automatic processing pipeline |
| M7 — Search System | ⏳ Planned | Hybrid semantic + keyword |
| M8 — Knowledge Graph | ⏳ Planned | Entities, relationships, GraphRAG |
| M9 — AI Agents | ⏳ Planned | LangGraph agent orchestration |
| M10 — Dashboard | ⏳ Planned | Web workspace |
| M11 — Automation | ⏳ Planned | n8n workflows |
| M12 — Deployment | ⏳ Planned | Production hardening |
