# Product Requirements

## Purpose
Define, at a governance level, what Hermes must do for users. This Bible entry summarizes
and stabilizes the detailed requirements in `docs/02-PRODUCT_REQUIREMENTS.md`.

## Current State
Requirements are fully specified in `docs/02`; **none are implemented** (Milestone 0). This
document is the durable index; the numbered spec holds the exhaustive MoSCoW list.

## Requirement areas (MoSCoW, milestone-tagged)

| Area | Priority | Milestone | Summary |
|------|----------|-----------|---------|
| Universal Search | Must | M7 | Hybrid semantic + keyword across all sources, permission-aware, cited. |
| AI Assistant | Must | M9/M10 | Grounded (GraphRAG) assistant that can call tools; scoped & audited. |
| Quick Actions | Must | M10 | One-click create project / research / analyze repo / upload / generate doc/diagram/mind map/image / brainstorm. |
| Project system | Must | M2/M10 | Projects auto-provision all sub-workspaces. |
| Project management | Must | M2/M10 | Tasks, kanban, roadmap; sync with GitHub/Notion. |
| Knowledge management | Must | M8 | Versioned docs, backlinks, KG, GraphRAG Q&A, diagrams/mind maps. |
| Repository intelligence | Must | M5/M9 | DeepWiki: analysis, docs, diagrams, "ask this repo". |
| Research engine | Must | M6/M9 | Add by URL/file/topic; agent gathers/summarizes/files. |
| File intelligence | Must | M6 | Automatic ingestion pipeline (10 steps). |
| Agent orchestration | Must | M9 | Dynamic, ephemeral agent teams. |
| Automation | Must | M11 | n8n workflows + native triggers. |
| Documentation generator | Should | M9 | Generate docs from code/files/research/prompts. |
| Visual knowledge hub | Should | M10 | Diagrams, mind maps, analytics. |
| Integrations | Must | M4/M5 | Notion (10 DBs) + GitHub; extensible. |
| Security & admin | Must | M3/M12 | Auth, RBAC, secrets, audit, backups. |

## Non-functional requirements
Self-hostability, performance (search P95 <500 ms, dashboard <2 s), horizontal
scalability, reliability/graceful degradation, security, extensibility, observability,
WCAG 2.1 AA accessibility, and full data portability. Detail in `docs/02 §17`.

## Architecture Decisions
- Requirements are **journey-anchored** (see `User_Workflows.md`) so implementation is
  validated by end-to-end value, not isolated features.
- "Must" items map to specific milestone exit criteria — no requirement is accepted
  without a testable definition of done.

## Alternatives Considered
- A flat feature backlog (rejected) — replaced by MoSCoW + milestone tagging to force
  sequencing and prevent building breadth before depth.

## Future Improvements
Add team/enterprise requirements (SSO policies, granular sharing, compliance/export) and
per-domain requirement packs after the core journeys ship.

## Implementation Notes
When implementing, trace each PR back to a requirement ID/area here and update the
relevant "Current State" section. Requirements that reveal open questions must be logged
in `docs/MISSING_INFORMATION.md`.
