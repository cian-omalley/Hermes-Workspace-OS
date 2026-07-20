# Mission

## Purpose
Translate the long-term vision into a concrete, present-tense statement of what Hermes
does for its users and how it earns its place.

## Current State
Documented intent only; no software yet (Milestone 0). This mission guides sequencing and
scope decisions in the roadmap.

## Mission statement
> **Give individuals and teams a single, self-hosted, AI-native workspace that
> understands their projects, code, documents, and research — and keeps that knowledge
> open, connected, and theirs.**

Concretely, Hermes:
- **Unifies** fragmented tools (tracker, docs, wiki, files, research, automation) into one
  workspace.
- **Understands** content via ingestion, embeddings, and a knowledge graph.
- **Acts** through ephemeral, tool-using AI agents that produce real artifacts.
- **Owns** the data in an open, portable store — no lock-in.

## Architecture Decisions
- The mission mandates **data ownership** (source-of-record DB) and **openness**
  (Apache-2.0, self-host) as non-negotiable product properties, not features.
- **Modularity** is a mission requirement: each capability must be independently useful
  and replaceable so the platform can grow for years.

## Alternatives Considered
- **"AI assistant bolted onto a note app"** — too shallow; fails the "understands and
  acts" mission.
- **"Dev-tool only" (repo intelligence)** — too narrow; misses the unify-all-knowledge
  goal. Repo intelligence is one pillar, not the whole.

## Future Improvements
- Team and organization features (shared workspaces, roles, governance) deepen over time.
- Domain-specific packs (research lab, software team, consultancy) as agent/template
  bundles.

## Implementation Notes
Mission success is measured by the headline journeys in
`01_Product/User_Workflows.md`: repo→workspace in minutes, file→knowledge automatically,
ask-anything with citations, and resilience when integrations are off.
