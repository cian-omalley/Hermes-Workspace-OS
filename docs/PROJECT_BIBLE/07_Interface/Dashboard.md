# Dashboard

## Purpose
Specify the main dashboard and the project workspace — the primary surfaces users live in.
Canonical spec: `docs/15-UI_DESIGN.md`.

## Current State
Designed; unimplemented (M10).

## Main dashboard widgets
A responsive, rearrangeable grid:
Universal Search · AI Assistant · Current Projects · Project Status · Kanban · Roadmaps ·
Research Queue · GitHub Activity · Recent Files · Knowledge Graph · Quick Actions.

### Quick Actions
Create Project · Research Topic · Analyze Repository · Upload Files · Generate
Documentation · Create Diagram · Create Mind Map · Generate Image · Brainstorm Idea. Each
opens a focused flow and, where relevant, launches an agent run with visible progress.

## Project workspace tabs
Dashboard · Documentation · Research · Repository · DeepWiki · Tasks · Kanban · Roadmap ·
Architecture · Files/Images/Videos · Meetings · Decisions · AI Agents · Knowledge Graph ·
Timeline — all auto-provisioned per `docs/02 §5`.

## Key interactions
- **Kanban:** drag to change status → optimistic update → API → event → Notion/GitHub sync.
- **Roadmap:** draggable milestone bars linked to tasks; zoomable timeline.
- **Graph explorer:** click to expand neighbors; filter by type/tag/time; deep-link to
  entities.
- **Search:** grouped by source with facets; "Ask" toggles a GraphRAG cited answer.

## Architecture Decisions
1. **Widget grid over fixed layout** — users prioritize what matters to them.
2. **Quick Actions are agent entry points** — the dashboard is where humans hand work to AI.
3. **Consistent primitives** across dashboard and project views (`UX_Principles.md`).

## Alternatives Considered
- **Fixed, non-configurable dashboard** — rejected: different users value different signals.
- **Separate apps per capability** — rejected: contradicts the "one workspace" vision.

## Future Improvements
Saved dashboard presets per role, more widget types (metrics, alerts), drag-and-drop
customization, and embeddable widgets.

## Implementation Notes
- Widgets fetch via TanStack Query with realtime invalidation; show empty/loading/error
  states.
- Build the shell + Current Projects + Kanban + Search first, then layer in graph/analytics.
- Wire Quick Actions to their flows/agents as those systems land (search M7, agents M9).
