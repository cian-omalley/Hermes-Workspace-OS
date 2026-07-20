# hermes-domain

The **framework-independent domain layer** for Hermes Workspace OS: entities, value
objects, and domain events. This package must not import web/ORM/provider libraries — it
holds pure business concepts shared across `services/api`, `services/worker`, and (later)
`services/agentd`.

See `docs/PROJECT_BIBLE/02_Architecture/Technical_Architecture.md`.

## Milestone 1 status
Starter content only: the base `DomainEvent` type and the event envelope. Concrete
entities (Project, Task, Document, …) land in Milestone 2 alongside the database models.
