# Cross-service tests

End-to-end and smoke tests that exercise the whole Hermes stack (as opposed to the
unit/integration tests that live inside each service/package).

- `smoke/` — minimal "is the stack up and reachable" checks. Gated behind
  `HERMES_SMOKE=1` so they only run against a running stack (`just up`), not in unit CI.

As the platform grows (Milestone 10), the headline user workflows (W1–W5, see
`docs/PROJECT_BIBLE/01_Product/User_Workflows.md`) get full Playwright e2e coverage here.
