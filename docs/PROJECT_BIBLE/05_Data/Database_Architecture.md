# Database Architecture

## Purpose
Describe Hermes' multi-store data architecture and how the stores stay consistent.
Canonical spec: `docs/05-DATABASE_DESIGN.md`.

## Current State
Designed; unimplemented (M2). No migrations or collections exist yet.

## Four data planes
| Plane | Store | Role | Authority |
|-------|-------|------|-----------|
| Relational | **PostgreSQL** | Domain data, sync state, audit, outbox | **Source of record** |
| Graph | **Neo4j** | Entities/relationships, GraphRAG | Derived |
| Vector | **Qdrant** | Embeddings for semantic search/RAG | Derived |
| Keyword | **Meilisearch** | Full-text index | Derived |
| Objects | **MinIO** | File/image/video bytes | Bytes (metadata in PG) |

**Rule:** never write authoritative data only to a derived store. All derived stores are
rebuildable from Postgres + MinIO via `reindex`/`rebuild-graph`.

## Consistency mechanisms
- **Transactional outbox:** domain write + event commit atomically; a relay publishes to
  the bus so projections never miss updates.
- **Bridge tables:** `embedding_refs`, `graph_refs`, `relationships` map derived records
  back to Postgres for rebuild, delete, and consistency.
- **Idempotent consumers + reconciliation** catch retries and drift.

## Conventions
UUID PKs (`pgcrypto`), UTC timestamps + soft delete where relevant, `workspace_id` on
nearly every table (optional RLS, D9), `metadata jsonb` for forward-compat, Postgres enums
for stable vocabularies, GIN/tsvector/partial indexes on hot paths.

## Architecture Decisions
1. **Polyglot persistence** — each retrieval mode gets the right engine; consistency is
   managed by making Postgres authoritative and everything else rebuildable.
2. **Outbox over dual-write** for reliable eventing.
3. **Polymorphic tag/embedding/graph links** (`(entity_type, entity_id)`) avoid per-table
   sprawl.

## Alternatives Considered
- **Single Postgres (with pgvector + recursive CTEs + FTS)** — simpler ops, viable for a
  "lite" mode; rejected as the default because graph traversal and vector scale suffer.
  Kept as a possible plugin profile (**Decision Required**, D-lite).
- **Event sourcing as the primary model** — rejected: too much complexity; the outbox gives
  reliable events without full ES.

## Future Improvements
Read replicas, partitioning of high-volume tables (audit, embeddings refs), CDC as an
outbox alternative at scale, and a documented "lite" single-store profile.

## Implementation Notes
- All schema changes via Alembic (reversible, CI-reviewed); Neo4j/Qdrant/Meili setup as
  idempotent bootstrap scripts.
- Deletes cascade to derived stores via bridge tables + Meili ids.
- Back up all planes on a schedule with a tested restore runbook (M12).
