# Non-Goals

## Purpose
Explicitly bound the project. Non-goals prevent scope creep and clarify what Hermes will
*not* try to be — especially important given the platform's broad ambition.

## Current State
Non-goals are declared; they shape roadmap sequencing. Some are "not yet," not "never."

## Non-goals (initial)
1. **Not a hosted SaaS with billing.** Hermes is self-host-first; a managed offering is
   out of scope for the core project.
2. **Not a replacement for GitHub as the code source of truth.** Hermes indexes and
   augments repositories; Git/GitHub remain authoritative for code.
3. **Not a real-time collaborative rich-text editor at launch.** Collaborative editing is
   delegated to interfaces (e.g. Notion) initially; native collab is a later evolution.
4. **Not mobile-native at launch.** Responsive web first.
5. **Not a general-purpose LLM chat product.** The assistant is grounded in the workspace
   (GraphRAG), not an open-domain chatbot.
6. **Not a reinvention of mature tools.** Hermes integrates n8n, Neo4j, Qdrant,
   Meilisearch, MinIO, etc. rather than rebuilding them.
7. **Not always-on autonomous agents.** Agents are ephemeral and purpose-scoped; no idle
   agent compute.

## Architecture Decisions
- The "don't reinvent" non-goal is enforced by the **plugin architecture**: integrate
  behind an interface instead of rebuilding.
- The "not always-on agents" non-goal is enforced by the **ephemeral agent lifecycle**
  (`03_Core_Systems/Agent_System.md`).

## Alternatives Considered
- **Making Notion authoritative** — rejected (contradicts the vision; see Vision.md).
- **Shipping everything at once** — rejected in favor of milestone gates.

## Future Improvements (non-goals that may become goals later)
- Native real-time collaboration.
- Mobile apps.
- Optional managed/hosted deployment for non-technical users.

## Implementation Notes
When a proposed change conflicts with a non-goal, it must be raised explicitly (and, if
adopted, the non-goal updated here with rationale). Claude Code sessions should treat
non-goals as guardrails (`10_Claude_Code/Instructions.md`).
