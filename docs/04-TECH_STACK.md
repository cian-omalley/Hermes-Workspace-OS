# 04 — Tech Stack

Every choice below is justified against three criteria: **maturity** (well-supported,
proven), **self-hostability** (runs on your own infra, permissive license), and **fit**
(right tool for the job). Because everything sits behind plugin interfaces (`06`), most
choices are swappable.

## 1. Frontend

| Tech | Why |
|------|-----|
| **Next.js (App Router)** | Production React framework; SSR/RSC for fast, SEO-able, data-rich dashboards; API routes for BFF/auth glue. |
| **React** | Ubiquitous, huge ecosystem, component model fits a modular UI. |
| **TypeScript** | End-to-end type safety; shared types with generated API client. |
| **TailwindCSS** | Utility-first styling; fast, consistent, themeable. |
| **shadcn/ui** | Accessible, unstyled-but-beautiful component primitives you own (not a black-box library). |
| **React Flow** | Interactive node graphs for knowledge graph, workflows, mind maps. |
| **Mermaid** | Text-to-diagram for architecture/flow docs; AI can emit it directly. |
| **Apache ECharts** | Rich, performant analytics/charts for dashboards. |
| **TanStack Query** | Server-state caching, mutations, and realtime invalidation. |

Client talks to the API via a **generated TypeScript client** from the OpenAPI schema,
so frontend and backend types never drift.

## 2. Backend

| Tech | Why |
|------|-----|
| **Python 3.12+** | First-class AI/ML ecosystem (LangGraph, extraction, embeddings). |
| **FastAPI** | Async, type-hinted, auto OpenAPI, Pydantic validation, great performance. |
| **Pydantic v2** | Rigorous request/response/domain schemas; fast validation. |
| **SQLAlchemy 2.0 + Alembic** | Mature ORM with typed core; reversible migrations. |
| **PostgreSQL** | Rock-solid relational source of record; JSONB, full-text, extensions. |
| **Redis** | Cache, Celery broker/result backend, Streams event bus, locks, rate limits. |
| **Celery** | Battle-tested distributed task queue for async ingestion/sync/analysis. |

**Why FastAPI over Django/Flask:** async-native (critical for I/O-bound AI/integration
work), automatic OpenAPI (drives the typed TS client), and Pydantic integration that
gives a single source of truth for schemas.

## 3. AI & Agents

| Tech | Why |
|------|-----|
| **LangGraph** | Graph-based agent orchestration: explicit state, cycles, checkpoints, human-in-the-loop — the right primitive for multi-agent teams. |
| **OpenHands concepts** | Patterns for autonomous developer agents (sandboxed tools, planning) informing our Developer/Review/Testing agents. |
| **MCP (Model Context Protocol)** | Standard tool/resource interface so agents can use external MCP servers and Hermes can expose its own tools. |
| **Provider APIs** | OpenAI, Anthropic, Google Gemini — best hosted models, behind one interface. |
| **Ollama** | Local/offline models for privacy and zero-cost inference. |

All model access goes through the **AI Provider plugin interface** (`06`) — chat,
embeddings, and (optionally) reranking — so any provider is swappable per workspace or
per agent, including mixing (e.g. local embeddings + hosted reasoning).

## 4. Knowledge, Search & Vectors

| Tech | Why |
|------|-----|
| **Neo4j** | Mature property-graph DB for the knowledge graph and GraphRAG traversal; Cypher is expressive for relationship queries. |
| **Qdrant** | Fast, self-hostable vector DB with payload filtering (permission-aware RAG) and hybrid search support. |
| **Meilisearch** | Instant, typo-tolerant keyword search; simple to self-host; great DX. |

**Why three stores, not one:** each excels at a different retrieval mode — relationships
(Neo4j), semantic similarity (Qdrant), and lexical/keyword (Meilisearch). The Search
module fuses them (`12`). All are rebuildable projections of the Postgres source of
record.

## 5. Storage

