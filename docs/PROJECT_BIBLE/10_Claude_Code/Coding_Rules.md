# Claude Code — Coding Rules

## Purpose
Concrete, day-to-day coding rules for changes in this repository. Complements
`08_Development/Coding_Standards.md` (the standards) with imperative do/don't guidance for
AI-assisted edits.

## Current State
No code yet; these rules apply from the first line written (Milestone 1).

## Always
- **Use clean architecture** (router → service → repository; framework-independent domain).
- **Use type safety** — Python fully hinted with `mypy` strict; TS with `tsc` strict. No
  `any`/untyped dicts crossing boundaries.
- **Avoid duplicated logic** — extract shared code into `packages/`; reuse before rewriting.
- **Create reusable components** — small, single-responsibility functions/modules/UI parts.
- **Write maintainable code** — clear names, minimal cleverness, comments explain *why*.
- **Document decisions** — update the relevant Bible sections and, for significant choices,
  an ADR.
- **Write tests** alongside code; add a regression test for every bug fix.
- **Validate at boundaries** — Pydantic (backend), generated types/zod (frontend).
- **Handle errors meaningfully** — typed errors; distinguish retryable vs fatal for jobs.

## Never
- **Never create empty files or folders.** Create structure only when it holds real content.
- **Never hand-write API types** — use the generated client.
- **Never commit secrets** — use the encrypted vault + env config.
- **Never bypass a module boundary** (no reaching into another module's repositories/DB).
- **Never make an external tool the source of record.**
- **Never leave a section blank when unsure** — write **"Decision Required"** and explain.
- **Never disable type checks/linters/tests to "make it pass."**

## Before a major change
State **what** changes, **why**, **alternatives**, and **risks** (with mitigations) before
implementing. Prefer improving existing systems over rewrites.

## Definition of done (per change)
Strict types clean · lint/format clean · tests written and passing · docs/Bible updated ·
no empty files/folders · commit follows Conventional Commits · CI green.

## Architecture Decisions
1. **Type safety and tests are gates, not suggestions** — they enable safe AI-assisted
   iteration.
2. **Reuse over rewrite** — protects working functionality (a core project rule).
3. **`packages/` for shared code** — single source of truth for cross-service logic.

## Alternatives Considered
Looser, "move fast" coding — rejected: this is a long-lived platform where drift and debt
compound quickly.

## Future Improvements
Pre-commit hooks, coverage thresholds, complexity limits, and import-boundary linting to
enforce these rules automatically.

## Implementation Notes
- Mirror the reference module (Projects/Tasks) for structure and style.
- Keep routers thin; put business rules in services over rich domain objects.
- Follow existing file conventions; match surrounding comment density and idiom.
