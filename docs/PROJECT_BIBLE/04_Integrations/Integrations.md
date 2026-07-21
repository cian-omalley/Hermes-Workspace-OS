# Integrations (Overview)

## Purpose
Explain how Hermes connects to external tools while preserving its source-of-record
guarantee. Integrations are plugins, not special cases.

## Current State
**Notion is implemented (M4).** A `NotionClient` abstraction (in-memory `FakeNotionClient`
for tests, real `HttpNotionClient` for production) sits behind a declarative entity↔Notion
mapping (Projects, Tasks) and a sync engine that is idempotent (checksums + `webhook_events`
dedup) and conflict-aware (**Hermes wins**). Admin-guarded connect/status/sync endpoints and
a signature-verified inbound webhook drive it; the Notion token is stored in the encrypted
vault. The **disconnect-safe** guarantee is tested. GitHub (M5) is next and reuses the same
`integrations`/`sync_state`/`webhook_events` machinery. Remaining Notion databases (beyond
Projects/Tasks) follow the same declarative mapping pattern.

## Principles
- **Hermes owns the data.** Integrations sync *to/from* Postgres; they never become the
  source of record.
- **Disconnect-safe.** Any integration can be turned off and the core keeps working
  (tested for Notion at M4).
- **Uniform contract.** Every integration implements `connect`, `sync_out`, `sync_in`,
  `verify_webhook` — so adding one doesn't touch core.

## Integration matrix
| Integration | Direction | Entities | Milestone | Spec |
|-------------|-----------|----------|-----------|------|
| **Notion** | Two-way | 10 databases (projects, tasks, research, repos, docs, agents, knowledge, ideas, meetings, assets) | M4 | `docs/07` |
| **GitHub** | Two-way (code read-authoritative) | repos, commits, PRs, issues | M5 | `docs/08` |
| Slack | Outbound (notify) | messages | Later | (planned) |
| Google Drive | Inbound (files) | assets | Later | (planned) |

## Shared sync machinery
- **`sync_state`** tracks external ids/versions/checksums per entity.
- **`webhook_events`** provides inbound idempotency.
- **Conflict policy** defaults to *Hermes wins*, configurable per field.
- **Loop prevention** via last-write comparison.
- All sync runs on the worker queue, never in the request path; rate-limited with backoff.

## Architecture Decisions
1. **Integrations are plugins** behind one port → replaceable and testable in isolation.
2. **Reconciliation** (periodic poll comparing `sync_state`) catches missed webhooks.
3. **Least-privilege credentials** stored in the encrypted vault.

## Alternatives Considered
- **Bespoke, per-tool integration code in core** — rejected: unmaintainable and couples
  core to vendors.
- **One-way mirroring only** — rejected for Notion/GitHub where two-way is the value; but
  read-authoritative boundaries are respected (GitHub owns code).

## Future Improvements
A community integration marketplace; a generic OAuth/connector framework; more providers
(Slack, Drive, Jira, Linear) as plugins.

## Implementation Notes
- Implement the Integration port first with a fake provider + conformance tests, then Notion.
- Every integration ships round-trip, conflict, idempotency, and disconnect tests.
- See `API_Design.md` for webhook endpoints and `Third_Party_Services.md` for provider
  specifics.
