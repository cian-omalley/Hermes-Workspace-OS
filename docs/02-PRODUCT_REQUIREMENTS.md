# 02 — Product Requirements

This document defines all user-facing functionality. Requirements use **MoSCoW**
priority (Must / Should / Could / Won't-yet) and reference the milestone that delivers
them.

## 1. Personas

| Persona | Needs |
|---------|-------|
| **Builder (solo)** | Manage projects, code, research, and docs in one place; AI help. |
| **Team lead** | Track tasks/roadmaps, assign work, see repo & research activity. |
| **Contributor** | Pick up tasks, read docs/wiki, search, upload files. |
| **Researcher** | Ingest PDFs/links, get summaries, build a knowledge base, ask questions. |
| **Operator/Admin** | Self-host, manage users/roles, secrets, backups, audit logs. |

## 2. Core objects

Hermes manages these first-class entities (schema in `05-DATABASE_DESIGN`):

Workspace · Team · User · Project · Task · Document · Research item · Repository ·
Asset (file/image/video) · Diagram · Idea · Meeting · Decision · Agent · Knowledge
node · Automation/Workflow.

## 3. Global capabilities

### 3.1 Universal Search *(Must — M7)*
- One search box covering Notion, GitHub, files, PDFs, documentation, research, and
  conversations.
- Hybrid **semantic + keyword** search with source facets and filters.
- Permission-aware; every result is clickable to its source and cites provenance.

### 3.2 AI Assistant *(Must — M9/M10)*
- Conversational assistant grounded in the workspace via GraphRAG.
- Can invoke tools (search, create task, analyze repo, generate doc, draw diagram).
- Scoped to the user's permissions; every action is auditable.

### 3.3 Quick Actions *(Must — M10)*
From the dashboard, one click to: **Create Project · Research Topic · Analyze
Repository · Upload Files · Generate Documentation · Create Diagram · Create Mind Map ·
Generate Image · Brainstorm Idea.**

### 3.4 Notifications & activity feed *(Should — M10/M11)*
- Per-project and global activity feeds (commits, PRs, task changes, ingests, agent
  runs). Configurable notifications via workflows.

## 4. Dashboard requirements *(Must — M10)*

The main dashboard contains: **Universal Search · AI Assistant · Current Projects ·
Project Status · Kanban · Roadmaps · Research Queue · GitHub Activity · Recent Files ·
Knowledge Graph · Quick Actions.** Layout and interaction detail in `15-UI_DESIGN`.

## 5. Project system *(Must — M2/M10)*

Every project **automatically** provisions these sub-workspaces:

Project Dashboard · Documentation · Research · Repository · DeepWiki · Tasks · Kanban ·
Roadmap · Architecture · Files · Images · Videos · Meetings · Decisions · AI Agents ·
Knowledge Graph · Timeline.

Requirements:
- **R-P1 (Must):** Creating a project scaffolds all sub-workspaces with sensible empty
  states.
- **R-P2 (Must):** Linking a repository auto-populates Repository, DeepWiki, and
  Architecture, and seeds Tasks from issues.
- **R-P3 (Should):** Creating a project spins up its default agent team (M9), which
  remains idle/ephemeral until invoked.
- **R-P4 (Must):** Everything in a project is indexed for search and the knowledge
  graph.

## 6. Project management *(Must — M2/M10)*
- Tasks with status, assignee, priority, labels, estimates, due dates, subtasks,
  dependencies, and links to code/docs/research.
- **Kanban** board (drag-and-drop), **Roadmap/Gantt** timeline, and list views.
- Bidirectional sync with **GitHub issues** (M5) and **Notion tasks** (M4).

## 7. Knowledge management *(Must — M8)*
- **Documents:** Markdown-based, versioned, linkable, with backlinks (Obsidian-style).
- **Knowledge graph:** entities and relationships across all content; visual explorer.
- **GraphRAG** question-answering with citations.
- **Mind maps & diagrams:** Mermaid + React Flow; AI-assisted generation.

## 8. Repository intelligence (DeepWiki) *(Must — M5/M9)*
- Automatic repo analysis → architecture overview, module docs, dependency map,
  generated wiki.
- Commit and PR analysis with summaries; wiki auto-updates on change.
- "Ask this repo" grounded Q&A.

## 9. Research engine *(Must — M6/M9)*
- Add research by URL, file, or topic; agent gathers, summarizes, and files it.
- **Research Queue** of pending/active items on the dashboard.
- Outputs land as Research items linked to projects and the knowledge graph.

## 10. File intelligence *(Must — M6)*
On upload, the system **automatically**: identifies type → extracts content → analyzes
→ summarizes → tags → detects related projects → stores embeddings → updates the
knowledge graph → creates documentation → updates Notion. Supported: PDF, DOCX, ZIP,
images, videos, repositories, Markdown (extensible via plugins).

## 11. AI agent orchestration *(Must — M9)*
- Create dynamic agents; **no unnecessary always-on agents.**
- Default project agent team: **Project Manager, Research, Documentation, Developer,
  Code Review, Testing, Release.**
- Agents communicate, share memory, use tools, update tasks, and produce artifacts.
- Full lifecycle, permission, and memory model in `10-AGENT_SYSTEM`.

## 12. Automation engine *(Must — M11)*
- Visual workflows via **n8n** plus native event triggers (file uploaded, PR opened,
  task completed, schedule, …).
- Templates: auto-document on repo change, weekly research digest, release-note
  generation.

## 13. Documentation generator *(Should — M9)*
- Generate docs from code, files, research, or prompts (MkDocs-Material style output).
- Publishable static docs site per project.

## 14. Visual knowledge hub *(Should — M10)*
- Central place for diagrams, mind maps, architecture charts, and generated images.
- ECharts analytics; React Flow graphs; Mermaid diagrams.

## 15. Integrations *(Must — M4/M5)*
- **Notion:** two-way sync of 10 databases (see `07`). Non-authoritative.
- **GitHub:** repos, commits, issues, PRs (see `08`).
- Extensible via the Integration plugin interface (`06`) — Slack, Google Drive, etc.

## 16. Security & administration *(Must — M3/M12)*
- Authentication (Auth.js / Authentik OIDC).
- Authorization: workspace/project RBAC, resource-level checks.
- Secrets management + encrypted API-key vault.
- Audit logs for all sensitive actions.
- Backups & restore; data export.
- Per-workspace configuration of providers and integrations.

## 17. Non-functional requirements

| Category | Requirement |
|----------|-------------|
| **Self-hostability** | Full stack via `docker compose up`; no mandatory external SaaS. |
| **Performance** | Search P95 < 500 ms on 100k items; dashboard first paint < 2 s. |
| **Scalability** | Horizontal scaling of API/workers; async ingestion via queues. |
| **Reliability** | Idempotent sync; retriable jobs; graceful degradation if an integration is down. |
| **Security** | Encryption at rest for secrets; least-privilege agent tools; audit trail. |
| **Extensibility** | New provider added without touching core (plugin contract). |
| **Observability** | Structured logs, metrics, traces (M12). |
| **Accessibility** | WCAG 2.1 AA for the web UI. |
| **Portability** | Full data export; no proprietary lock-in. |

## 18. Acceptance themes (per milestone)

Each milestone's exit criteria in `00-ROADMAP` are the concrete acceptance tests for
the requirements above. The headline user journeys we must eventually satisfy:

1. **Repo → workspace:** Link a repo → wiki, diagrams, tasks, agents, search — in
   minutes.
2. **File → knowledge:** Upload a PDF → summary, tags, embeddings, graph, docs, Notion
   mirror — automatically.
3. **Ask anything:** One search/assistant query answers across all sources with
   citations.
4. **Resilience:** Turn off Notion → everything still works.
