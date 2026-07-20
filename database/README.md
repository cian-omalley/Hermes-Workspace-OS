# database

Schema management for the **PostgreSQL source of record**.

- `alembic.ini` — Alembic configuration (DB URL supplied at runtime via `DATABASE_URL`).
- `migrations/` — the migration environment and versioned migrations.
  - `env.py` targets the ORM metadata in `hermes_api.models`.
  - `versions/0001_initial_core_schema.py` — creates `workspaces`, `projects`, `tasks`.

## Commands
```bash
just migrate                       # upgrade to head (uses DATABASE_URL / .env)
alembic -c database/alembic.ini revision -m "add X"   # new migration
alembic -c database/alembic.ini downgrade -1          # roll back one
```

Every schema change ships as a reversible migration (see
`docs/PROJECT_BIBLE/05_Data/Migration_Strategy.md`). Derived stores (Neo4j/Qdrant/
Meilisearch) are bootstrapped separately from later milestones and are rebuildable from
this source of record.
