# Deployment

## Purpose
Define how Hermes is packaged and deployed, with self-hosting as the first-class target.

## Current State
Designed; unimplemented. No `docker-compose.yml`, Dockerfiles, or Helm chart exist yet
(M1 introduces the dev compose stack; M12 hardens production).

## Topologies
### Single-host (default, self-host)
One `docker compose up` brings up: web, api, worker, agentd, scheduler, n8n, and all
datastores (Postgres, Redis, Neo4j, Qdrant, Meilisearch, MinIO). Suitable for individuals
and small teams.

### Scale-out (later)
api/worker/agentd scale horizontally; datastores externalized to managed/replicated
instances; optional **Helm chart** (M12).

## Configuration
- **12-factor env vars;** `.env.example` is the authoritative config/secret list (ships M1).
- **Provider selection** via the plugin registry (AI/storage/search/graph/integrations).
- **Secrets** from the encrypted vault; never baked into images.

## Build & release
- Per-service Docker images built from `infrastructure/docker/*`.
- CI builds and tests images; tagged releases produce versioned images.
- Migrations run as a deploy step (`just migrate`).

## Architecture Decisions
1. **Compose-first** — lowest-friction path to a full self-hosted stack.
2. **Config over code** — deployments differ by env/plugins, not forks.
3. **Reduced "lite" profile proposed** (Decision Required) so evaluators can run fewer
   stores.

## Alternatives Considered
- **Kubernetes-first** — rejected as the default: too heavy for self-hosters; offered later
  via Helm.
- **Single mega-container** — rejected: poor scaling/failure isolation.
- **PaaS-specific packaging** — avoided to prevent lock-in (self-host-first).

## Future Improvements
Helm chart, one-click deploy templates, health/status dashboard, blue-green deploys, and a
documented minimal footprint.

## Implementation Notes
- M1: dev compose + health checks + `.env.example`.
- M12: production compose profile, backups (Postgres/Neo4j/Qdrant/MinIO), restore runbook,
  observability (logs/metrics/traces), rate limiting, secret rotation, upgrade guide.
- Document required vs optional services (`04_Integrations/External_Services.md`).