| Tech | Why |
|------|-----|
| **MinIO** | S3-compatible object storage, self-hostable, for files/images/videos/assets. |
| **Local filesystem** | Simple default for single-host dev; same interface as MinIO. |
| **Git** | Source-of-truth mirror for analyzed repositories (DeepWiki). |

Behind the **Storage Provider interface** (`06`), so MinIO can be swapped for real S3,
GCS, or local disk without code changes.

## 6. Automation

| Tech | Why |
|------|-----|
| **n8n** | Mature, self-hostable, fair-code visual automation with 400+ nodes; we add Hermes nodes and bridge domain events to it (`14`). |

## 7. Documentation

| Tech | Why |
|------|-----|
| **MkDocs Material** | Beautiful static docs sites generated per project. |
| **Markdown** | Universal, diff-friendly, AI-friendly source format for all docs. |
| **DeepWiki concepts** | Automatic repo documentation/architecture generation patterns (`09`). |

## 8. Authentication

| Tech | Why |
|------|-----|
| **Auth.js (NextAuth)** | Flexible web auth (OAuth, email, credentials) integrated with Next.js. |
| **Authentik** | Self-hostable OIDC/SAML identity provider for org SSO; optional. |

The API trusts a verified JWT/session; the identity provider is pluggable (Auth.js
credentials for solo, Authentik OIDC for teams).

## 9. Infrastructure & tooling

| Concern | Choice | Why |
|---------|--------|-----|
| **Packaging/runtime** | Docker + Docker Compose | One-command self-host of the full stack. |
| **Python deps** | `uv` + `pyproject.toml` | Fast, reproducible, modern. |
| **JS deps** | `pnpm` workspaces | Efficient monorepo package management. |
| **Lint/format (py)** | `ruff` | Fast, all-in-one lint+format. |
| **Types (py)** | `mypy` (strict) | Enforced static typing. |
| **Tests (py)** | `pytest` + `httpx` | Unit/integration/contract tests. |
| **Lint (ts)** | `eslint` + `prettier` | Consistency. |
| **Types (ts)** | `tsc` strict | Type safety. |
| **Tests (ts)** | `vitest` + Playwright | Unit + e2e. |
| **CI** | GitHub Actions | Lint, type-check, test, build on every PR. |
| **Task runner** | `just` (Justfile) | Discoverable dev commands. |
| **Observability** | OpenTelemetry, Prometheus, structured logs | Standard, vendor-neutral (M12). |

## 10. Monorepo layout (planned, from M1)

```
hermes-workspace-os/
├── apps/
│   └── web/                 # Next.js dashboard
├── services/
│   ├── api/                 # FastAPI gateway + core modules
│   ├── worker/              # Celery workers (ingestion, sync, indexing)
│   ├── agentd/              # LangGraph agent runtime
│   └── scheduler/           # Celery beat
├── packages/
│   ├── hermes-domain/       # entities, value objects, domain events
│   ├── hermes-core/         # services, repositories, plugin registry
│   ├── hermes-plugins/      # provider interfaces + built-in adapters
│   └── ts-client/           # generated TS API client + shared types
├── infra/
│   ├── docker/              # Dockerfiles
│   ├── compose/             # docker-compose stacks
│   └── helm/                # optional chart (M12)
├── docs/                    # this documentation
└── tests/                   # cross-service e2e
```

## 11. Language & boundary rationale

- **Python for the backend/AI plane**: the AI, extraction, and agent ecosystems are
  Python-first; keeping ingestion, agents, and API in one language avoids a second
  runtime and lets them share the domain packages.
- **TypeScript for the frontend**: best-in-class UI ecosystem; type-shared with the
  backend via generated client.
- **Two languages, one contract**: the OpenAPI schema is the seam. No hand-written,
  drift-prone client code.

## 12. Licensing posture

All core dependencies are permissively or fair-code licensed and self-hostable
(Postgres/Redis/Neo4j Community/Qdrant/Meilisearch/MinIO/n8n/Ollama). Hermes itself is
**Apache-2.0**. Where a dependency's license has conditions (e.g. n8n's fair-code,
Neo4j Community/Enterprise split), the plugin interface allows substitution.
