# Knowledge System (Knowledge Graph & GraphRAG)

## Purpose
Define Hermes' model of meaning: the knowledge graph of entities/relationships and the
GraphRAG retrieval it powers. Canonical spec: `docs/11-KNOWLEDGE_GRAPH.md`.

## Current State
Designed; unimplemented (M8). Backed by **Neo4j** (derived projection of Postgres +
extraction).

## Entities & relationships
- **Domain nodes** mirror entities (Project, Task, Document, Repository, Commit, PR, Issue,
  Asset, Person, Agent, …).
- **Semantic nodes** discovered during ingestion: Concept, Topic, Technology.
- **Edges** are structural (from domain data) and semantic (from extraction), carrying
  weight/confidence, source, and timestamps.

## How it's built
- **Structural sync:** domain events upsert nodes/edges deterministically.
- **Semantic extraction:** during ingestion (`docs/13`), entities/concepts/technologies are
  extracted, resolved/deduplicated, and linked with confidence.
- **Bridge tables:** `graph_refs`/`relationships` in Postgres record what's synced,
  enabling incremental updates and full rebuilds.

## GraphRAG
Combine vector retrieval (Qdrant) with graph traversal (Neo4j): retrieve relevant chunks,
link them + the query to graph nodes, traverse to pull in structurally related context,
assemble/rank, then generate a cited answer. This is the retrieval backbone for the
assistant, agents, and "ask this repo."

## Architecture Decisions
1. **Property graph (Neo4j)** for expressive relationship queries via Cypher.
2. **Graph is a rebuildable projection**, never the source of record.
3. **Entity resolution** canonicalizes concepts (string + embedding similarity + synonym
   dictionary) to avoid duplicate nodes.
4. **Permission-aware queries** scoped by `workspace_id` and accessible projects.

## Alternatives Considered
- **Vector-only RAG** — rejected: misses structural/relational context that improves
  accuracy.
- **Relational graph in Postgres (recursive CTEs)** — workable for small graphs but less
  expressive/performant for deep traversal; Neo4j chosen, kept behind the Graph plugin.
- **Embedding everything without a graph** — rejected: loses explicit relationships and
  explainability.

## Future Improvements
Community detection/centrality for "important" nodes, temporal graph queries, graph-based
recommendations ("related work"), and learned relationship extraction.

## Implementation Notes
- Expose only safe, parameterized graph queries via the API (no raw Cypher from clients).
- Keep heavy text/bytes in Postgres/MinIO; Neo4j holds structure + lightweight props.
- Provide `rebuild-graph` to regenerate from Postgres + `relationships`.
- Visualization via React Flow (`07_Interface/*`).
