# Technical Architecture

## Purpose
Describe the *internal* technical structure of the backend/frontend: layering, module
anatomy, contracts, and cross-cutting concerns. Complements the system view.

## Current State
Design only. The layering below is the target for Milestone 2 onward.

## Layered (clean) architecture
Each backend module is organized as:

```
router (HTTP)  ->  service (use-cases)  ->  repository (persistence)
      |                   |                       |
   schemas (Pydantic)  domain events         SQLAlchemy models
```

- **Router:** validates input, enforces auth, calls services. No business logic.
- **Service:** use-cases/business rules; orchestrates repositories + emits events;
  transaction boundary (unit of work).
- **Repository:** data access only; hides SQL/ORM behind an interface.
- **Domain:** entities, value objects, and events in `packages/hermes-domain`, independent
  of framework and I/O.

Frontend mirrors separation: server components for data, client components for
interaction, server state via TanStack Query, types from the generated client.

## The contract seam (no drift)
FastAPI emits an **OpenAPI schema** → a **TypeScript client** is generated into
`packages/ts-client`. Frontend and backend types cannot silently diverge. This is a
first-class architectural rule.

## Cross-cutting concerns
| Concern | Approach |
|---------|----------|
| **AuthN/Z** | Verified at gateway; RBAC + resource checks in services. |
| **Validation** | Pydantic (backend), zod/generated types (frontend). |
| **Errors** | Typed error contract; retryable vs fatal distinguished for jobs. |
| **Events** | Emitted via outbox in the same transaction as the write. |
| **Idempotency** | Consumers dedupe on event id; external ops use idempotency keys. |
| **Observability** | Structured logs + `trace_id` threaded api→worker→agentd (M12). |
| **Config** | 12-factor env; provider selection via plugin registry. |

## Architecture Decisions
1. **Framework-independent domain.** Business rules don't import FastAPI/SQLAlchemy,
   keeping them testable and portable.
2. **Repository pattern + unit of work.** Enables testing with fakes and swapping storage.
3. **Generated client over hand-written.** Eliminates a whole class of integration bugs.
4. **Module boundaries enforced by convention + review** (and later import-linting).

## Alternatives Considered
- **Active Record / fat models** — rejected: couples domain to ORM, harder to test.
- **GraphQL API** — deferred: REST + OpenAPI gives simpler codegen and caching now;
  GraphQL can be added as an adapter later if needed.
- **tRPC** — rejected: ties frontend to a TS backend; Hermes' backend is Python.

## Future Improvements
Add import-boundary enforcement (e.g. `import-linter`), contract tests against OpenAPI,
and architectural fitness functions in CI.

## Implementation Notes
- Start the layering in Milestone 2 with one module (Projects/Tasks) as the reference
  implementation others mirror.
- Keep services thin over rich domain objects; avoid logic leaking into routers.
- The unit-of-work commits the write and the outbox event together.
