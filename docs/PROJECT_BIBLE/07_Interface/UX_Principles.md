# UX Principles

## Purpose
Define the experience principles that keep Hermes coherent, fast, and humane despite its
broad feature surface.

## Current State
Principles established; no UI yet (M10). These guide every interface decision.

## Principles
1. **One workspace, many lenses.** A consistent shell frames every view; the dashboard and
   project workspaces share primitives so nothing feels bolted on.
2. **AI everywhere, unobtrusive.** Universal search and the assistant are a keystroke away
   (⌘K), never in the way; AI proposes, the user disposes.
3. **Fast & keyboard-first.** Linear-grade responsiveness; every primary action has a
   shortcut and a quick action.
4. **Show the work.** AI/agent actions are transparent — progress, artifacts, and citations
   are visible; mutating actions confirm first.
5. **Progressive disclosure.** Powerful capabilities without overwhelming — sensible empty
   states and onboarding guide new users.
6. **Accessible by default.** WCAG 2.1 AA, full keyboard navigation, light/dark, sufficient
   contrast.
7. **Trust through provenance.** Every answer/result links to its source; nothing is a black
   box.

## Architecture Decisions
- **Optimistic UI with reconciliation** for perceived speed.
- **Confirmation gates** mirror agent approval gates for mutating/external actions
  (`03_Core_Systems/Agent_System.md`).
- **Citations are first-class** in search and assistant outputs.

## Alternatives Considered
- **Maximal-density "power tool" UI** — rejected: intimidating; progressive disclosure
  preferred.
- **Hiding AI reasoning** — rejected: transparency builds trust and aids debugging.
- **Mouse-first design** — rejected: keyboard-first serves the target power users.

## Future Improvements
Personalization (layout, saved views), command-palette-driven everything, in-context AI
explanations, and accessibility beyond AA where feasible.

## Implementation Notes
- Every interactive widget: clear loading/empty/error states.
- Long-running actions (ingestion, agent runs, DeepWiki) show progress + link to results.
- Enforce accessibility in CI (axe) and manual keyboard passes.
- Keep the ⌘K command bar as the universal entry point (search + commands + assistant).
