# User Workflows

## Purpose
Describe the end-to-end journeys that define the product experience. These are the
integration tests of the vision — if they work, Hermes works.

## Current State
Workflows are designed, not implemented. Each becomes an e2e test as its milestones land.

## Headline workflows

### W1 — Repo → Workspace (minutes)
```mermaid
flowchart LR
    A[Link GitHub repo] --> B[Backfill: files, commits, issues, PRs]
    B --> C[DeepWiki analysis]
    C --> D[Architecture diagrams + module docs]
    B --> E[Seed tasks from issues]
    C --> F[Index for search + KG]
    F --> G[Agent team ready]
```
*Value:* a new codebase becomes an understandable, planned, searchable workspace almost
immediately. *Milestones:* M5 (sync), M8 (KG), M9 (agents/DeepWiki).

### W2 — File → Knowledge (automatic)
```mermaid
flowchart LR
    A[Upload PDF/DOCX/image/zip] --> B[Detect type + extract]
    B --> C[Summary + tags]
    B --> D[Chunk + embed -> Qdrant]
    C --> E[Entities -> Neo4j]
    C --> F[Generated doc]
    F --> G[Mirror to Notion]
```
*Value:* zero manual filing; every file becomes connected knowledge. *Milestone:* M6.

### W3 — Ask Anything (cited)
```mermaid
flowchart LR
    A[Query in search / assistant] --> B[Vector + keyword retrieval]
    B --> C[Graph traversal - GraphRAG]
    C --> D[Synthesized answer + citations]
```
*Value:* answers across code, docs, research, files, conversations. *Milestones:* M7, M8.

### W4 — Plan & Execute with Agents
```mermaid
flowchart LR
    A[State a goal] --> B[PM agent decomposes into tasks]
    B --> C[Developer/Docs/Research agents act]
    C --> D[Code Review + Testing agents verify]
    D --> E[Artifacts + task updates + release notes]
```
*Value:* routine work automated by an ephemeral agent team. *Milestone:* M9.

### W5 — Resilience (disconnect Notion)
```mermaid
flowchart LR
    A[Disable Notion integration] --> B[Core CRUD unaffected]
    B --> C[Queued syncs pause + retry]
    C --> D[Reconnect -> reconcile via sync_state]
```
*Value:* no lock-in; the product's defining guarantee. *Milestone:* M4 (tested).

## Supporting workflows
- **Research a topic** (W2-adjacent): topic → research agent → cited research items.
- **Generate documentation**: source → Documentation agent → published docs (MkDocs).
- **Automate on events**: event (PR merged, file ingested) → workflow → actions (M11).

## Architecture Decisions
Workflows are cross-cutting; they exercise multiple modules and datastores, validating the
event-driven design and the source-of-record/derived-store split.

## Alternatives Considered
Documenting only screen-level flows was rejected — the platform's value is in these
cross-system journeys, so they are first-class.

## Future Improvements
Add collaboration workflows (assign, review, comment), scheduled digests, and
domain-specific journeys (research lab, software team) as templates.

## Implementation Notes
Implement each workflow as a Playwright/e2e test (`08_Development/Testing_Strategy.md`).
W5 is the highest-priority resilience test and gates Milestone 4.
