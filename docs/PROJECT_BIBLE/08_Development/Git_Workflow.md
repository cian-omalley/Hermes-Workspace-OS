# Git Workflow

## Purpose
Define how changes flow from idea to merged code so history stays clean and releases are
traceable.

## Current State
The repository has a single commit and currently **no `main` base branch** — the session
branch is also the default (**Decision Required D10:** establish `main`). This workflow
applies from Milestone 1.

## Branching model
- **`main`** — always releasable; protected (once created).
- **Feature branches:** `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `refactor/<slug>`,
  `chore/<slug>`.
- **Short-lived branches;** rebase or squash-merge to keep history linear.
- **One logical change per PR;** prefer vertical slices.

## Commits
- **Conventional Commits:** `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`,
  `build:`, `ci:`.
- Messages explain **why**, not just what; reference issue/story IDs (US-n) where relevant.

## Pull requests
- Use the PR template; describe **what changed, why, alternatives, risks**.
- **CI must be green** (lint, type-check, tests) before merge.
- Update affected docs — including the relevant Bible **Current State** — in the same PR.
- Significant architectural changes require an explanation and (once adopted) an ADR entry.

## Releases
- **SemVer;** maintain `CHANGELOG.md` (Keep a Changelog) under Unreleased → tagged release.
- Tag releases from `main`; release notes generated with help from the Release agent later.

## Architecture Decisions
1. **Trunk-based with short-lived branches** — simpler than long-lived release branches for
   this project size.
2. **Squash-merge default** — clean, linear history; PR captures detail.
3. **Docs-with-code rule** — prevents the design/code drift flagged in the audit.

## Alternatives Considered
- **Git Flow** — rejected: heavyweight for the team size.
- **Long-lived develop branch** — rejected: adds merge overhead without benefit here.

## Future Improvements
Branch protection rules, required reviews, CODEOWNERS, signed commits, and automated
release tagging.

## Implementation Notes
- **First action for M1:** create `main` from the foundation and set it as default +
  protected.
- Add `.github/` PR/issue templates and CI so the workflow is enforced, not just documented.
- Claude Code sessions follow their designated feature branch and never push to `main`
  without explicit permission (`10_Claude_Code/Instructions.md`).
