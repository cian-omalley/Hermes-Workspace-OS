# Changelog

All notable changes to Hermes Workspace OS are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Until the
first release, changes are tracked under **Unreleased** and grouped by milestone.

## [Unreleased]

### Added — Repository Intelligence & Documentation Pass (2026-07-20)
- `CLAUDE.md` — entry point and operating rules pointer for Claude Code sessions.
- `CONTRIBUTING.md` — contribution guidelines.
- `CHANGELOG.md` — this file.
- `docs/AUDIT_REPORT.md` — full repository audit of commit `ff45a54`.
- `docs/PROJECT_MAP.md` — single-page orientation to the repo and system.
- `docs/MISSING_INFORMATION.md` — consolidated open decisions, gaps, and risks.
- `docs/PROJECT_BIBLE/` — complete Claude Code Project Bible (11 sections, 50+ documents)
  as the permanent source of truth: Overview, Product, Architecture, Core Systems,
  Integrations, Data, AI, Interface, Development, Implementation, and Claude Code rules.

### Notes
- **Non-destructive pass:** no files were deleted or moved — the existing tree contained
  no empty, duplicate, or deprecated files. Intended code directories were intentionally
  **not** scaffolded (to honor the "no empty folders" rule); they are documented in
  `docs/PROJECT_MAP.md` and created when real code lands.

### Added — Milestone 0: Engineering Foundation (commit `ff45a54`)
- 16 design specifications in `docs/` (`00-ROADMAP` … `15-UI_DESIGN`).
- `README.md`, Apache-2.0 `LICENSE`, `.gitignore`.
- Core architectural decision documented: Hermes' database is the source of record;
  Notion/GitHub are replaceable interfaces.

---

## Milestone tracking

| Milestone | Status | Summary |
|-----------|--------|---------|
| M0 — Engineering Foundation | ✅ Complete | Design docs + Project Bible + repo scaffolding |
| M1 — Project Foundation | ⏳ Planned | Monorepo, tooling, compose stack, CI |
| M2 — Database & API | ⏳ Planned | Domain model + FastAPI CRUD |
| M3 — Authentication | ⏳ Planned | Auth, RBAC, secrets, audit |
| M4 — Notion Integration | ⏳ Planned | Two-way sync; disconnect-safe |
| M5 — GitHub Integration | ⏳ Planned | Repo/commit/PR/issue sync |
| M6 — File Ingestion | ⏳ Planned | Automatic processing pipeline |
| M7 — Search System | ⏳ Planned | Hybrid semantic + keyword |
| M8 — Knowledge Graph | ⏳ Planned | Entities, relationships, GraphRAG |
| M9 — AI Agents | ⏳ Planned | LangGraph agent orchestration |
| M10 — Dashboard | ⏳ Planned | Web workspace |
| M11 — Automation | ⏳ Planned | n8n workflows |
| M12 — Deployment | ⏳ Planned | Production hardening |
