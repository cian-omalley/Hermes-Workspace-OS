# Orchestration — how the agent departments work together

This directory is the **coordination protocol** for the Hermes department agents
(`.claude/agents/`). It is Claude Code *tooling* — it lets a team of agents collaborate on one
task and lets that task **run across many sessions** (the "run for days" mechanism) by keeping
durable state in the repo instead of in a single session.

Canonical design: [`docs/16-AGENT_DEPARTMENTS.md`](../../docs/16-AGENT_DEPARTMENTS.md).

## The departments

**Engineering (Core)** — builds & verifies the product:
`product-manager` (lead) · `researcher` · `engineer` · `code-reviewer` · `qa-tester` ·
`release-manager`.

**Knowledge & Operations** — maintains the brain and keeps long tasks running:
`orchestrator` (lead) · `knowledge-curator` (the sorter) · `deepwiki-brain` · `memory-keeper`.

Full roster and tools: the frontmatter of each file in [`../agents/`](../agents/).

## Execution model (important)

Claude Code subagents **do not spawn other subagents**. So:

- The **top-level session is the Supervisor**. It reads the plan and invokes department agents
  via the Agent tool, one focused job at a time.
- The **`orchestrator`** agent produces the *routing plan* (decompose → route → checkpoint →
  guard); the top-level session *executes* it.
- Agents coordinate through the **shared blackboard** ([`blackboard.md`](./blackboard.md)),
  not by calling each other.

## Running a task (the loop)

1. **Intake.** Copy [`task-template.md`](./task-template.md) into the blackboard (or a per-task
   file) and state the mission + exit criteria.
2. **Plan.** Invoke `orchestrator` (or `product-manager`) to decompose the goal into
   department-sized steps with owners and exit criteria. Record it on the blackboard.
3. **Execute a step.** Invoke the owning agent (e.g. `engineer` for code, `deepwiki-brain` for
   docs). Keep steps small and verifiable.
4. **Verify.** Route to `qa-tester` / `code-reviewer` as needed.
5. **Checkpoint.** Have `memory-keeper` update the blackboard: decisions, per-agent status,
   handoffs, and the single **Next action**. After this, the blackboard alone must be enough to
   resume.
6. **Repeat or pause.** Pick the next step, or stop. Because state is on the blackboard, a
   *new* session can resume by reading it first.

### Running "for days" across sessions
- State lives in the repo (blackboard + committed work), so elapsed time between steps costs
  nothing and survives session ends.
- To pace a long task, the driving session may schedule check-ins (a wakeup/Routine) that
  re-read the blackboard and run the next step. Compute is spent only while a step runs.

## Guardrails

- **Milestone gate.** Never route work past the current milestone
  (`docs/PROJECT_BIBLE/09_Implementation/Current_Status.md`, `docs/00-ROADMAP.md`) without
  explicit human approval.
- **Gated actions.** Mutating/external steps (pushes, publishes, external services) are
  human-approval checkpoints, not automatic.
- **Least privilege.** Each agent has only the tools its role needs; Knowledge & Operations
  agents never write product code.
- **Budgets & stop condition.** Set loop/step limits up front; on exhaustion, escalate rather
  than loop.
