# Third-Party Services

## Purpose
Detail the specifics of each third-party service Hermes integrates with: auth model, data
touched, permissions, and constraints. Complements `External_Services.md` (catalog) with
per-provider depth.

## Current State
Designed; unimplemented. Notion and GitHub are first (M4/M5); others are planned plugins.

## Notion (M4) — interface, not source of record
- **Auth:** OAuth / integration token, stored encrypted.
- **Data:** 10 mapped databases (see `docs/07`); hidden `hermes_id` binds pages to records.
- **Sync:** two-way; outbound via outbox events, inbound via webhooks/polling; conflict
  default *Hermes wins* (per-field configurable).
- **Constraints:** API rate limits (token-bucket + backoff); Markdown⇄blocks conversion for
  rich content; binaries stay in MinIO with links.
- **Guarantee:** disconnect-safe (tested).

## GitHub (M5) — code stays authoritative
- **Auth:** GitHub App (preferred, per-repo, webhooks) or PAT/OAuth; encrypted.
- **Data:** repos, commits, PRs, issues, files → `repositories`/`commits`/`pull_requests`/
  `issues`/`repo_files`; Issue↔Task and PR↔Task links.
- **Sync:** webhooks (`push`, `pull_request`, `issues`, `release`) + backfill +
  reconciliation; commit/PR analysis feeds ingestion/DeepWiki.
- **Constraints:** API quotas (backoff), signature-verified webhooks, least-privilege
  scopes, write only where explicitly enabled.

## AI providers (OpenAI / Anthropic / Gemini / Ollama)
- **Auth:** API keys in the encrypted vault (Ollama local, no key).
- **Use:** chat, embeddings, optional rerank/vision/STT — all behind the AI provider port.
- **Constraints:** per-provider capabilities (context, tools, modalities) detected via
  `capabilities()`; graceful degradation if unsupported.

## Authentik (optional, teams)
- **Role:** OIDC/SAML SSO identity provider; the API trusts a verified token.
- **Fallback:** Auth.js for solo self-host (D6).

## Planned (later plugins)
Slack (notifications), Google Drive (file inbound), possibly Jira/Linear (issue sync) —
each via the Integration port.

## Architecture Decisions
1. **Per-provider specifics live behind ports**, so core logic is provider-agnostic.
2. **Read-authoritative boundaries respected:** GitHub owns code; Notion is an interface.
3. **All credentials least-privilege + encrypted + rotatable + audited.**

## Alternatives Considered
- **Direct SDK usage sprinkled through core** — rejected: couples core to providers.
- **Single hardcoded AI provider** — rejected: contradicts the plugin principle and
  self-host/local goals.

## Future Improvements
A generic connector/OAuth framework to speed new integrations; provider health dashboards;
cost tracking per provider; a community provider registry with an allowlist.

## Implementation Notes
- Verify webhook signatures; record inbound events in `webhook_events` for idempotency.
- Store provider capabilities and chosen models per workspace settings (`docs/06 §5`).
- Never log secrets or pass raw secrets to models; adapters decrypt in-process only.
