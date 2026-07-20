# hermes-api

The FastAPI **gateway and core API** for Hermes Workspace OS. Handles validation, auth
(from Milestone 3), routing to core modules, persistence (from Milestone 2), and domain
event emission.

Run locally: `just api` (or `uvicorn hermes_api.main:app --reload`).

## Milestone 1 status
Skeleton only: application factory, settings, and a `/health` endpoint with tests. Domain
modules (projects, tasks, …) arrive in Milestone 2. See
`docs/PROJECT_BIBLE/04_Integrations/API_Design.md`.
