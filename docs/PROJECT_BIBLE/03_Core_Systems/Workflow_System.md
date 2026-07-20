# Workflow System (Automation)

## Purpose
Define how users automate work across Hermes and external tools. Canonical spec:
`docs/14-WORKFLOW_SYSTEM.md`.

## Current State
Designed; unimplemented (M11). Built on **n8n** for visual flows, bridged to Hermes' native
event bus, plus lightweight native rules.

## Two layers
- **Native triggers/actions:** Hermes emits domain events and exposes actions (create task,
  generate doc, run agent). Simple rules run natively for speed.
- **n8n workflows:** visual, multi-step, branching, external-service automations for
  anything complex.

## Triggers & actions
- **Triggers:** domain events (`asset.ingested`, `repo.pr.opened`, `task.completed`, …),
  schedules (cron), manual, external webhooks.
- **Actions (Hermes n8n nodes):** create/update tasks/docs/research/ideas/decisions;
  generate doc/diagram/image; run agent; search/GraphRAG; Notion/GitHub ops; notify.

## Example templates
Auto-document on repo change · Weekly research digest · Release notes on merge · New file →
triage task · Issue SLA ping · Idea → project scaffold.

## Architecture Decisions
1. **n8n over a custom engine** — mature, self-hostable, 400+ integrations; kept as a peer
   service bridged via events (replaceable via the Automation Engine port).
2. **Native fast-path** for trivial single-step rules to avoid n8n overhead.
3. **Idempotent, audited, scoped:** workflows run with a scoped service identity; all
   mutations audited; deliveries deduped on event id.

## Alternatives Considered
- **Build a bespoke workflow engine** — rejected: reinvents mature tooling (a non-goal).
- **Temporal/Prefect** — powerful but heavier and code-centric; n8n better serves visual,
  non-developer authoring. Revisit for complex internal orchestration.
- **Embed n8n in-process** — rejected: isolation and replaceability favor a peer service.

## Future Improvements
A native lightweight rules engine for common cases, a template gallery, workflow
versioning, and testing/preview of workflows before enabling.

## Implementation Notes
- Bridge subscribes to the event bus and forwards subscribed events to n8n via signed
  webhooks; bindings stored in `workflows` (`docs/05 §1.11`).
- Hermes n8n nodes call the API with scoped credentials from the secret vault.
- Record executions in `workflow_runs`; surface failures with retry/backoff.
