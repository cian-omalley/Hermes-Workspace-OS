# Memory System

## Purpose
Define how agents and the workspace retain and retrieve context over time — the substrate
that makes agents coherent across runs and enables long-term learning.

## Current State
Designed as part of the agent system (`docs/10 §4`); unimplemented (M9). Backed by the
`agent_memory` table plus embeddings in Qdrant.

## Memory tiers
| Tier | Scope | Lifetime | Store |
|------|-------|----------|-------|
| **Working** | Current run | Ephemeral | LangGraph state (checkpointed) |
| **Short-term** | Agent/project, recent | Time-boxed (`expires_at`) | `agent_memory` |
| **Long-term** | Durable facts/preferences/learnings | Persistent | `agent_memory` + embedding ref |
| **Shared (blackboard)** | Project team | Project lifetime | Project memory scope |

## Retrieval
- **Semantic recall:** long-term memories are embedded (`embedding_ref_id`) and retrieved
  by similarity to the current goal/context.
- **Importance & eviction:** each memory has an importance score governing retention;
  low-value/expired memories are pruned.
- **Sharing:** agents on a project read the shared scope (PM plan, decisions, glossary) for
  coordination without tight coupling.

## Architecture Decisions
1. **Tiered memory** mirrors proven cognitive-architecture patterns and keeps context
   windows focused (only relevant memory is retrieved).
2. **Memory is workspace-scoped and permissioned** like all other data — no cross-tenant
   bleed.
3. **Embeddings reuse the same Qdrant infrastructure** as search, avoiding a parallel store.

## Alternatives Considered
- **Single flat memory log** — rejected: unbounded context, poor relevance, cost.
- **A dedicated memory database** — rejected: `agent_memory` + Qdrant already suffice;
  revisit only if scale demands.
- **No long-term memory** — rejected: agents would relearn context every run.

## Future Improvements
Reflection/summarization to compress episodic memory into semantic memory; memory sharing
across projects (with permission); user-visible memory inspection/editing; forgetting
policies tuned by evaluation.

## Implementation Notes
- Keep working memory in LangGraph checkpoints; persist only what has lasting value to
  `agent_memory`.
- Tag memories with `scope`, `importance`, and provenance (originating run).
- Retrieval must respect the agent's permission scope (`Agent_System.md`).
- **Decision Required:** default retention windows and importance thresholds
  (`docs/MISSING_INFORMATION.md`, relates to D7).
