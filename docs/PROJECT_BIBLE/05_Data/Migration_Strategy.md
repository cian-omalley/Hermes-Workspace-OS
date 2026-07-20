# Migration Strategy

## Purpose
Define how schema and data evolve safely over the life of the project across all data
stores.

## Current State
No migrations exist yet (M2 introduces the first). This strategy governs them from the
start.

## Relational (PostgreSQL) — Alembic
- **Every schema change is a reversible Alembic migration**, reviewed in CI.
- **Forward + backward:** each migration provides `upgrade()` and `downgrade()`.
- **Additive-first:** prefer add-then-migrate-then-remove over destructive changes; expand/
  contract pattern for column/table renames to avoid downtime.
- **Data migrations** are explicit, idempotent, and batched for large tables.
- **No manual DB edits** — the migration history is the single source of schema truth.

## Derived stores (Neo4j / Qdrant / Meilisearch)
- **Idempotent bootstrap scripts** create constraints/indexes/collections, versioned in
  `database/`.
- **Rebuildable:** because these are projections, most "migrations" are handled by a
  `reindex`/`rebuild-graph` job that regenerates them from Postgres + MinIO.
- **Embedding model changes** trigger a re-embed job (tracked via `embedding_refs.model`).

## Object storage (MinIO)
- Bucket/layout changes handled by migration scripts + content-addressed keys (rarely
  need to move objects).

## Architecture Decisions
1. **Alembic as the relational migration authority** — mature, integrates with SQLAlchemy.
2. **Expand/contract for zero-downtime** schema evolution.
3. **Rebuild over migrate for derived stores** — simpler and leverages the source-of-record
   design.

## Alternatives Considered
- **Auto-generated schema sync (no versioned migrations)** — rejected: unsafe, unauditable.
- **Hand-written SQL migrations** — Alembic chosen for reversibility and ORM alignment.
- **In-place migration of vector/graph stores** — unnecessary given rebuildability.

## Future Improvements
Migration testing in CI (apply up/down on a scratch DB), seed/fixture management, blue-green
or online migration tooling for large tables, and automated backup-before-migrate in
production.

## Implementation Notes
- Name migrations descriptively; one logical change per migration.
- Run migrations as a deploy step (`just migrate`), gated in CI.
- For destructive changes, ship in two releases (deprecate → remove) with data backfill in
  between.
- Always back up before production migrations (M12 runbook).
