# Vision

## Purpose
Establish the long-term "north star" for Hermes Workspace OS so every decision can be
checked against a shared intent.

## Current State
The vision is fully articulated in `docs/01-VISION.md`. This Bible entry is the canonical
summary. **Nothing is implemented yet** — the project is at Milestone 0 (documentation).

## The vision
**Hermes Workspace OS is a self-hostable operating system for knowledge work.** It sits
*above* your existing tools and *owns the meaning* of your work — projects, code,
documents, research, files, ideas, and the relationships between them — while exposing
that meaning through familiar interfaces (Notion, a web dashboard) and autonomous AI
agents.

It unifies the strongest ideas from Notion (workspace), GitBook (docs), DeepWiki (repo
intelligence), Obsidian (knowledge graph), GitHub (dev workflows), Linear (tracking), n8n
(automation), and LangGraph/OpenHands (agents) — as **one modular, open-source system**.

## Architecture Decisions
- **Hermes owns the data.** Its PostgreSQL database is the source of record; every
  external tool is a replaceable *interface*. Test of correctness: disconnect Notion and
  Hermes still works completely.
- **Open-source first & self-hostable.** The whole stack runs on your own infrastructure;
  no mandatory SaaS.
- **AI-native, not AI-bolted-on.** Agents, embeddings, and the knowledge graph are core
  primitives.

## Alternatives Considered
- **Build on top of Notion's API as the DB** — rejected: vendor lock-in, no unified
  queryable/embeddable store, breaks if Notion changes.
- **A single-store design (Postgres only)** — deferred: relational + graph + vector +
  keyword each serve a distinct retrieval need; a single store would compromise the
  knowledge/search experience that defines the product.
- **Closed-source SaaS product** — rejected: contradicts the self-host, data-ownership,
  and extensibility goals.

## Future Improvements
- Native real-time collaborative editing (initially delegated to interfaces like Notion).
- Mobile-native clients (responsive web first).
- A marketplace of community plugins (AI providers, integrations, agent templates).
- Federation between Hermes instances.

## Implementation Notes
The vision is realized incrementally via the 12-milestone roadmap
(`09_Implementation/Development_Phases.md`). The knowledge graph compounds in value over
time — the longer Hermes runs, the more it understands the user's work, which is the
strategic moat.
