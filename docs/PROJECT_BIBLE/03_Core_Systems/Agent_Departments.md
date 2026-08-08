# Agent Departments

## Purpose
Organize the agent system into **departments** with a **Harness** (durable runtime), a unified
**Knowledge & Memory Hub**, and a coordination protocol so a team of agents can collaborate on
a single task over a long horizon. This is the governance view; the canonical design is
`docs/16-AGENT_DEPARTMENTS.md`.

## Current State
Designed; runtime **unimplemented (M9)**. The department model is, however, **live today as
Claude Code tooling** — `.claude/agents/` subagents + the `.claude/orchestration/` protocol —
which build and maintain this repo. See `docs/16` §9 and `.claude/orchestration/README.md`.

## Departments
| Department | Members | Writes |
|---|---|---|
| **Engineering (Core)** | Project Manager (lead), Research, Developer, Code Review, Testing, Release | code (sandboxed; external pushes gated) |
| **Knowledge & Operations** | Orchestrator (lead), Knowledge Curator, DeepWiki Brain, Memory Keeper | docs & memory only; no product code |

## The Harness (runs for days)
- LangGraph executor (`agentd`) + supervisor routing + scheduler (`docs/16 §4`, `docs/10 §9`).
- **Durability:** checkpoint/resume + a durable blackboard worklog let a task span days while
  consuming compute only during active steps (ephemeral, `docs/10 §10`).
- **Budgets across the whole task** and loop limits prevent runaway runs.
- Human-in-the-loop checkpoints for mutating/external actions.

## Knowledge & Memory Hub
One addressable brain composing existing stores (no new store): working/short/long-term memory
(`agent_memory` + Qdrant), the shared blackboard, the DeepWiki brain (`docs/09`,
`wiki_pages`), the knowledge graph (Neo4j, `docs/11`), and the docs knowledge hub
(`docs/knowledge/`). Retrieval is GraphRAG (`docs/12`). Curated by the Memory Keeper +
Knowledge Curator; see `Memory_System.md`.

## Architecture Decisions
1. **Departments over a flat team** — clearer ownership, routing, and least-privilege
   boundaries than one undifferentiated pool.
2. **Compose, don't add a store** — the Knowledge & Memory Hub reuses memory + DeepWiki + KG +
   the docs hub; no parallel database.
3. **Durability via checkpoints + blackboard**, not long-held processes — matches the
   ephemeral, no-idle-compute rule while still supporting multi-day tasks.
4. **Two-layer delivery** — design now (this doc + `docs/16`); product runtime at M9; a real
   `.claude/` tooling team is usable immediately without jumping the milestone gate.

## Alternatives Considered
- **One flat agent team (no departments)** — rejected: weaker ownership and coordination at
  scale; `docs/16 §2` supersedes.
- **A dedicated long-running daemon per task** — rejected: violates the ephemeral/no-idle-compute
  rule; checkpoint-and-resume achieves "runs for days" without it.
- **A new memory/brain database** — rejected: `agent_memory` + Qdrant + Neo4j + `docs/knowledge`
  already cover it.

## Future Improvements
Domain-specific department packs (Security, Data/Integrations, Design), learned routing from
evaluation results, and a department-level guardrail policy layer.

## Implementation Notes
- Instantiate departments as configuration (`06_AI/Agent_Templates.md`), not hardcoded agents.
- Enforce department permission defaults at the tool layer, not by prompt alone.
- Persist only lasting value to the blackboard/`agent_memory`; keep run scratch in checkpoints.
- Keep this governance doc in sync with `docs/16` and `Current_Status.md`.
