# Claude Code — Architecture Rules

## Purpose
The architectural guardrails any change must respect. These make the system's key
properties non-negotiable regardless of who (or what) is coding.

## Current State
Rules defined against the documented architecture; enforced by review now and by automated
checks once code + CI exist.

## The rules
1. **Hermes owns the data.** PostgreSQL is the source of record. Never make Notion, GitHub,
   or any external tool authoritative. External tools sync to/from Postgres.
2. **Derived stores are rebuildable projections.** Never write authoritative data only to
   Neo4j/Qdrant/Meilisearch. Maintain the bridge tables (`embedding_refs`, `graph_refs`,
   `relationships`) so `reindex`/`rebuild-graph` always works.
3. **Ports & adapters everywhere replaceable.** AI, storage, search, graph, and integrations
   go behind plugin interfaces. No provider SDK is imported directly into core business
   logic.
4. **Clean layering.** router → service → repository; the domain layer is framework- and
   I/O-independent. Modules never import another module's repositories — call services or
   react to events.
5. **Event-driven with a transactional outbox.** Domain write + event emission commit
   atomically; consumers are idempotent (dedupe on event id).
6. **The API contract seam is sacred.** The frontend uses the generated TS client from the
   OpenAPI schema — never hand-written API types. Keep them in sync in CI.
7. **Async by default.** Slow work (ingestion, sync, agents, analysis) runs on the queue,
   not in the request path.
8. **Least privilege.** Agents and workflows run with explicit, scoped permissions; mutating/
   external actions may require approval; code execution is sandboxed.
9. **Graceful degradation.** If a derived store or integration is down, core CRUD still
   succeeds and affected work re-queues. Disconnecting Notion must never break the core.
10. **Multi-tenant safety.** Everything is `workspace_id`-scoped; search/RAG are ACL-filtered
    at the index and re-checked after fusion.

## Architecture Decisions
These rules encode the decisions in `02_Architecture/*` and `docs/03`–`06`. Violating one is
an architectural change requiring the what/why/alternatives/risks explanation and an ADR.

## Alternatives Considered
Treating architecture as advisory — rejected; without hard rules, a broad, multi-session
project erodes into inconsistency.

## Future Improvements
Encode rules as automated fitness functions: import-boundary linting (rules 3–4), a check
that mutations emit outbox events (rule 5), OpenAPI/client sync check (rule 6), and a
resilience test in CI (rule 9).

## Implementation Notes
- When a task seems to require breaking a rule, stop and raise it as **Decision Required**.
- New subsystems must fit the ports/events model — don't bolt on a parallel architecture.
- Keep entity names aligned across DB, API, KG, and UI (`00_Overview/Glossary.md`).
