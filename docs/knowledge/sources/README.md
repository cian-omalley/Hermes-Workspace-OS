# Sources — MRZ Hermes Knowledge Stack

A curated, indexed library of the tools, repositories, and references that inform the
Hermes vision. This is **reference material** — external projects and links — not part of
the Hermes Workspace OS codebase.

> **Provenance:** compiled from the NotebookLM notebook *"MRZ Hermes Knowledge Stack"* on
> **2026-07-21**. Links are reproduced as provided. Descriptions are brief functional
> summaries; some are inferred from each tool's layer in the stack and are **not
> independently verified**. Source files (PDFs, exports, etc.) will be added alongside
> this index in follow-up commits.

## How this folder is organized

Sources are grouped by **functional layer** in the architecture. Each layer has its own
catalog file with a table of tools (links, role, and status).

| # | Layer | Catalog | Focus |
|---|-------|---------|-------|
| 1 | Workspace & Agent Orchestration | [`01-workspace-and-agent-orchestration.md`](./01-workspace-and-agent-orchestration.md) | The AI workspace + agent runtime |
| 2 | Knowledge Browser & PKM | [`02-knowledge-browser-and-pkm.md`](./02-knowledge-browser-and-pkm.md) | Markdown editors, note-taking, wikis |
| 3 | Search, Retrieval & Graph | [`03-search-retrieval-and-graph.md`](./03-search-retrieval-and-graph.md) | Local search, vectors, knowledge graphs |
| 4 | Source Ingestion & Conversion | [`04-source-ingestion-and-conversion.md`](./04-source-ingestion-and-conversion.md) | Parsing, conversion, media, transcription |
| 5 | Memory, Context & Metadata | [`05-memory-context-and-metadata.md`](./05-memory-context-and-metadata.md) | Agent memory, context compression, local DBs |
| 6 | Skills, Agent Ideas & References | [`06-skills-agent-ideas-and-references.md`](./06-skills-agent-ideas-and-references.md) | Skill catalogs and agent-pattern collections |
| 7 | UI/Design & Security References | [`07-ui-design-and-security-references.md`](./07-ui-design-and-security-references.md) | Frontend/design bookmarks, OSINT/security |
| 8 | Utilities & Disabled/Skipped Tools | [`08-utilities-and-disabled-tools.md`](./08-utilities-and-disabled-tools.md) | Core utilities + deliberately deferred tools |

## Status legend

- **Active** — part of the stack.
- **Optional** — an alternative or add-on.
- **Reference** — a link/collection consulted for ideas, not a running tool.
- **Deferred** — explicitly "do not add yet."

## Relationship to Hermes Workspace OS

Several of these projects overlap conceptually with what Hermes Workspace OS builds
(knowledge management, agents, search, ingestion). They are kept here as prior art and
inspiration; the platform's own design lives in
[`../../PROJECT_BIBLE`](../../PROJECT_BIBLE) and the numbered specs in [`../../`](../../).
