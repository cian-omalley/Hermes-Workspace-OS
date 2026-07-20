# Prompt System

## Purpose
Define how prompts are authored, versioned, composed, and grounded across Hermes so AI
behavior is consistent, testable, and maintainable.

## Current State
Designed conceptually; unimplemented. No prompts exist yet. This establishes the approach
before the first prompt is written (M6/M9).

## Principles
- **Prompts are code artifacts:** versioned, reviewed, and tested — not scattered string
  literals.
- **Composable:** a shared system layer (identity, safety, output format) + task-specific
  templates + retrieved context (GraphRAG) + user input.
- **Grounded:** user-facing generation includes retrieved, cited context; the model is
  instructed to answer only from provided evidence where accuracy matters.
- **Structured output:** prefer typed/structured outputs (JSON schemas / tool calls) over
  free text when the result is consumed programmatically.

## Structure
```
[system: role + constraints + safety]
[context: GraphRAG-retrieved evidence with citations]
[task: template with variables]
[input: user/goal]
-> structured or cited response
```

## Prompt catalog (planned)
Ingestion (summary, tags, entity extraction), DeepWiki (architecture synthesis, module
docs), search (rerank, answer synthesis), and per-agent-role prompts (PM planning, code
review, testing, release notes) — see `Agent_Templates.md`.

## Architecture Decisions
1. **Centralized, versioned prompt templates** (a prompt module) rather than inline strings.
2. **Retrieval-grounded prompts** with explicit citation requirements.
3. **Structured outputs via tool/function calling** for machine-consumed results.
4. **Model-aware rendering** (respect provider capabilities/context limits).

## Alternatives Considered
- **Inline ad-hoc prompts** — rejected: unmaintainable, untestable, drift-prone.
- **A heavy prompt-management SaaS** — rejected: keep it in-repo and open-source.
- **Free-text outputs everywhere** — rejected where results are parsed downstream.

## Future Improvements
Prompt evaluation/regression tests (`Evaluation_System.md`), A/B prompt variants, prompt
templates as plugins, and locale/tone configuration.

## Implementation Notes
- Store templates in a versioned module; parameterize with typed inputs.
- Keep a safety/system layer applied to all prompts (no secret leakage, scope adherence).
- Test prompts against fixtures; treat prompt changes like code changes (review + CI).
- **Decision Required:** prompt template format/tooling (plain templates vs a library).
