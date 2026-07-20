# User Stories

## Purpose
Capture requirements as user-centric stories so implementation stays anchored to real
value and acceptance is testable.

## Current State
Stories are defined here to guide implementation; none are delivered yet (Milestone 0).
Format: *As a [persona], I want [capability], so that [outcome].* Each has acceptance
criteria and a target milestone.

## Personas
Builder (solo) · Team lead · Contributor · Researcher · Operator/Admin
(see `docs/02 §1`).

## Stories

### Projects & tasks
- **US-1 (M2/M10) — Builder:** *create a project and immediately get docs, tasks, repo,
  wiki, and agent slots,* so I can start working without manual setup.
  - *Accept:* creating a project provisions all sub-workspaces with helpful empty states.
- **US-2 (M2/M10) — Team lead:** *manage tasks on a kanban board and a roadmap,* so I can
  track and plan work.
  - *Accept:* drag-to-change-status persists, emits events, and syncs to GitHub/Notion.

### Repository intelligence
- **US-3 (M5/M9) — Builder:** *link a GitHub repo and get an auto-generated DeepWiki,
  architecture diagrams, and seeded tasks,* so I understand and plan a codebase fast.
  - *Accept:* linking a repo produces wiki pages with citations + tasks from issues.
- **US-4 (M9) — Contributor:** *ask questions about a repository and get grounded answers
  with citations,* so I can onboard quickly.
  - *Accept:* "ask this repo" cites real files/lines.

### Files & research
- **US-5 (M6) — Researcher:** *upload a PDF and automatically get a summary, tags,
  embeddings, graph links, and a doc,* so my knowledge base builds itself.
  - *Accept:* upload → asset becomes `ready` with all outputs; mirrored to Notion.
- **US-6 (M6/M9) — Researcher:** *add a research topic and have an agent gather and
  summarize sources,* so I save hours of manual searching.
  - *Accept:* a research item appears with cited summary, linked to the project.

### Search & assistant
- **US-7 (M7) — Any user:** *search once across code, docs, research, files, and
  conversations,* so I never hunt across tools.
  - *Accept:* one query returns fused, permission-scoped, source-faceted results.
- **US-8 (M9/M10) — Any user:** *ask the assistant a question about my workspace and get a
  cited answer,* so I get answers, not just links.
  - *Accept:* GraphRAG answer with citations; mutating actions require confirmation.

### Agents
- **US-9 (M9) — Builder:** *have a team of specialized agents (PM, dev, review, docs, …)
  collaborate on a goal and produce artifacts,* so routine work is automated.
  - *Accept:* a goal triggers a multi-agent run that updates tasks and yields artifacts;
    agents are ephemeral (no idle compute).

### Platform & admin
- **US-10 (M3) — Admin:** *control who can access what via roles,* so data stays secure.
  - *Accept:* role checks enforced at API and resource level; actions audited.
- **US-11 (M4) — Admin:** *disconnect Notion and keep working,* so I'm never locked in.
  - *Accept:* full core test suite passes with Notion disabled.
- **US-12 (M12) — Operator:** *self-host the whole stack with one command and back it up,*
  so I own my deployment.
  - *Accept:* `docker compose up` yields a healthy stack; backup/restore verified.

## Architecture Decisions
Stories map to milestone exit criteria, keeping product intent and engineering acceptance
in one line of sight.

## Alternatives Considered
Pure technical tasks without user framing were rejected — stories keep the "why" visible
and prevent building infrastructure with no user payoff.

## Future Improvements
Expand with team-collaboration, notification, and marketplace stories as those areas mature.

## Implementation Notes
Use these IDs (US-n) in issues/PRs. A story is "done" only when its acceptance criteria
have automated coverage.
