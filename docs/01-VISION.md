# 01 — Vision

## The problem

Knowledge work is fragmented across a dozen tools. Projects live in Linear or Jira,
docs in Notion or GitBook, code in GitHub, research in browser tabs and PDFs, diagrams
in yet another app, and "AI" bolted onto each in isolation. Context is scattered, and
no single system understands how a repository, a research note, a task, and a decision
relate to one another.

The tools that try to unify this either **lock your data inside a SaaS silo** or stop
at note-taking. None of them are simultaneously: an operating system for knowledge
work, AI-native from the ground up, open-source, and self-hostable.

## The vision

**Hermes Workspace OS is a self-hostable operating system for knowledge work.** It is
the connective tissue that sits *above* your existing tools and *owns the meaning* of
your work — projects, code, documents, research, files, ideas, and the relationships
between them — while exposing that meaning through familiar interfaces and autonomous
AI agents.

Hermes lets one person, or a whole team, manage from a single workspace:

> Projects · Research · Code · Documentation · Files · Knowledge · AI Agents · Tasks ·
> Ideas · Images · Diagrams · Repositories · Teams

It combines, in one modular system, the strongest ideas from best-in-class tools:

| Inspiration | What Hermes takes from it |
|-------------|---------------------------|
| **Notion** | Flexible, human-friendly workspace & databases (as an *interface*) |
| **GitBook** | Beautiful, structured documentation |
| **DeepWiki** | Automatic repository intelligence and wikis |
| **Obsidian** | A linked knowledge graph of everything |
| **GitHub** | Development workflows, source of truth for code |
| **Linear** | Fast, opinionated project & issue tracking |
| **n8n** | Visual automation across everything |
| **OpenHands / LangGraph** | Autonomous, tool-using AI agents |

## The defining architectural decision

**Notion is the primary user interface. Notion is _not_ the database of record.**

Hermes stores the real data in its own database. Notion — and GitHub, and any other
surface — are **interchangeable interfaces** over that data. This matters because:

- **Durability:** Your knowledge outlives any vendor. If Notion changes pricing, its
  API, or disappears, Hermes keeps functioning with zero data loss.
- **Intelligence:** AI reasoning, search, and the knowledge graph require a unified,
  queryable, embeddable store — not scattered across third-party APIs.
- **Portability:** Because interfaces are plugins, you can swap Notion for another
  front-end (or use several at once) without re-platforming.

**Test of correctness:** *Disconnect Notion, and Hermes must still work completely.*
This is a first-class, tested requirement (Milestone 4 exit criteria).

## Principles

1. **Hermes owns the data.** Every external tool is a replaceable surface, never the
   source of record.
2. **Open-source first.** Integrate mature, well-supported projects instead of
   reinventing them. Contribute back where possible.
3. **Everything is a plugin.** AI providers, storage, search, and integrations all sit
   behind stable interfaces and are swappable at runtime/config.
4. **Modular services.** Each capability (search, agents, ingestion, KG, …) is an
   independently developed, tested, and deployable module.
5. **Self-hostable by default.** The entire stack runs on your own infrastructure via
   Docker Compose. No mandatory cloud dependency.
6. **AI-native, not AI-bolted-on.** Agents, embeddings, and the knowledge graph are
   core primitives, not add-ons.
7. **Professional engineering.** Type safety, tests, clean architecture, documentation,
   and reproducible builds are requirements, not aspirations.

## Who it is for

- **Solo builders & researchers** who want a private "second brain + build system" that
  actually understands their code and documents.
- **Small teams** who want Linear + Notion + a wiki + automation without stitching five
  SaaS bills together or leaking data.
- **Organizations with data-residency needs** who must self-host and audit everything.
- **Open-source communities** who want a hackable, extensible workspace platform.

## What success looks like

- A user connects a GitHub repo and, within minutes, has an auto-generated DeepWiki,
  architecture diagrams, a task board seeded from issues, and an agent team ready to
  work — all searchable and linked in a knowledge graph.
- Uploading a PDF automatically produces a summary, tags, embeddings, graph
  relationships, documentation, and a Notion mirror — with no manual filing.
- A single search box answers questions across code, docs, research, files, and
  conversations, with citations.
- The whole thing runs on one server, is fully open-source, and keeps working when any
  external integration is turned off.

## Non-goals (initially)

- Not a general-purpose SaaS competitor with hosted billing — Hermes is
  self-host-first.
- Not a replacement for GitHub as the *code* source of truth — Hermes indexes and
  augments it.
- Not a real-time collaborative rich-text editor at launch — collaboration flows
  through interfaces like Notion first; native collab editing is a later evolution.
- Not a mobile-native app at launch — responsive web first.

## Long-term horizon

Hermes is designed to grow for years: a stable plugin contract, a versioned data model,
and modular services mean new AI providers, storage backends, interfaces, and agent
capabilities can be added without rewrites. The knowledge graph compounds in value over
time — the longer Hermes runs, the more it understands your work.
