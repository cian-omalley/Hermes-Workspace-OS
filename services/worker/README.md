# hermes-worker

Celery **workers** for Hermes Workspace OS: async jobs for ingestion, integration sync,
analysis, and index/graph updates. Consumes domain events from the Redis-backed bus.

Run locally: `just worker`.

## Milestone 1 status
Skeleton only: a configured Celery app and a `ping` health task with a test. Real
pipelines (ingestion, sync, indexing) arrive from Milestone 6. See
`docs/PROJECT_BIBLE/02_Architecture/Service_Architecture.md`.
