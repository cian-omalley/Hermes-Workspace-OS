# External Services

## Purpose
Catalog the external/runtime services Hermes depends on or integrates with, their role,
and their failure behavior — so operators know what's required vs optional.

## Current State
Declared in the design; none provisioned yet. Split into **infrastructure services** (run
in the stack) and **external APIs** (third-party, pluggable).

## Infrastructure services (self-hosted, in compose)
| Service | Role | Required? | Failure behavior |
|---------|------|-----------|------------------|
| PostgreSQL | Source of record | **Required** | Core is down without it (hard dependency). |
| Redis | Cache, broker, event bus | **Required** | Async + caching degrade; core writes need the outbox relay. |
| MinIO | Object storage | Required for files | Uploads/ingestion fail; metadata safe. |
| Qdrant | Vectors | Optional-ish | Semantic search off; keyword still works. |
| Meilisearch | Keyword search | Optional-ish | Keyword off; semantic still works. |
| Neo4j | Knowledge graph | Optional-ish | Graph/GraphRAG off; vector+keyword search works. |
| n8n | Automation | Optional | Workflows unavailable; core unaffected. |

## External APIs (third-party, pluggable)
| Service | Role | Required? | Failure behavior |
|---------|------|-----------|------------------|
| OpenAI/Anthropic/Gemini | Hosted LLM/embeddings | Optional (if not using local) | AI features degrade; retry/backoff. |
| Ollama | Local LLM/embeddings | Optional | Local AI off; can fall back to hosted. |
| Notion API | Interface sync | Optional | Sync pauses/retries; core works (tested). |
| GitHub API | Repo integration | Optional | Repo sync pauses; existing data intact. |
| Authentik | OIDC SSO | Optional | Falls back to Auth.js. |

## Architecture Decisions
1. **Only Postgres (and Redis) are hard dependencies;** everything else degrades
   gracefully — consistent with the resilience goal.
2. **External APIs sit behind plugins** so they can be swapped or run locally (Ollama).
3. **A "lite" profile is proposed** (Decision Required, D-lite) to run a reduced store set
   for evaluation.

## Alternatives Considered
- **Managed cloud services** (RDS, Pinecone, Algolia) — valid but contradict self-host-
  first; supported *via plugins* but not the default.
- **Making all stores mandatory** — rejected; graceful degradation is a feature.

## Future Improvements
Health/status dashboard per dependency; automatic fallback (hosted↔local AI); a documented
minimal deployment; circuit breakers around external APIs.

## Implementation Notes
- Each provider adapter exposes `health()`; startup and `/health` aggregate them.
- Document required vs optional services in `.env.example` and the deployment guide.
- Respect third-party rate limits with token buckets + exponential backoff (all on the
  queue).
