# Milestones

## Purpose
Provide the authoritative, at-a-glance milestone list with exit criteria — the checkpoints
that define "done" for each increment. Full detail: `docs/00-ROADMAP.md`.

## Current State
**M0 complete** (documentation). **M1 complete** (skeleton, tooling, CI). **M2 complete** —
layered CRUD API for all core entities with migrations, contract tests, and a generated TS
client. **M3 (Authentication) is next.** All others planned.

## Milestone table
| # | Name | Status | Exit criteria (definition of done) |
|---|------|--------|-----------------------------------|
| 0 | Engineering Foundation | ✅ | Docs + Project Bible + scaffolding reviewed/approved. |
| 1 | Project Foundation | ✅ | `docker compose up` → green health; CI passes. Skeleton + tests + CI done and verified. |
| 2 | Database & API | ✅ | Full CRUD for all core entities w/ tests; OpenAPI published; generated TS client (drift-checked in CI). |
| 3 | Authentication | ⏳ | Protected endpoints; RBAC tests; encrypted secret storage. |
| 4 | Notion Integration | ⏳ | Round-trip sync (Projects/Tasks); **disconnect test passes**. |
| 5 | GitHub Integration | ⏳ | Linked repo streams activity; issues↔tasks sync. |
| 6 | File Ingestion | ⏳ | Upload PDF → summary, tags, embeddings, relations, doc. |
| 7 | Search System | ⏳ | One query → fused, permission-scoped results across sources. |
| 8 | Knowledge Graph | ⏳ | Ingested content → navigable graph; GraphRAG answers. |
| 9 | AI Agents | ⏳ | Project creation spins up agent team on demand; artifacts produced. |
| 10 | Dashboard | ⏳ | E2E: create project → tasks → search → graph in the UI. |
| 11 | Automation | ⏳ | An event triggers a workflow that updates Hermes + Notion. |
| 12 | Deployment | ⏳ | One-command deploy; backup/restore verified; security review done. |

## Approval gates
At each milestone end: demo exit criteria, confirm CI green, update affected docs (incl.
Bible "Current State"), then **request approval before the next milestone.**

## Architecture Decisions
Exit criteria are **testable and user-observable**, not "code written" — every milestone is
validated by a demoable outcome.

## Alternatives Considered
Time-boxed milestones without exit criteria — rejected: "done" must be objective.

## Future Improvements
Attach concrete acceptance tests (US-n / W-n IDs) to each exit criterion as they're written;
track velocity once implementation begins.

## Implementation Notes
Keep this table and `CHANGELOG.md`'s milestone tracker in sync. `Current_Status.md` holds
the live per-system status; this file holds the milestone contract.
