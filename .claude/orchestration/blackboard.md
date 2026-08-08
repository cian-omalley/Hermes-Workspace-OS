# Shared Blackboard

The **durable shared memory** for the active task. This is the tooling analogue of the agent
system's shared project-memory blackboard (`docs/16-AGENT_DEPARTMENTS.md §5`). The
`memory-keeper` agent owns it; any agent may read it.

**Rule of resumability:** after every step, this file alone must be enough for a fresh session
to answer *"what are we doing, what's decided, and what's next?"* Keep it current; keep it short.

> This file starts as a template. Overwrite the placeholders when a task begins. When no task is
> active, leave the template in place (do not delete — it documents the format).

---

## Mission
<!-- One or two sentences: the goal and why. -->
_Placeholder — no active task. State the goal + why here when a task begins._

## Exit criteria
<!-- What "done" looks like, as verifiable checks. -->
- _Placeholder — e.g. "tests X pass", "doc Y exists", "CI green"._

## Plan (steps → owner → exit criterion → status)
| # | Step | Owner (agent) | Exit criterion | Status |
|---|------|---------------|----------------|--------|
| 1 | _…_ | _product-manager_ | _…_ | pending |

## Decisions (with rationale)
<!-- Recorded so they are not relitigated. Cite origin: agent/step or spec. -->
- _Placeholder — decision · why · who/when._

## Open questions
- _Placeholder — question · who can answer._

## Per-agent status
| Agent | Last did | Handoff to |
|-------|----------|------------|
| _…_ | _…_ | _…_ |

## Next action
<!-- The single most important thing to do next. A resumed session starts here. -->
_Placeholder — the one next step._

## Guardrails for this task
- Milestone gate respected: _yes/flagged_ · Budget/stop condition: _…_ · Gated actions pending
  approval: _…_
