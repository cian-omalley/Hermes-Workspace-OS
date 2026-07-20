# Search System

## Purpose
Define universal, permission-aware search across all content. Canonical spec:
`docs/12-SEARCH_SYSTEM.md`.

## Current State
Designed; unimplemented (M7). Combines **Meilisearch** (keyword) and **Qdrant** (semantic),
optionally enriched by **Neo4j** (GraphRAG).

## Retrieval modes
| Mode | Engine | Strength |
|------|--------|----------|
| Keyword/full-text | Meilisearch | Exact terms, typo tolerance, filters, speed. |
| Semantic | Qdrant | Meaning-based recall. |
| Relational | Neo4j | Structurally related context (answers). |

## Pipeline
Parse/route → keyword search → semantic search (same filters incl. `acl`) → **RRF fusion**
→ optional rerank → permission re-check → assemble (facets, highlights, provenance).

Indexing is event-driven and idempotent; indices are rebuildable projections of Postgres +
MinIO.

## Coverage
Notion-synced content, GitHub (code/issues/PRs), files/PDFs, documentation, research,
conversations — with source facets and filters.

## Architecture Decisions
1. **Hybrid by default** via Reciprocal Rank Fusion (no cross-engine score calibration).
2. **Permission-aware at two layers:** index-level `acl` filter + post-fusion re-check.
3. **Graceful degradation:** if one engine is down, return the other's results (flagged).
4. **Reranking optional** (AI-plugin cross-encoder/LLM) for top-N precision.

## Alternatives Considered
- **Single-engine (keyword OR vector)** — rejected: each alone misses cases the other
  catches.
- **Elasticsearch hybrid** — heavier to self-host; Meilisearch + Qdrant chosen for DX and
  footprint.
- **Weighted score blending** — rejected in favor of RRF's robustness to disparate scales.

## Future Improvements
Learned ranking from click/feedback signals, query understanding (intent/filters), saved
searches, and personalized boosts — all behind the search module's interface.

## Implementation Notes
- Chunk long content; keep both document- and chunk-level records for precise highlighting.
- Target hybrid P95 < 500 ms @ 100k items — benchmark early; treat as a hypothesis.
- Cache per `(query, filters, acl)` with short TTL.
- Agent searches use the agent's scoped permissions (`Agent_System.md`).
