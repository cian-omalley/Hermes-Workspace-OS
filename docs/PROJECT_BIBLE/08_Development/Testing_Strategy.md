# Testing Strategy

## Purpose
Define what and how Hermes tests so that "tests are required, not optional" is operational,
not aspirational.

## Current State
No tests exist yet (no code). The testing pyramid and gates below apply from Milestone 1.

## Test levels
| Level | Scope | Tools | Where |
|-------|-------|-------|-------|
| **Unit** | Pure logic, services with fakes | pytest / vitest | Every module |
| **Integration** | Services + real datastores (containers) | pytest + httpx / testcontainers | Per module |
| **Contract** | API matches OpenAPI; provider adapters match ports | schema tests, port conformance suites | api + plugins |
| **E2E** | Headline user workflows (W1–W5) | Playwright | `tests/` |
| **Eval** | AI output quality | in-repo eval harness (`06_AI/Evaluation_System.md`) | AI features |

## Key policies
- **Every new behavior ships with tests;** bug fixes ship with a regression test.
- **Port conformance suites** guarantee any provider swap is safe (storage/AI/search).
- **The resilience test (W5): full core suite passes with Notion disconnected** — gates M4.
- **Contract seam:** CI verifies the generated TS client is in sync with the OpenAPI schema.
- **Deterministic-first:** prefer objective assertions; use LLM-as-judge only for
  subjective AI quality, with human spot-checks.

## Architecture Decisions
1. **Testing pyramid** — many fast unit tests, fewer integration/e2e.
2. **Conformance tests per plugin port** — the mechanism that makes "everything swappable"
   trustworthy.
3. **CI-enforced gates** — lint, types, unit, integration, and (sampled) evals block merge.

## Alternatives Considered
- **Manual/e2e-heavy testing** — rejected: slow, flaky, poor coverage of logic.
- **No AI evaluation** — rejected: AI regressions would go unnoticed.
- **Mock-only integration tests** — supplemented with containerized real stores for
  fidelity.

## Future Improvements
Coverage thresholds, mutation testing, load/performance benchmarks (search P95, ingestion
throughput), nightly full eval runs, and flaky-test quarantine.

## Implementation Notes
- Provide factory fixtures + seed data (M2) for fast test setup.
- Use testcontainers (or compose) for Postgres/Redis/Qdrant/Meili/Neo4j in integration/e2e.
- Add `just test` (unit+integration) and `just e2e` (Playwright) commands.
- Write W5 (disconnect Notion) as a first-class e2e test at M4.
