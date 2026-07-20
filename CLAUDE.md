# CLAUDE.md — Entry point for Claude Code

This file orients any Claude Code session (or human) working in this repository. **Read
this first, then the Project Bible.**

## What this project is

**Hermes Workspace OS** — an open-source, self-hostable AI Workspace Operating System.
Its **own PostgreSQL database is the source of record**; Notion, GitHub, and other tools
are *replaceable interfaces*. The system must keep working if any integration is
disconnected.

## Current stage (read carefully)

The repository is in **Milestone 2 — Database & API (in progress)**. Milestones 0
(documentation) and 1 (runnable skeleton + tooling + CI) are complete. M2 has added the
core domain model and a full layered CRUD API for the **Workspace → Project → Task**
hierarchy (SQLAlchemy models, Alembic migrations, Pydantic schemas, repository + unit-of-
work, service layer, FastAPI routers under `/api/v1`, OpenAPI + contract tests). Remaining
core entities (Document, Repository, Asset, Agent, …) and **authentication (M3)** are not
built yet — the API is currently unauthenticated. See
`docs/PROJECT_BIBLE/09_Implementation/Current_Status.md` for the live status.

## Required reading order

1. `CLAUDE.md` (this file)
2. `docs/PROJECT_BIBLE/10_Claude_Code/Instructions.md` — **how you must operate here**
3. `docs/PROJECT_BIBLE/README.md` — the Bible index
4. `docs/PROJECT_MAP.md` — fast orientation
5. `docs/AUDIT_REPORT.md` and `docs/MISSING_INFORMATION.md` — state & open decisions
6. The numbered specs `docs/00-ROADMAP.md` … `docs/15-UI_DESIGN.md` as needed

## Non-negotiable rules (summary — full text in the Bible)

- **Read the Project Bible before coding.** Understand existing architecture first.
- **Preserve working functionality.** Prefer improving existing systems over rewrites.
- **Prefer mature open-source solutions** over rebuilding them.
- **Hermes owns the data.** Never make an external tool the source of record.
- **Everything replaceable is a plugin** (AI, storage, search, integrations).
- **Type safety, tests, and docs are required**, not optional.
- **No empty files or folders.** Create structure only when it holds real content.
- **Before major changes,** explain what will change, why, alternatives, and risks.
- **Update the Bible's "Current State"** whenever you implement or change a system.
- **Respect the milestone gates.** Do not build ahead without approval.

## Where to put things (once code exists)

See `docs/PROJECT_MAP.md §3` for the intended monorepo layout (`apps/`, `services/`,
`packages/`, `database/`, `infrastructure/`, `config/`, `scripts/`, `tests/`). Create
these directories only when adding real code to them.

## Full development rules

`docs/PROJECT_BIBLE/10_Claude_Code/` — `Instructions.md`, `Architecture_Rules.md`,
`Coding_Rules.md`, `Build_Process.md`.
