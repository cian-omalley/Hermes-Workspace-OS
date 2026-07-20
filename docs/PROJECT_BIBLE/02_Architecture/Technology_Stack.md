# Technology Stack

## Purpose
Record every technology choice and its justification so the stack is intentional and
defensible. Canonical deep spec: `docs/04-TECH_STACK.md`.

## Current State
Choices are **decisions, not installations** — no `pyproject.toml`, `package.json`, or
lockfiles exist yet. Dependencies land in Milestone 1.

## The stack (by layer)
| Layer | Choice | One-line justification |
|-------|--------|------------------------|
| Frontend | Next.js, React, TypeScript, Tailwind, shadcn/ui | Mature, type-safe, data-rich SSR/RSC UI. |
| Visualization | React Flow, Mermaid, ECharts | Graphs, diagrams, analytics. |
| Frontend state | TanStack Query | Server-state caching + realtime invalidation. |
| Backend | Python 3.12+, FastAPI, Pydantic v2 | Async, type-hinted, auto-OpenAPI, AI ecosystem. |
| ORM/migrations | SQLAlchemy 2.0, Alembic | Typed ORM, reversible migrations. |
| Queue | Celery + Redis | Battle-tested async jobs. |
| Source of record | PostgreSQL | Reliable relational store; JSONB, FTS. |
| Cache/bus | Redis (+ Streams) | Cache, broker, event bus, locks. |
| Graph | Neo4j | Property graph for KG + GraphRAG. |
| Vectors | Qdrant | Self-hostable vector DB with payload filtering. |
| Keyword | Meilisearch | Instant, typo-tolerant full-text. |
| Objects | MinIO (+ local FS, Git) | S3-compatible self-hostable storage. |
| Agents | LangGraph (+ MCP) | Stateful graph orchestration; standard tools. |
| AI providers | OpenAI/Anthropic/Gemini/Ollama | Pluggable; hosted + local. |
| Automation | n8n | Mature self-hostable visual automation. |
| Docs | MkDocs Material, Markdown | Beautiful static docs; diff-friendly source. |
| Auth | Auth.js, Authentik (OIDC) | Web auth + optional self-hosted SSO. |
| Tooling | uv, pnpm, ruff, mypy, pytest, eslint, tsc, vitest, Playwright, Docker, GitHub Actions, just | Fast, reproducible, type-safe, tested. |

## Architecture Decisions
1. **Two languages, one contract.** Python (backend/AI) + TypeScript (frontend), joined by
   the OpenAPI→TS client seam.
2. **Four data planes** because relational, graph, vector, and keyword retrieval are
   genuinely different problems; all derived stores are rebuildable from Postgres.
3. **Everything swappable via plugins** (`docs/06`) — the stack is a set of defaults, not a
   cage.
4. **Self-host-first, permissive licensing** throughout (`docs/04 §12`).

## Alternatives Considered
- **Django/Flask** vs FastAPI — FastAPI chosen for async + auto-OpenAPI + Pydantic.
- **pgvector** vs Qdrant — Qdrant chosen for scale, filtering, and hybrid features;
  pgvector remains a possible plugin for lean deployments (**Decision Required** to offer a
  "lite" profile — see `docs/MISSING_INFORMATION.md`).
- **Elasticsearch** vs Meilisearch — Meilisearch for DX and light footprint.
- **Temporal/Prefect** vs Celery — Celery for simplicity now; revisit for complex
  orchestration.

## Future Improvements
Offer a reduced-store "lite" compose profile; evaluate pgvector-only mode; consider
Turborepo/Nx if build times grow (D8); add a hosted-model gateway for cost control.

## Implementation Notes
- Pin versions and commit lockfiles in Milestone 1; enable dependency + secret scanning.
- Record the resolved provider/model defaults in `.env.example` (D1, D5).
- Keep license-sensitive components (Neo4j edition, n8n fair-code) behind plugin seams.
