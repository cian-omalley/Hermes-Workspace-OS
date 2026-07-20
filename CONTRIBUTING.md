# Contributing to Hermes Workspace OS

Thank you for your interest in contributing! Hermes is an open-source (Apache-2.0) AI
Workspace Operating System. This guide explains how to get involved productively.

> **Project stage:** Milestone 0 — the repository currently holds the **engineering
> foundation (documentation only)**. Most "code" contributions begin at Milestone 1. Until
> then, the highest-value contributions are **design review, documentation, and helping
> resolve the open decisions in `docs/MISSING_INFORMATION.md`.**

## 1. Before you start

1. Read `CLAUDE.md`, `docs/PROJECT_MAP.md`, and the relevant Project Bible sections.
2. Check `docs/MISSING_INFORMATION.md` for open decisions and known gaps.
3. Open an issue to discuss anything non-trivial **before** writing code — align on the
   approach first.

## 2. Ways to contribute

- **Design feedback** on the specs (`docs/00-15`) and Project Bible.
- **Documentation** improvements and corrections.
- **Resolving open decisions** (D1–D10 in `MISSING_INFORMATION.md`).
- **Code** — once implementation milestones are underway.
- **Testing, examples, and tooling.**

## 3. Development workflow (once code exists)

1. **Branch** from `main`: `feat/<short-desc>`, `fix/<short-desc>`, or `docs/<short-desc>`.
2. **Keep changes focused** — one logical change per PR; prefer vertical slices.
3. **Match the architecture** described in the Project Bible; don't rewrite working
   systems without a documented reason.
4. **Write tests** for new behavior; keep the build green.
5. **Update documentation** — including the affected Bible "Current State" sections.
6. **Run checks locally** (`just check` / `just test` once available) before pushing.
7. **Open a PR** using the template; describe what changed, why, alternatives, and risks.

Detailed conventions: `docs/PROJECT_BIBLE/08_Development/` (Coding_Standards, Git_Workflow,
Testing_Strategy) and `docs/PROJECT_BIBLE/10_Claude_Code/`.

## 4. Standards

- **Type safety** everywhere (Python: `mypy` strict; TS: `tsc` strict).
- **Clean architecture**: routers → services → repositories; no cross-module reach-through.
- **No duplicated logic**; prefer reusable components and shared packages.
- **Everything replaceable is a plugin** (AI, storage, search, integrations).
- **No empty files or folders.**
- **Conventional commit style** for messages (e.g. `feat:`, `fix:`, `docs:`, `refactor:`).

## 5. Commit & PR expectations

- Clear, descriptive commit messages explaining *why*, not just *what*.
- PRs must pass CI (lint, type-check, tests) once CI exists.
- Significant architectural changes require an explanation of alternatives and risks, and
  should be recorded as an ADR (see `docs/MISSING_INFORMATION.md §6`).

## 6. Code of Conduct

Be respectful and constructive. A formal `CODE_OF_CONDUCT.md` will be added before public
release (tracked in `docs/MISSING_INFORMATION.md`). Until then, the
[Contributor Covenant](https://www.contributor-covenant.org/) applies in spirit.

## 7. License

By contributing, you agree that your contributions are licensed under the project's
**Apache-2.0** license.
