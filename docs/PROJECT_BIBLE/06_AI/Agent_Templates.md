# Agent Templates

## Purpose
Define the reusable templates for the default project agent team — their roles, tools,
permissions, and prompts — so agent creation is consistent and extensible.

## Current State
Designed (`docs/10`); unimplemented (M9). Templates are configuration that instantiate
idle agents at project creation.

## Default team templates
Grouped into departments (`docs/16-AGENT_DEPARTMENTS.md`): **Engineering (Core)** and
**Knowledge & Operations**.

| Department | Role | Goal | Key tools | Default permissions |
|------------|------|------|-----------|---------------------|
| Engineering | **Project Manager** *(lead)* | Plan, decompose goals, coordinate, update roadmap/kanban | Tasks, Search, KG | Read all; write tasks/roadmap; no external writes |
| Engineering | **Research** | Gather & summarize with citations | Search, Files/ingest, Web (if enabled) | Read; create research items |
| Engineering | **Developer** | Read/modify code (sandboxed) | Code (sandbox), GitHub (read; write gated), Search | Sandbox write; external push needs approval |
| Engineering | **Code Review** | Review diffs/PRs | GitHub (read), Search, KG | Read; comment (gated) |
| Engineering | **Testing** | Generate/run tests, report | Code (sandbox), CI hooks | Sandbox execute; report artifacts |
| Engineering | **Release** | Prepare release notes, coordinate release | GitHub (read), Docs | Read; draft notes (publish gated) |
| Knowledge & Ops | **Orchestrator** *(lead)* | Decompose, route across departments, checkpoint, guard budgets | Search, KG, Tasks | Read; plan/route; no external writes |
| Knowledge & Ops | **Knowledge Curator** | Sort & rewrite incoming sources into the hub | Files, Docs, Web | Read; write knowledge docs |
| Knowledge & Ops | **DeepWiki Brain** | Generate/maintain grounded repo wiki & diagrams | Files, Docs, KG, GitHub (read) | Read; write documents/wiki |
| Knowledge & Ops | **Memory Keeper** | Curate shared blackboard, decisions, memory retention | Docs, KG, Memory | Read; write memory/knowledge |

## Template shape
Each template declares: `role`, `name`, default `config` (model, memory scope), `permissions`
(data scope, tool allowlist, external-action policy, budget), and role prompt(s)
(`Prompt_System.md`). Stored per `docs/05 §1.9` (`agents.config`/`permissions`).

## Architecture Decisions
1. **Least-privilege per role** — e.g. Research can't push code; Developer's external pushes
   need approval.
2. **Ephemeral instantiation** — templates create idle agents; runs are on-demand.
3. **Customizable & extensible** — workspaces can override templates or add custom roles.

## Alternatives Considered
- **One generalist agent** — rejected: specialization improves reliability/auditability.
- **Hardcoded agents in code** — rejected: templates as config enable customization and a
  future marketplace.

## Future Improvements
Domain-specific team packs (research lab, data team), a template marketplace, learned/tuned
templates from evaluation results, and per-template guardrail policies.

## Implementation Notes
- Instantiate the team on `project.created` (idle, zero compute).
- Enforce template permissions at the tool layer, not just by prompt instruction.
- Version templates; changing a template shouldn't silently alter running agents.
- Keep prompts in the prompt module, referenced by templates.
