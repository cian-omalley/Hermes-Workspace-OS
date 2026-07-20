# Goals

## Purpose
Define the measurable objectives that determine whether Hermes is succeeding, across
product, engineering, and community dimensions.

## Current State
Goals are set; none are yet measurable in software (Milestone 0). Performance/quality
targets are **hypotheses to validate** during implementation, not proven results.

## Product goals
1. **One workspace** for projects, code, docs, research, files, knowledge, and agents.
2. **Repo → workspace in minutes:** link a repo and get a DeepWiki, diagrams, seeded
   tasks, and an agent team.
3. **File → knowledge automatically:** upload → summary, tags, embeddings, graph links,
   docs, Notion mirror — no manual filing.
4. **Ask anything:** one query answers across all sources with citations.
5. **Resilience:** disconnect any integration (esp. Notion) and Hermes still works.

## Engineering goals
- **Type-safe, tested, modular** codebase with clean architecture.
- **Plugin seams** for AI, storage, search, and integrations (swap with a config change).
- **Rebuildable derived stores** from the Postgres source of record.
- **One-command self-host** via Docker Compose.

## Measurable targets (to validate)
| Target | Metric | Source |
|--------|--------|--------|
| Search latency | Hybrid P95 < 500 ms @ 100k items | `docs/12` |
| Dashboard responsiveness | First paint < 2 s | `docs/02` |
| Ingestion correctness | PDF upload → summary+tags+embeddings+graph+doc | `docs/13` |
| Resilience | Full core test suite passes with Notion disconnected | `docs/07` |
| Provider swap | New provider passes port conformance suite with no core change | `docs/06` |

## Architecture Decisions
Goals directly drive architecture: the resilience goal forces the source-of-record
design; the "ask anything" goal forces hybrid search + GraphRAG; the swap goal forces the
plugin architecture.

## Alternatives Considered
- **Vanity goals (feature count)** — rejected in favor of journey- and quality-based
  goals that reflect real user value.

## Future Improvements
Add adoption/community goals (contributors, plugins, deployments) and reliability SLOs
once the system is running (post-M10).

## Implementation Notes
Each milestone's exit criteria (`09_Implementation/Milestones.md`) are the concrete,
testable checkpoints toward these goals. Targets become CI/benchmark gates as the
relevant systems land (search benchmarks at M7, resilience test at M4).
