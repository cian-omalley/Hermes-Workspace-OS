# CLAUDE.md — Entry point for Claude Code

This file orients any Claude Code session (or human) working in this repository. **Read
this first, then the Project Bible.**

## What this project is

**Hermes Workspace OS** — an open-source, self-hostable AI Workspace Operating System.
Its **own PostgreSQL database is the source of record**; Notion, GitHub, and other tools
are *replaceable interfaces*. The system must keep working if any integration is
disconnected.

## Current stage (read carefully)

Milestones 0–4 are complete. **Milestone 5 — GitHub Integration is next.** M2 delivered the
full CRUD API + **generated TypeScript client** (`packages/ts-client`, drift-checked in CI).
M3 added **auth & RBAC** (JWT, owner/admin/editor/viewer membership guards, encrypted secret
vault, audit logging). M4 added the **Notion integration**: a `NotionClient` abstraction
(in-memory fake for tests, real HTTP client for production), a declarative entity↔Notion
mapping (Projects/Tasks), and a two-way sync engine that is idempotent and conflict-aware
(**Hermes wins**), with the headline **disconnect-safe** guarantee tested. The Next.js
Auth.js **login UI** is deferred to the M10 dashboard. See
`docs/PROJECT_BIBLE/09_Implementation/Current_Status.md` for the live status.

## Required reading order

1. `CLAUDE.md` (this file)
2. **`docs/knowledge/AI_PRIMER.md`** — the condensed, memorizable brief of the whole project
   (fastest way to "load" Hermes)
3. `docs/PROJECT_BIBLE/10_Claude_Code/Instructions.md` — **how you must operate here**
4. `docs/PROJECT_BIBLE/README.md` — the Bible index
5. `docs/PROJECT_MAP.md` — fast orientation
6. `docs/AUDIT_REPORT.md` and `docs/MISSING_INFORMATION.md` — state & open decisions
7. The numbered specs `docs/00-ROADMAP.md` … `docs/15-UI_DESIGN.md` as needed

The **Knowledge Hub** (`docs/knowledge/`) is the single front door that indexes every
document in the repo (`docs/knowledge/README.md`).

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
- **Curate incoming knowledge.** Every new file, link, or note is sorted into the Knowledge
  Hub and rewritten into the AI-friendly format — see `docs/knowledge/CURATION_RULES.md`.
  The dedicated **`knowledge-curator`** agent (`.claude/agents/knowledge-curator.md`) does
  this; invoke it when source material arrives. Keep `docs/knowledge/AI_PRIMER.md` current.
- **Work as a team of departments.** A roster of Claude Code subagents in `.claude/agents/` is
  organized into **Engineering** (product-manager, researcher, engineer, code-reviewer,
  qa-tester, release-manager) and **Knowledge & Operations** (orchestrator, knowledge-curator,
  deepwiki-brain, memory-keeper). For a large or long-running task, follow the coordination
  protocol in `.claude/orchestration/README.md`: plan via `orchestrator`/`product-manager`,
  route steps to the owning agent, and checkpoint state to `.claude/orchestration/blackboard.md`
  so the task can resume across sessions. Design: `docs/16-AGENT_DEPARTMENTS.md`.

## Where to put things (once code exists)

See `docs/PROJECT_MAP.md §3` for the intended monorepo layout (`apps/`, `services/`,
`packages/`, `database/`, `infrastructure/`, `config/`, `scripts/`, `tests/`). Create
these directories only when adding real code to them.

## Full development rules

`docs/PROJECT_BIBLE/10_Claude_Code/` — `Instructions.md`, `Architecture_Rules.md`,
`Coding_Rules.md`, `Build_Process.md`.
