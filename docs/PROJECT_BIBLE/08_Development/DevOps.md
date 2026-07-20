# DevOps

## Purpose
Define CI/CD, observability, and operational practices that keep Hermes reliable and
maintainable.

## Current State
No CI, monitoring, or automation exists yet. CI lands in Milestone 1; full observability in
Milestone 12.

## CI/CD (GitHub Actions)
Pipeline on every PR:
1. **Lint & format** (ruff, eslint/prettier).
2. **Type-check** (mypy strict, tsc strict).
3. **Test** (unit + integration; sampled evals).
4. **Contract check** (OpenAPI ↔ generated TS client in sync).
5. **Build** (Docker images).
6. (Security) **dependency review + secret scanning.**
Merges blocked unless green. Tagged releases build/publish versioned images.

## Observability (M12)
- **Logs:** structured JSON with `trace_id` correlation.
- **Metrics:** Prometheus (request rates, queue depth, job latency, agent runs, token cost).
- **Tracing:** OpenTelemetry across api → worker → agentd.
- **Dashboards & alerts:** shipped as templates.

## Operations
- **Backups:** Postgres (dump/WAL), Neo4j dumps, Qdrant snapshots, MinIO replication;
  scheduled with a tested restore runbook.
- **Health:** per-service `/health` aggregating provider `health()` checks.
- **Runbooks:** backup/restore, incident, upgrade/migration (M12).

## Architecture Decisions
1. **CI as the quality gate** — standards are enforced by machines, not goodwill.
2. **Vendor-neutral observability** (OTel/Prometheus) — no lock-in.
3. **Backups + rebuildable derived stores** — recovery combines DB/object restore with
   `reindex`/`rebuild-graph`.

## Alternatives Considered
- **Other CI (GitLab CI, CircleCI)** — GitHub Actions chosen (repo is on GitHub, zero extra
  setup).
- **Proprietary APM** — rejected for self-host-first; OTel/Prometheus preferred.
- **No formal runbooks** — rejected; operability is a product requirement.

## Future Improvements
CD to a reference environment, canary/blue-green deploys, SLOs + alerting, chaos/resilience
testing (esp. store-down scenarios), and automated dependency updates.

## Implementation Notes
- Stand up CI in M1 with the skeleton (even a "hello world" smoke test).
- Add secret scanning + dependency review immediately (supply-chain risk in
  `MISSING_INFORMATION.md`).
- Introduce metrics/tracing incrementally; don't defer all observability to M12 — add
  `trace_id` logging from the first service.
