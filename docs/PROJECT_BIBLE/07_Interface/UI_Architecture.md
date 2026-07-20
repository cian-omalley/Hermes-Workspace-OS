# UI Architecture

## Purpose
Define the frontend's structure and technical approach. Canonical spec:
`docs/15-UI_DESIGN.md`.

## Current State
Designed; unimplemented (M10). No `apps/web` exists yet.

## Stack & structure
- **Next.js App Router** with React Server Components for data-heavy pages; client
  components for interactive widgets.
- **Server state:** TanStack Query (cache + realtime invalidation); minimal local UI state.
- **Types:** generated TS client from the OpenAPI schema — no drift with the backend.
- **Design system:** Tailwind + shadcn/ui tokens; light/dark themes; responsive grid;
  shared components in `packages`.
- **Auth:** Auth.js session; API calls carry the verified token.

## App shell
Sidebar (Home, Projects, Search, Research, Graph, Files, Agents, Automate, Settings) +
top bar (⌘K universal search, AI assistant, user) + content area (dashboard or project
workspace). See `Dashboard.md`.

## Visualization components
React Flow (graphs/workflows/mind maps), Mermaid (diagrams), ECharts (analytics), shadcn/ui
(primitives).

## Realtime
SSE/WebSocket for activity feeds, agent progress, ingestion status, and search-as-you-type;
optimistic UI with reconciliation.

## Architecture Decisions
1. **RSC for data, client components for interaction** — performance + interactivity.
2. **Generated client** as the single source of API types.
3. **Own the components (shadcn/ui)** rather than a black-box component library.
4. **Accessibility (WCAG 2.1 AA) is a requirement**, checked in CI (axe).

## Alternatives Considered
- **SPA (CRA/Vite) without SSR** — rejected: worse first paint/SEO for data-rich pages.
- **A component library like MUI/AntD** — rejected: less control over design; shadcn/ui
  gives owned, themeable primitives.
- **Hand-written API types** — rejected: drift risk.

## Future Improvements
Offline/PWA support, mobile-native clients (post-launch non-goal), collaborative editing,
and a plugin surface for custom dashboard widgets.

## Implementation Notes
- Code-split and lazy-load heavy visualizations; virtualize long lists/boards.
- Targets: first paint < 2 s; interactions feel instant (optimistic + cached).
- Keep UI logic thin over the API; no business rules in the frontend.
- Build the shell + one journey (project → tasks/kanban → search → graph) first (M10).
