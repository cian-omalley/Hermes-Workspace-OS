# Design System

## Purpose
Define the visual and component language so the UI is consistent, themeable, accessible,
and efficient to build.

## Current State
Chosen approach (Tailwind + shadcn/ui) documented; no components built yet (M10).

## Foundations
- **Tokens:** color, spacing, typography, radius, shadow defined as Tailwind theme tokens;
  light/dark via CSS variables.
- **Components:** shadcn/ui primitives (owned in-repo, not a black-box dependency) — dialogs,
  menus, tables, forms, tabs, toasts, command palette.
- **Shared library:** reusable components live in a `packages` UI package for use across the
  app.
- **Icons:** a single icon set (e.g. Lucide) for consistency.

## Visualization language
| Need | Component | Conventions |
|------|-----------|-------------|
| Node graphs | React Flow | Nodes colored by entity type; labeled edges; expandable. |
| Diagrams | Mermaid | Editable source; live re-render. |
| Analytics | ECharts | Consistent palette; theme-aware. |

## Accessibility & theming
- WCAG 2.1 AA contrast in both themes; ARIA on custom widgets; visible focus states;
  keyboard operability throughout. Checked with axe in CI.

## Architecture Decisions
1. **Own the components (shadcn/ui)** for full control over design and a11y.
2. **Token-driven theming** so light/dark and future themes are a config change.
3. **One shared UI package** to prevent divergent component copies.

## Alternatives Considered
- **Full component libraries (MUI/AntD/Chakra)** — rejected: heavier, less control, harder
  to theme to a distinct identity.
- **Bespoke design system from scratch** — rejected: shadcn/ui + Tailwind is the pragmatic,
  maintainable middle ground.

## Future Improvements
A documented component gallery (Storybook), design tokens exported for docs/marketing,
additional themes, and density options.

## Implementation Notes
- Establish tokens + core primitives before building feature UI.
- Keep entity-type → color mapping centralized (used by graph, badges, cards).
- Enforce a11y and visual consistency via lint rules and review.
- Reuse the same palette across ECharts, React Flow, and badges for a coherent look.
