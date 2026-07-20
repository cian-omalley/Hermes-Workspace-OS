# Glossary

## Purpose
Define the shared vocabulary of Hermes so docs, code, and conversations use terms
consistently. Ambiguous terms cause architectural drift; this is the reference.

## Current State
Terms are drawn from the design docs. Extend this list as implementation introduces new
concepts.

## Core terms

| Term | Definition |
|------|------------|
| **Workspace** | Top-level tenant boundary; owns projects, users, settings, and provider config. |
| **Project** | A unit of work that auto-provisions sub-workspaces (docs, tasks, repo, wiki, agents, graph, timeline, …). |
| **Source of record** | The authoritative data store. In Hermes this is **PostgreSQL** — never an external tool. |
| **Interface / surface** | A replaceable front-end over Hermes data (web app, Notion, GitHub, API). |
| **Derived store** | A projection rebuildable from the source of record: Neo4j (graph), Qdrant (vectors), Meilisearch (keyword). |
| **Plugin / adapter** | A concrete implementation of a port (AI, storage, search, integration, extractor). |
| **Port** | A stable interface the core depends on (ports & adapters / hexagonal). |
| **Integration** | A plugin that syncs Hermes with an external tool (Notion, GitHub, …). |
| **Ingestion** | The pipeline that turns uploaded/synced files into structured, searchable, connected knowledge. |
| **Extractor** | A plugin that extracts text/metadata/derivatives from a file type (PDF, DOCX, image, repo, …). |
| **Embedding** | A vector representation of a content chunk, stored in Qdrant for semantic search. |
| **Chunk** | A slice of content sized for embedding; one chunk → one vector point. |
| **Knowledge Graph (KG)** | The Neo4j property graph of entities and relationships across all content. |
| **GraphRAG** | Retrieval combining vector search (Qdrant) with graph traversal (Neo4j) for grounded answers. |
| **Agent** | An ephemeral, tool-using AI worker (LangGraph) with a role, permissions, memory, and tools. |
| **Agent run** | A single bounded execution of an agent toward a goal, producing artifacts and traces. |
| **Artifact** | A concrete output of an agent run (document, diagram, code change, report). |
| **Orchestrator** | The component that schedules and supervises agent runs / multi-agent teams. |
| **Tool** | A typed, permission-gated capability an agent can call (search, KG, GitHub, files, …), optionally via MCP. |
| **MCP** | Model Context Protocol — a standard interface for exposing tools/resources to models. |
| **Event bus** | Redis Streams transport for domain events; consumers project into search, graph, integrations, workflows. |
| **Outbox** | A Postgres table making domain write + event emission transactionally consistent. |
| **DeepWiki** | Auto-generated, living repository documentation (architecture, module docs, diagrams, "ask this repo"). |
| **Workflow** | An automation (native rule or n8n flow) triggered by events/schedules to perform actions. |
| **RBAC** | Role-based access control (workspace/project roles + resource checks). |
| **Secret vault** | The encrypted store for provider API keys and credentials. |
| **Audit log** | Append-only record of sensitive actions (by users, agents, integrations, system). |
| **Milestone / gate** | A shippable increment with entry/exit criteria; approval is required between milestones. |
| **Decision Required** | A marker for an unresolved decision; tracked in `docs/MISSING_INFORMATION.md`. |

## Architecture Decisions
Naming conventions favor domain language (Project, Task, Document, Asset, Agent) that maps
1:1 across the database (`docs/05`), the API, the knowledge graph, and the UI to minimize
translation layers.

## Alternatives Considered
Generic terms like "item" or "object" were avoided in favor of specific entity names to
keep the model legible.

## Future Improvements
Add domain-specific terms as agent templates and integrations expand; consider generating
part of this glossary from the code's domain model once it exists.

## Implementation Notes
Entity names here should match SQLAlchemy models, Pydantic schemas, KG node labels, and TS
types. Divergence is a smell — keep them aligned.
