# Claude Code — Operating Instructions

## Purpose
Define how every future Claude Code session must operate in this repository. This is the
governance contract for AI-assisted development. Read it before doing anything.

## Current State
The repository is at **Milestone 0 — documentation only** (see
`09_Implementation/Current_Status.md`). No code exists. Do not assume runtime behavior.

## Before you code — required reading
1. `CLAUDE.md` (root)
2. This file
3. `docs/PROJECT_BIBLE/README.md` and the sections relevant to your task
4. `docs/PROJECT_MAP.md`, `docs/AUDIT_REPORT.md`, `docs/MISSING_INFORMATION.md`
5. The relevant numbered spec(s) in `docs/00-15`

## Core operating rules
Claude Code **must**:
- **Read the Project Bible before coding** and understand the existing architecture.
- **Preserve working functionality;** prefer improving existing systems over rewrites.
- **Avoid unnecessary rewrites;** justify any rewrite with what/why/alternatives/risks.
- **Preserve compatibility** (APIs, schemas, plugin contracts); use expand/contract for
  breaking changes.
- **Prefer mature open-source integrations** over rebuilding (a project non-goal to reinvent).
- **Keep Hermes the source of record;** never make an external tool authoritative.
- **Treat everything replaceable as a plugin** (AI, storage, search, integrations).
- **Write tests** for new behavior; keep CI green.
- **Update documentation** — including the affected Bible **Current State** — in the same
  change.
- **Explain architectural changes** before making them.
- **Keep systems modular;** respect module boundaries (no cross-module repository reach-through).
- **Respect milestone gates;** do not build ahead without approval.
- **Never create empty files or folders;** create structure only when it holds real content.

## Before major changes — always explain
Provide, up front:
1. **What** will change.
2. **Why** it is needed.
3. **What alternatives** exist (and why not chosen).
4. **What risks** exist (and mitigations).
Record significant decisions as an ADR (see `MISSING_INFORMATION.md §6`) and update the
relevant Bible sections.

## Handling unknowns
If information is missing, **do not guess silently.** Mark it **"Decision Required,"**
explain what must be decided, why it matters, and the options — and add it to
`docs/MISSING_INFORMATION.md`. Ask for a decision when it blocks progress.

## Git & workflow
- Work on the designated feature branch; **never push to `main` without explicit
  permission** (`08_Development/Git_Workflow.md`).
- Conventional Commits; small, vertical PRs; PR body states what/why/alternatives/risks.
- Do not commit secrets; use the vault + env config.

## Definition of done (every change)
Code + tests pass in CI · docs/Bible "Current State" updated · no empty files/folders ·
types strict-clean · architectural changes explained · milestone gate respected.

## Architecture Decisions
1. **AI-assisted development is governed, not ad-hoc** — these rules keep the project
   coherent across many sessions.
2. **Docs-with-code is mandatory** to prevent the design/code drift flagged in the audit.
3. **Decisions are explicit and recorded**, never buried in a diff.

## Alternatives Considered
Letting each session set its own conventions — rejected: guarantees drift and inconsistency
across a long-lived, multi-session project.

## Future Improvements
Add automated checks that enforce parts of this contract (docs-updated check, no-empty-file
check, import-boundary lint) once CI exists.

## Implementation Notes
See the companion rules: `Architecture_Rules.md`, `Coding_Rules.md`, `Build_Process.md`.
When these and a numbered spec disagree, prefer the Bible and raise the discrepancy as
"Decision Required."
