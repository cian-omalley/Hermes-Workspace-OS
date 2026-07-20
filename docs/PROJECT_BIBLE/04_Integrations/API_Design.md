# API Design

## Purpose
Define the conventions and shape of Hermes' API — the primary contract between the
frontend, external clients, and the core.

## Current State
**Implemented (M2).** The FastAPI gateway serves 22 `/api/v1` endpoints (full CRUD for the
core entities) with an auto-published OpenAPI schema. The **contract seam is live**: a
generated TypeScript client (`packages/ts-client`) is produced from the OpenAPI document via
`openapi-typescript`, and a CI job fails on any drift between the committed client and the
API. Authentication/authorization are not yet applied (M3).

## Style & conventions
- **REST + JSON** over the FastAPI gateway; **OpenAPI 3** auto-published.
- **Versioned:** `/api/v1/...`; additive changes preferred, breaking changes bump version.
- **Auth:** Bearer (JWT/session) verified at the gateway; RBAC per resource.
- **Resource-oriented paths:** `/workspaces`, `/projects`, `/projects/{id}/tasks`,
  `/documents`, `/assets`, `/repositories`, `/agents`, `/search`, `/integrations`.
- **Pagination:** cursor-based for large collections; consistent envelope.
- **Errors:** typed problem responses; distinguish client (4xx) vs server (5xx) vs
  retryable.
- **Idempotency:** mutating external-affecting endpoints accept idempotency keys.

## Realtime & webhooks
- **Realtime:** SSE/WebSocket channel for activity feeds, agent progress, search-as-you-type.
- **Inbound webhooks:** `/webhooks/notion`, `/webhooks/github`, `/webhooks/n8n` — signature
  verified, recorded in `webhook_events` for idempotency.

## The contract seam
FastAPI → OpenAPI schema → generated **TypeScript client** (`packages/ts-client`). Frontend
never hand-writes API types. This prevents drift and is enforced in CI (schema/client in
sync).

## Architecture Decisions
1. **REST + OpenAPI over GraphQL/tRPC** — simplest reliable codegen + caching for a
   Python backend + TS frontend (see `Technical_Architecture.md`).
2. **Gateway-enforced auth + per-resource RBAC** — defense in depth.
3. **Everything mutating emits domain events** via the outbox, so the API and event model
   stay consistent.

## Alternatives Considered
- **GraphQL** — deferred: flexible querying is valuable but adds complexity; can be added as
  an adapter over the same services later.
- **tRPC** — rejected: assumes a TS backend.
- **Ad-hoc realtime polling** — rejected in favor of SSE/WebSocket push.

## Future Improvements
Public API tokens with scopes (`api_tokens`), rate-limit tiers, GraphQL adapter, webhook
*out* subscriptions for third parties, and SDKs generated from OpenAPI.

## Implementation Notes
- Stand up the OpenAPI schema in M2 with the first module; generate the TS client in CI.
- Keep routers thin (validate + authorize + delegate); business logic in services.
- Document every endpoint's required role and emitted events.
- Verify webhook signatures before processing; treat payloads as untrusted.
