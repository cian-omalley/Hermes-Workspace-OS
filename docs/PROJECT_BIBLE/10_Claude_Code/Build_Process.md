# Claude Code — Build Process

## Purpose
Describe how to build, run, test, and verify Hermes so any session can reproduce a working
environment and validate changes. Complements `08_Development/Deployment.md` and `DevOps.md`.

## Current State
**No build system exists yet** — there is no code, `docker-compose.yml`, `pyproject.toml`,
or `package.json`. The commands below are the **target** from Milestone 1; until then there
is nothing to build or run. Do not claim a build/test ran when the tooling doesn't exist.

## Target local workflow (from Milestone 1)
```bash
# 1. Configure
cp config/.env.example .env        # set provider keys / options

# 2. Bring up the stack
docker compose -f infrastructure/compose/docker-compose.yml up -d
                                    # Postgres, Redis, Neo4j, Qdrant, Meili, MinIO, services

# 3. Migrate + seed
just migrate                        # Alembic
just seed                           # dev fixtures (optional)

# 4. Run services (dev)
just api                            # FastAPI (uvicorn)
just worker                         # Celery
pnpm --filter web dev               # Next.js

# 5. Quality gates
just check                          # ruff + mypy + eslint + tsc
just test                           # unit + integration
just e2e                            # Playwright (headline workflows)
```

## Build pipeline (target)
1. Python packages built with `uv` from `pyproject.toml`; services share `packages/hermes-*`.
2. Frontend built with `pnpm` workspaces (Next.js build).
3. **OpenAPI schema generated from FastAPI → TS client generated** into `packages/ts-client`
   (the contract seam; CI verifies it's in sync).
4. Docker images built per service (`infrastructure/docker/*`).
5. CI (GitHub Actions): lint → type-check → test → build on every PR.

## Verifying a change
- Run the relevant tests + `just check` locally.
- For behavior changes, exercise the affected flow end-to-end (not just unit tests).
- Update docs/Bible; ensure CI is green before requesting merge.

## Architecture Decisions
1. **One task runner (`just`)** exposes a discoverable, consistent command surface.
2. **Compose-first local dev** mirrors the self-host deployment target.
3. **Contract generation in the build** prevents frontend/backend drift.

## Alternatives Considered
- **Per-service ad-hoc scripts** — rejected in favor of a unified `just` interface.
- **Manual client maintenance** — rejected; generation is part of the build.

## Future Improvements
Dev containers, hot-reload across services, a `compose` "lite" profile, and cached CI
builds for speed.

## Implementation Notes
- Establish these commands in Milestone 1 so every later session has a stable build/test
  loop.
- Until M1 exists, there is nothing to run — say so plainly rather than inventing output.
- Keep this file updated as the real build system lands (replace "target" with "actual").
