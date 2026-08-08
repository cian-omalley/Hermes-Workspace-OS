# Hermes Workspace OS — AI Primer

> **Purpose:** a dense, front-loaded brief that lets any AI model "load" the whole project
> quickly. Facts first, short declarative lines, minimal prose. For depth, follow the
> pointers. Keep this in sync when the project changes (the Knowledge Curator agent owns
> it). **Last updated: 2026-08-08 (Milestones 0–4 complete; agent-department design +
> `.claude/` department tooling added).**

## 1. What it is (one paragraph)
Hermes Workspace OS is an open-source, self-hostable **AI Workspace Operating System** —
project management + documentation + repository intelligence + knowledge graph + research +
automation + AI agents in one modular platform. Its **own PostgreSQL database is the source
of record**; Notion, GitHub, and other tools are *replaceable interfaces*. The system must
keep working if any integration is disconnected.

## 2. Non-negotiable rules (memorize these)
1. **Hermes owns the data.** Postgres is authoritative; external tools are interfaces, never
   the source of record.
2. **Everything replaceable is a plugin** (AI, storage, search, integrations) behind a
   stable interface (ports & adapters).
3. **Derived stores are rebuildable projections** (Neo4j, Qdrant, Meilisearch) from Postgres
   + object storage. Never write authoritative data only to a derived store.
4. **Async by default**; event-driven via a transactional outbox; consumers are idempotent.
5. **Type-safe, tested, documented** — mypy strict + tsc strict; tests required; update docs
   (incl. Bible "Current State") in the same change.
6. **No empty files or folders.** Create structure only when it holds real content.
7. **Respect milestone gates**; don't build ahead without approval.
8. **The API contract seam is sacred:** the frontend uses the generated TypeScript client
   from OpenAPI — never hand-written API types; a CI drift check enforces it.
9. **Disconnect-safe:** turning any integration off must never break core CRUD (tested).

## 3. Architecture in 12 lines
- Modular **monolith-of-modules**: FastAPI gateway + bounded core modules; separate
  services for workers (Celery), agents (LangGraph `agentd`), scheduler.
- **Stores:** PostgreSQL (source of record), Redis (cache/broker/event bus), Neo4j
  (knowledge graph), Qdrant (vectors), Meilisearch (keyword), MinIO/Git (objects/code).
- **Layering per module:** router → service → repository; domain layer is
  framework-independent (`packages/hermes-domain`).
- **Unit of Work** owns the transaction; **repositories** hide persistence; a generic
  `CrudService` covers simple workspace-scoped entities.
- **Events:** domain write + event commit atomically (outbox); projections update search,
  graph, integrations, automation.
- **Retrieval:** hybrid keyword (Meili) + vector (Qdrant) fused by RRF, enriched by graph
  traversal (GraphRAG). **AI providers** (OpenAI/Anthropic/Gemini/Ollama) behind one port.
- **Agents:** ephemeral, tool-using LangGraph teams; least-privilege; no idle compute. Grouped
  into **departments** (Engineering + Knowledge & Operations) run by a **Harness** that
  checkpoints/resumes so one task can run for days; memory + DeepWiki + KG + docs hub compose a
  single **Knowledge & Memory Hub** (design: `docs/16-AGENT_DEPARTMENTS.md`; runtime = M9).

## 4. Tech stack
- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0 + Alembic, Celery.
- **Frontend:** Next.js/React/TypeScript, Tailwind, shadcn/ui, React Flow, Mermaid, ECharts.
- **AI/agents:** LangGraph, MCP, pluggable LLM providers. **Automation:** n8n.
- **Tooling:** uv + pnpm workspaces; ruff, mypy(strict), pytest; eslint, tsc(strict),
  vitest, Playwright; Docker Compose; GitHub Actions; `just`.

## 5. Delivery — 12 milestones (gated)
**Done:** M0 Docs & Project Bible · M1 Runnable skeleton + tooling + CI · M2 DB & CRUD API
for all core entities + generated TS client (drift-checked) · M3 Auth (JWT) + RBAC
(owner/admin/editor/viewer) + encrypted secret vault (Fernet) + audit log · M4 Notion
two-way sync (Projects/Tasks), idempotent + Hermes-wins conflicts, disconnect-safe.
**Next:** M5 GitHub integration. **Then:** M6 ingestion · M7 search · M8 knowledge graph ·
M9 agents · M10 dashboard · M11 automation · M12 deployment/hardening.

## 6. Current implemented state (code)
- `services/api` (FastAPI): auth, RBAC guards, workspaces/projects/tasks + users, documents,
  research, repositories, assets, agents, tags, members, secrets, Notion integration +
  webhook. Alembic migrations `0001`–`0004`.
- `services/worker` (Celery skeleton), `apps/web` (Next.js shell + health dashboard),
  `packages/hermes-domain` (domain events), `packages/ts-client` (generated client).
- Tests: SQLite-backed (portable models); ~81 Python + 6 web + 1 client passing.
- Not built yet: ingestion, search, graph, agents runtime, dashboard UI, automation; the
  web app does not yet consume the TS client (M10).

## 7. Core entities (data model)
Workspace → Project → Task; User + Membership (RBAC); Document, ResearchItem, Repository,
Asset, Agent; Tag/TagLink (polymorphic); Secret (encrypted), AuditLog; Integration,
SyncState, WebhookEvent, SyncLog. UUID PKs, `workspace_id` scoping, portable SQLAlchemy
types (SQLite in tests, Postgres in prod).

## 8. Key decisions & open questions
- **Open (see `docs/MISSING_INFORMATION.md`):** D1 embedding model, D5 default AI provider,
  D2 Neo4j edition, D7 chunking, D9 multi-tenancy isolation. (D10 create `main` = resolved.)
- **Resolved patterns:** REST+OpenAPI over GraphQL; audit within the unit of work (not
  middleware); portable DB types for CI; per-entity routers + a generic CRUD service.

## 9. Glossary (compact)
Source of record = authoritative store (Postgres). Interface/surface = replaceable
front-end. Derived store = rebuildable projection. Port/adapter = plugin interface/impl.
Integration = plugin syncing an external tool. Ingestion = file→knowledge pipeline.
GraphRAG = vector + graph retrieval. Agent = ephemeral tool-using LLM worker. Outbox =
table making write+event atomic. Disconnect-safe = core works with an integration off.

## 10. Where to go deeper
- Orientation: `docs/PROJECT_MAP.md`. Source of truth: `docs/PROJECT_BIBLE/` (start at its
  `README.md`). Live status: `docs/PROJECT_BIBLE/09_Implementation/Current_Status.md`.
- Claude Code rules: `docs/PROJECT_BIBLE/10_Claude_Code/`. Deep specs: `docs/00`–`16`.
- Agent departments: `docs/16-AGENT_DEPARTMENTS.md`; the real Claude Code department team +
  coordination protocol: `.claude/agents/` + `.claude/orchestration/README.md`.
- External reference stack: `docs/knowledge/sources/`.
