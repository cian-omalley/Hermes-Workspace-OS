# Agent Templates

## Purpose
Define the reusable templates for the default project agent team — their roles, tools,
permissions, and prompts — so agent creation is consistent and extensible.

## Current State
Designed (`docs/10`); unimplemented (M9). Templates are configuration that instantiate
idle agents at project creation.

## Default team templates
| Role | Goal | Key tools | Default permissions |
|------|------|-----------|---------------------|
| **Project Manager** | Plan, decompose goals, coordinate, update roadmap/kanban | Tasks, Search, KG | Read all; write tasks/roadmap; no external writes |
| **Research** | Gather & summarize with citations | Search, Files/ingest, Web (if enabled) | Read; create research items |
| **Documentation** | Generate/maintain docs & DeepWiki | Files, Docs, KG, GitHub (read) | Read; write documents/wiki |
| **Developer** | Read/modify code (sandboxed) | Code (sandbox), GitHub (read; write gated), Search | Sandbox write; external push needs approval |
| **Code Review** | Review diffs/PRs | GitHub (read), Search, KG | Read; comment (gated) |
| **Testing** | Generate/run tests, report | Code (sandbox), CI hooks | Sandbox execute; report artifacts |
| **Release** | Prepare release notes, coordinate release | GitHub (read), Docs | Read; draft notes (publish gated) |

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
