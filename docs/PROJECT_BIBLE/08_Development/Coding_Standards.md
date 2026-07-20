# Coding Standards

## Purpose
Define the code-quality bar so contributions are consistent, type-safe, and maintainable —
by humans and Claude Code alike.

## Current State
Standards defined; no code yet. Linters/formatters/type-checkers are declared
(`docs/04`) and land with Milestone 1.

## Language standards
### Python (backend/AI)
- **Python 3.12+**, fully type-hinted; **`mypy` strict** must pass.
- **`ruff`** for lint + format (single tool); no unused imports/vars.
- **Pydantic v2** for all I/O schemas; no untyped dicts crossing boundaries.
- **Clean layering:** router → service → repository; domain logic framework-independent.
- **Docstrings** on public modules/classes/functions explaining *why*.

### TypeScript (frontend)
- **`tsc` strict**; no `any` without justification.
- **ESLint + Prettier**; consistent import ordering.
- **Types from the generated OpenAPI client** — never hand-write API types.
- **Components:** small, reusable, accessible; server vs client components deliberate.

## General rules
- **No duplicated logic** — extract shared code into `packages/`.
- **Small, focused functions and modules;** single responsibility.
- **No empty files or folders;** create structure only with real content.
- **Errors are typed and meaningful;** distinguish retryable vs fatal.
- **No secrets in code;** use the vault and env config.
- **Comments match the surrounding density and idiom;** explain rationale, not mechanics.

## Architecture Decisions
1. **Strict typing both languages** — catches errors early, aids AI-assisted edits.
2. **One formatter/linter per language** (ruff, prettier) — no bikeshedding.
3. **Generated client** as the sole source of frontend API types.

## Alternatives Considered
- **Loose typing / gradual adoption** — rejected: type safety is a stated project value.
- **Black + isort + flake8 stack** — replaced by `ruff` (faster, unified).

## Future Improvements
Import-boundary linting (`import-linter`), complexity/coverage gates, pre-commit hooks, and
architectural fitness functions in CI.

## Implementation Notes
- Enforce all standards in CI (M1); failing lint/types/tests blocks merge.
- Add a `just check` command running ruff + mypy + eslint + tsc.
- Establish the reference module (Projects/Tasks) as the style exemplar others follow.
