# Agent System

## Purpose
Define the AI agent framework: how agents are created, run, remember, are permissioned,
communicate, and produce artifacts. Canonical spec: `docs/10-AGENT_SYSTEM.md`.

## Current State
Designed; unimplemented (M9). Built on **LangGraph**, executed by the `agentd` service,
with models via the AI provider plugin.

## Principles
- **Ephemeral & purpose-scoped.** No idle agent compute; agents exist as rows and run only
  when triggered.
- **Communicate, share memory, use tools, update tasks, produce artifacts.**

## Default project agent team
Project Manager · Research · Documentation · Developer · Code Review · Testing · Release
(plus custom). Provisioned idle at project creation; templates in `06_AI/Agent_Templates.md`.

## Lifecycle
`Created → Idle → Scheduled → Running → (WaitingHuman) → Succeeded/Failed → Idle`, with
`Disabled` as a terminal off-state. Triggers are event-driven (e.g. `repo.pr.opened` →
Code Review) or plan-driven (PM decomposes a goal).

## Permissions (least privilege)
Each run carries: data scope, tool allowlist, external-action rights (with optional
approval), and budget (tokens/cost/time). Enforced by the tool layer; all privileged
actions audited.

## Tools
Search, Knowledge Graph, Projects/Tasks, GitHub, Files, Notion, and sandboxed Code
(Developer). Exposed via a tool registry and optionally **MCP**. Each tool declares a typed
schema, permission requirement, and mutation flag.

## Communication & orchestration
Structured messages between agents (`agent_messages`) + a shared project memory
"blackboard"; a supervisor/orchestrator (LangGraph supervisor pattern) routes work and
aggregates results.

## Architecture Decisions
1. **LangGraph** for explicit stateful graphs, cycles, checkpoints, and human-in-the-loop.
2. **Ephemerality by design** to control cost and avoid runaway processes.
3. **Approval gates + sandboxing** for mutating/external/code actions.
4. **Provider-agnostic reasoning** via the AI plugin (per agent/run selection).

## Alternatives Considered
- **Always-on autonomous agents** — rejected (cost, safety, and an explicit non-goal).
- **A single "do-everything" agent** — rejected; specialized roles are more reliable and
  auditable.
- **Custom orchestration from scratch** — rejected; LangGraph is mature and fit-for-purpose.

## Future Improvements
Learned routing, richer inter-agent negotiation, agent performance evaluation
(`Evaluation_System.md`), and a marketplace of community agent templates.

## Implementation Notes
- Persist runs/messages/artifacts/memory per `docs/05 §1.9`.
- Enforce max steps/iterations to prevent loops; thread `trace_id` for observability.
- Developer-agent code execution runs in isolated containers with no ambient credentials.
- See `Memory_System.md` for memory tiers and sharing.
