# Development Phases

## Purpose
Group the 12 milestones into coherent development phases with goals, tasks, dependencies,
and expected results — the strategic build plan. Pairs with `docs/00-ROADMAP.md` (milestone
detail) and `Milestones.md`.

## Current State
**Phase 1's predecessor (Milestone 0 — documentation) is complete.** No phase's code exists
yet. Phases proceed with an approval gate between milestones.

---

## Phase 1 — Foundation (Milestone 1)
- **Goals:** Runnable monorepo skeleton; tooling; local stack; CI.
- **Tasks:** monorepo layout; `docker-compose.yml` (Postgres/Redis/Neo4j/Qdrant/Meili/
  MinIO); ruff/mypy/pytest + eslint/tsc/vitest; GitHub Actions; `.env.example`;
  `just`/Makefile; health checks; smoke e2e.
- **Dependencies:** none (starts from the documented design).
- **Expected result:** `docker compose up` → green health; CI passes.

## Phase 2 — Core Architecture (Milestones 2–3)
- **Goals:** The domain model + API behind secure auth — Hermes as source of record.
- **Tasks (M2):** SQLAlchemy models + Alembic; FastAPI layered modules; Pydantic schemas +
  OpenAPI; repository/unit-of-work; seed/factories; contract tests. **(M3):** Auth.js/JWT +
  optional Authentik; RBAC; encrypted secret vault; audit log.
- **Dependencies:** Phase 1.
- **Expected result:** Full CRUD for core entities, authenticated + authorized; OpenAPI +
  generated TS client published.

## Phase 3 — Main Features (Milestones 4–6)
- **Goals:** Interfaces + content pipeline.
- **Tasks:** Notion two-way sync (M4, disconnect-safe); GitHub sync + analysis (M5); file
  ingestion pipeline + extractors (M6).
- **Dependencies:** Phase 2.
- **Expected result:** Work syncs with Notion/GitHub; uploads become structured knowledge;
  W5 resilience test passes.

## Phase 4 — Integrations & Retrieval (Milestones 7–8)
- **Goals:** Make everything findable and connected.
- **Tasks:** hybrid search (M7, Meili+Qdrant, RRF, permission-aware); knowledge graph +
  GraphRAG (M8, Neo4j, extraction, rebuildable).
- **Dependencies:** Phase 3 (ingestion produces the content).
- **Expected result:** One query searches all sources; GraphRAG answers with citations.

## Phase 5 — AI Features (Milestone 9)
- **Goals:** Autonomous, ephemeral agent teams that do real work.
- **Tasks:** LangGraph agent framework; lifecycle/memory/permissions/tools/comms; default
  team templates; tool registry (search/KG/GitHub/files/Notion); artifacts; eval harness.
- **Dependencies:** Phases 3–4 (agents rely on retrieval + GraphRAG + integrations).
- **Expected result:** A goal spins up an agent team on demand; agents produce artifacts and
  update tasks; no idle compute.

## Phase 6 — Experience & Automation (Milestones 10–11)
- **Goals:** The unified UI + event-driven automation.
- **Tasks:** Next.js dashboard + project workspace + visualizations (M10); n8n bridge +
  Hermes nodes + native triggers + templates (M11).
- **Dependencies:** Phases 2–5 (UI surfaces working systems; automation acts on them).
- **Expected result:** End-to-end workspace UI; events trigger workflows that update
  Hermes/Notion.

## Phase 7 — Production Release (Milestone 12)
- **Goals:** Production-ready self-hosting.
- **Tasks:** production compose + optional Helm; backups/restore; observability (logs/
  metrics/traces); security review; rate limiting; secret rotation; upgrade guide.
- **Dependencies:** Phases 1–6.
- **Expected result:** Documented one-command deploy; verified backup/restore; security
  review complete.

---

## Architecture Decisions
1. **Phases are dependency-ordered vertical slices** — each yields something runnable and
   testable, not a horizontal layer.
2. **Approval gate between milestones** — no building ahead without acceptance.
3. **Data before features; retrieval before agents; everything before the dashboard.**

## Alternatives Considered
- **UI-first or big-bang** — rejected (see `01_Product/Roadmap.md`): rework and unmanageable
  scope.

## Future Improvements
Post-Phase-7: plugin marketplace, team/enterprise features, mobile, federation, domain
packs — sequenced by adoption feedback.

## Implementation Notes
Each phase updates `Current_Status.md`, `CHANGELOG.md`, and the relevant Bible "Current
State" sections at its gate. See `Task_Breakdown.md` for the near-term (M1) task list.
