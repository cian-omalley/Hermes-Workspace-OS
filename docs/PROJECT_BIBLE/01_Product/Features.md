# Features

## Purpose
Provide a single, honest feature inventory with implementation status, so no one
overestimates what exists.

## Current State
Documentation is complete and the **Milestone 1 platform skeleton exists** (runnable
services, tooling, CI). All *product* features remain `Planned` (they begin at Milestone
2). Status legend: ✅ Done · 🟡 Partial · ⏳ Planned.

Platform skeleton (M1): API/worker/web health services, monorepo tooling, compose stack,
and CI are **🟡 In progress** (see `09_Implementation/Current_Status.md`).

## Feature inventory

### Global
| Feature | Status | Milestone |
|---------|--------|-----------|
| Universal hybrid search | ⏳ | M7 |
| Grounded AI assistant | ⏳ | M9/M10 |
| Quick actions launcher | ⏳ | M10 |
| Activity feed & notifications | ⏳ | M10/M11 |

### Projects
| Feature | Status | Milestone |
|---------|--------|-----------|
| Project CRUD + auto-provisioned sub-workspaces | ⏳ | M2/M10 |
| Tasks, subtasks, dependencies | ⏳ | M2 |
| Kanban board (drag-and-drop) | ⏳ | M10 |
| Roadmap / timeline | ⏳ | M10 |
| Decisions (ADR) & meetings | ⏳ | M2/M10 |

### Knowledge
| Feature | Status | Milestone |
|---------|--------|-----------|
| Versioned Markdown documents + backlinks | ⏳ | M2/M8 |
| Knowledge graph explorer | ⏳ | M8/M10 |
| GraphRAG Q&A with citations | ⏳ | M8 |
| Diagrams & mind maps (Mermaid/React Flow) | ⏳ | M10 |

### Repository intelligence
| Feature | Status | Milestone |
|---------|--------|-----------|
| Repo linking & sync | ⏳ | M5 |
| Commit / PR / issue analysis | ⏳ | M5 |
| DeepWiki generation | ⏳ | M5/M9 |
| "Ask this repo" | ⏳ | M9 |

### Files & research
| Feature | Status | Milestone |
|---------|--------|-----------|
| Upload + automatic ingestion pipeline | ⏳ | M6 |
| Extractors (PDF/DOCX/MD/image/video/zip/repo) | ⏳ | M6 |
| Research queue + agent research | ⏳ | M6/M9 |

### AI agents
| Feature | Status | Milestone |
|---------|--------|-----------|
| Ephemeral agent lifecycle | ⏳ | M9 |
| Default project agent team | ⏳ | M9 |
| Agent memory, tools, permissions, comms | ⏳ | M9 |

### Integrations & automation
| Feature | Status | Milestone |
|---------|--------|-----------|
| Notion two-way sync (10 DBs) | ⏳ | M4 |
| GitHub integration | ⏳ | M5 |
| n8n workflows + native triggers | ⏳ | M11 |

### Platform
| Feature | Status | Milestone |
|---------|--------|-----------|
| Auth (Auth.js/Authentik) + RBAC | ⏳ | M3 |
| Encrypted secret vault + audit log | ⏳ | M3 |
| Backups & deployment hardening | ⏳ | M12 |

## Architecture Decisions
Features are grouped to match service/module boundaries
(`02_Architecture/Service_Architecture.md`) so a feature maps cleanly to an owning module.

## Alternatives Considered
Presenting features without status was rejected — honest status tracking is essential to
avoid the "docs imply it exists" trap flagged in the audit.

## Future Improvements
Add community/enterprise features (marketplace, federation, SSO policy, mobile) after the
core journeys are delivered.

## Implementation Notes
Update the status column in the same PR that implements a feature. `09_Implementation/
Current_Status.md` is the roll-up view of this table.
