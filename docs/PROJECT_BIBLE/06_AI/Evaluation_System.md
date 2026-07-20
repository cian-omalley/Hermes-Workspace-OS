# Evaluation System

## Purpose
Define how Hermes measures the quality of its AI outputs — retrieval, generation, agents,
and ingestion — so improvements are evidence-based and regressions are caught.

## Current State
Designed conceptually; unimplemented. No evals exist yet. This establishes the intent early
so AI features ship with measurement, not vibes.

## What to evaluate
| Area | Metrics | Method |
|------|---------|--------|
| Search/retrieval | Precision@k, recall, MRR/nDCG | Golden query set with labeled relevant items. |
| GraphRAG answers | Faithfulness, answer relevance, citation correctness | Fixture Q&A + automated + LLM-as-judge checks. |
| Ingestion | Summary quality, tag accuracy, extraction correctness | Fixture files with expected outputs. |
| Agents | Task success rate, artifact quality, cost/latency, steps-to-done | Scenario runs on fixture projects. |
| DeepWiki | Grounding (claims cite real code), coverage | Fixture repos; no-orphan-claim checks. |

## Approach
- **Golden datasets** committed as fixtures (queries, files, repos, expected outputs).
- **Automated metrics** in CI where deterministic; **LLM-as-judge** for subjective quality
  (with human spot-checks).
- **Regression gates:** prompt/model/retrieval changes run the eval suite; significant
  regressions block merge.
- **Cost/latency budgets** tracked alongside quality.

## Architecture Decisions
1. **Ship AI features with evals** — treat prompts/retrieval like code with tests.
2. **Deterministic-first, judge-second** — prefer objective metrics; use LLM judging only
   where necessary, with human oversight.
3. **Fixtures in-repo** for reproducibility.

## Alternatives Considered
- **Manual/eyeball evaluation only** — rejected: not reproducible, hides regressions.
- **A third-party eval SaaS** — optional later; start with an in-repo harness (open-source
  first).

## Future Improvements
Continuous evaluation on real (anonymized/opt-in) usage, human feedback loops (thumbs
up/down feeding retrieval/prompt tuning), a model/prompt leaderboard, and drift detection.

## Implementation Notes
- Introduce the harness alongside the first AI feature (ingestion summaries, M6) and expand
  through M7–M9.
- Keep eval runs cheap enough for CI (sampled) with a fuller nightly run.
- **Decision Required:** eval framework choice and CI budget (`docs/MISSING_INFORMATION.md`).
