# 15 — UI Design

## 1. Principles

- **One workspace, many lenses.** A consistent shell (sidebar + command bar + content)
  frames every view; projects and the global dashboard share the same primitives.
- **AI everywhere, unobtrusive.** The assistant and universal search are always a
  keystroke away (`⌘K`), never in the way.
- **Fast & keyboard-first.** Linear-grade responsiveness; every primary action has a
  shortcut and a quick action.
- **Accessible & themeable.** WCAG 2.1 AA, light/dark, keyboard navigable, built on
  shadcn/ui + Tailwind.
- **Graph-native.** Relationships are first-class visuals (React Flow), diagrams are
  text-driven (Mermaid), analytics are rich (ECharts).

## 2. Application shell

```
┌───────────────────────────────────────────────────────────────┐
│  Top bar:  ⌘K Universal Search   |   AI Assistant   |  User    │
├──────────┬────────────────────────────────────────────────────┤
│ Sidebar  │  Content area (dashboard or project workspace)      │
│  Home    │                                                     │
│  Projects│   ── main panels ──                                 │
│  Search  │                                                     │
│  Research│                                                     │
│  Graph   │                                                     │
│  Files   │                                                     │
│  Agents  │                                                     │
│  Automate│                                                     │
│  Settings│                                                     │
└──────────┴────────────────────────────────────────────────────┘
```

- **Command bar (`⌘K`):** universal search + command palette (navigate, create, run
  quick actions, ask the assistant).
- **AI Assistant:** slide-over panel, context-aware (knows the current project/entity),
  can invoke tools and show its work/citations.

## 3. Main dashboard

The home dashboard is a responsive grid of widgets (rearrangeable):

| Widget | Content |
|--------|---------|
| **Universal Search** | Prominent search with source facets. |
| **AI Assistant** | Ask anything; grounded answers with citations. |
| **Current Projects** | Cards with status, progress, next milestone. |
| **Project Status** | Roll-up health across projects (ECharts). |
| **Kanban** | Cross-project or focused task board (drag-and-drop). |
| **Roadmaps** | Timeline/Gantt of milestones. |
| **Research Queue** | Pending/active research items. |
| **GitHub Activity** | Recent commits, PRs, issues across linked repos. |
| **Recent Files** | Latest ingested assets with summaries/tags. |
| **Knowledge Graph** | Mini graph explorer (React Flow) into the full view. |
| **Quick Actions** | The action launcher (below). |

### Quick Actions
One click / palette command each: **Create Project · Research Topic · Analyze Repository
· Upload Files · Generate Documentation · Create Diagram · Create Mind Map · Generate
Image · Brainstorm Idea.** Each opens a focused modal/flow and, where relevant, kicks off
an agent run and shows progress.

## 4. Project workspace

Selecting a project opens its workspace with tabbed sub-views (all auto-provisioned,
`02` §5):

| Tab | View |
|-----|------|
| **Dashboard** | Project overview: status, activity, key metrics, agents. |
| **Documentation** | Markdown docs with backlinks, versions, TOC. |
| **Research** | Research items + queue for this project. |
| **Repository** | Linked repo(s): files, commits, PRs, issues. |
| **DeepWiki** | Auto-generated wiki (`09`). |
| **Tasks** | List/table of tasks with filters. |
| **Kanban** | Drag-and-drop board. |
| **Roadmap** | Milestones timeline/Gantt. |
| **Architecture** | Diagrams + dependency map (Mermaid/React Flow). |
| **Files / Images / Videos** | Asset galleries with summaries & tags. |
| **Meetings** | Notes, transcripts, action items. |
| **Decisions** | ADR-style decision log. |
| **AI Agents** | The project's agent team, runs, artifacts. |
| **Knowledge Graph** | Project-scoped graph explorer. |
| **Timeline** | Chronological activity across everything. |

## 5. Key interaction patterns

- **Kanban:** columns per status; drag to change status (optimistic update → API →
  event → Notion/GitHub sync). Card shows assignee, priority, labels, linked PR/doc.
- **Roadmap:** draggable bars for milestones; links to tasks; zoomable timeline.
- **Graph explorer:** click a node to expand neighbors; filter by type/tag/time;
  double-click to open the entity. Backed by the Graph API (`11`).
- **Search results:** grouped by source with facets; inline previews; "Ask" toggles a
  GraphRAG synthesized answer with citations above raw hits.
- **Assistant actions:** when the assistant proposes a mutating/external action, it
  shows a confirm step (mirrors agent approval gates, `10`).

## 6. Visualization components

| Need | Library |
|------|---------|
| Node graphs (KG, workflows, mind maps) | **React Flow** |
| Diagrams (architecture, flow, sequence) | **Mermaid** |
| Analytics/charts (status, metrics, trends) | **Apache ECharts** |
| Primitives (dialogs, tables, menus, forms) | **shadcn/ui** |

Mind maps and diagrams support **AI generation** (Quick Actions) and manual editing;
Mermaid source is editable and re-renders live.

## 7. Realtime & feedback

- Live updates via SSE/WebSocket: task moves, new activity, agent progress, ingestion
  status, search-as-you-type.
- Optimistic UI with reconciliation; clear loading/empty/error states everywhere.
- Long-running actions (ingestion, agent runs, DeepWiki) show progress with links to the
  resulting artifacts.

## 8. Empty & onboarding states

- New workspace → guided setup (connect Notion/GitHub, pick AI/storage providers).
- New project → scaffolded sub-views with helpful empty states ("Link a repo to generate
  a DeepWiki", "Upload files to build knowledge").
- Quick Actions are surfaced prominently until the workspace has content.

## 9. Frontend architecture

- **Next.js App Router** with React Server Components for data-heavy pages; client
  components for interactive widgets.
- **State:** TanStack Query for server state (cache + realtime invalidation); local UI
  state kept minimal.
- **Types:** generated TypeScript client from the OpenAPI schema (`04`) — no drift.
- **Design system:** Tailwind + shadcn/ui tokens; dark/light themes; responsive grid;
  component library in `packages` for reuse.
- **Auth:** Auth.js session in the web app; API calls carry the verified token.

## 10. Accessibility & performance

- Keyboard navigation and focus management throughout; ARIA on custom widgets; sufficient
  contrast in both themes.
- Code-splitting, lazy-loaded heavy visualizations, virtualized long lists/boards.
- Targets: first paint < 2 s; interactions feel instant (optimistic + cached).

## 11. Testing (M10)

- Component tests (Vitest) for widgets; Playwright e2e for the headline journeys:
  create project → tasks/kanban → search → graph.
- Accessibility checks (axe) in CI.
- Visual/interaction checks for kanban drag, graph expand, search facets, quick actions.
