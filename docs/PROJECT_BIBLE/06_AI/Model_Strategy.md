# Model Strategy

## Purpose
Define how Hermes selects, configures, and manages AI models (chat + embeddings) across
providers, balancing quality, cost, privacy, and self-hostability.

## Current State
Designed; unimplemented. Defaults are **Decision Required** (D1, D5 in
`docs/MISSING_INFORMATION.md`).

## Selection model
- **Configurable per scope** with precedence: run → agent → project → workspace → global
  default (`docs/06 §4`).
- **Chat and embeddings configured independently** (mix providers freely).
- **Local vs hosted:** Ollama for privacy/cost-free; hosted (OpenAI/Anthropic/Gemini) for
  peak quality.

## Guidance (proposed defaults — to confirm)
| Use | Proposed default | Rationale |
|-----|------------------|-----------|
| Embeddings | Local `nomic-embed-text` (Ollama) | Self-host-first, free, private; hosted opt-in. |
| Reasoning/agents | Configurable; a strong hosted model recommended | Agent reliability benefits from top models. |
| Summaries/tags (ingestion) | Mid-tier model | Cost-efficient at volume. |
| Rerank (optional) | Cross-encoder or LLM rerank | Precision on top-N only. |

> These are proposals, not commitments — finalize in `.env.example` at M1/M6.

## Cost & performance controls
- Model **routing** (easy tasks → cheap models), **caching** of repeated calls, **budgets**
  per agent run (tokens/cost/time), and **batching** of embeddings.

## Architecture Decisions
1. **No hardcoded model** — all selection is config-driven via the plugin registry.
2. **Embedding model is a load-bearing choice** — it fixes vector dims; changing it forces a
   re-embed (tracked via `embedding_refs.model`).
3. **Self-host-first defaults** with hosted opt-in.

## Alternatives Considered
- **One fixed frontier model everywhere** — simplest but costly and lock-in; rejected.
- **Only local models** — great for privacy but limits quality for hard agent tasks;
  rejected as a hard rule (offer as a mode).

## Future Improvements
Automatic model routing based on task difficulty/cost, a model performance leaderboard from
the evaluation system, quantized local models, and per-workspace spend caps/alerts.

## Implementation Notes
- Persist chosen models in workspace settings; expose safe overrides per agent.
- Validate a selected provider supports required capabilities (e.g. tools) before use.
- Record model + version on every embedding and agent run for reproducibility/migration.
