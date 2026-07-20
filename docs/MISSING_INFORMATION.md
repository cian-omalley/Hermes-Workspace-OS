# Missing Information & Open Decisions

This document consolidates everything that is **unknown, undecided, or not yet built**.
It is the companion to `AUDIT_REPORT.md`. Items here are referenced throughout the
Project Bible as **"Decision Required."** Keep this file current — resolved items move to
a decision record (`PROJECT_BIBLE/02_Architecture/*` or a future ADR log) and are struck
through here.

Priority: 🔴 blocks implementation · 🟠 needed soon · 🟢 nice-to-have / later.

---

## 1. Missing decisions

| # | Decision | Prio | Why it matters | Options |
|---|----------|------|----------------|---------|
| D1 | **Default embedding model** | 🔴 | Determines Qdrant vector dims, quality, cost, and whether ingestion works offline. Changing it later forces a re-embed of all content. | (a) Local `nomic-embed-text` via Ollama (free, private, self-host-first); (b) OpenAI `text-embedding-3`; (c) configurable with a local default. **Rec:** (c) local default, hosted opt-in. |
| D2 | **Neo4j edition / graph store** | 🟠 | Community vs Enterprise affects clustering, licensing, and RBAC. | Neo4j Community (default); or swap for a lighter graph via the Graph plugin. **Rec:** Community for self-host; keep plugin seam. |
| D3 | **Canonical repo name casing** | 🟢 | `Hermes-Workspace-OS` vs `hermes-workspace-os` appears inconsistently. | Pick one (lowercase-kebab is conventional for repos). **Rec:** `hermes-workspace-os`. |
| D4 | **Docs consolidation** | 🟠 | Numbered specs (`docs/00-15`) and the Project Bible overlap. | (a) Keep both, cross-linked; (b) fold specs into Bible. **Rec:** keep both until Milestone 2, then re-evaluate. |
| D5 | **Primary AI provider default** | 🟠 | Sets out-of-box behavior and cost for agents/assistant. | Anthropic / OpenAI / Gemini / local. Pluggable per workspace regardless. **Rec:** configurable; document a sane default in `.env.example`. |
| D6 | **AuthN default for solo self-host** | 🟠 | Authentik (OIDC) is heavy for a single user. | Auth.js credentials/email for solo; Authentik optional for teams. **Rec:** Auth.js default, Authentik opt-in. |
| D7 | **Chunking strategy & sizes** | 🟠 | Affects retrieval quality and token cost across search/RAG/DeepWiki. | Fixed-size w/ overlap vs semantic/structural chunking per content type. **Rec:** structural per type (code by symbol, prose by section), tunable. |
| D8 | **Monorepo tooling specifics** | 🟢 | `uv` + `pnpm` chosen; task runner (`just`) and Nx/Turbo not finalized. | Plain pnpm workspaces vs Turborepo/Nx. **Rec:** start plain, add Turbo if build times demand it. |
| D9 | **Multi-tenancy isolation level** | 🟠 | Single Postgres with `workspace_id` scoping vs Postgres RLS vs per-tenant schemas. | Row scoping (simplest) → add RLS for hard isolation. **Rec:** `workspace_id` scoping + optional RLS. |
| ~~D10~~ | ~~**`main` base branch**~~ ✅ **RESOLVED** | — | Resolved 2026-07-20: `main` created from the foundation commit; work now PRs into it. | — |

## 2. Missing documentation

- **`.env.example`** — the authoritative list of required config/secrets (ships M1).
- **`CODE_OF_CONDUCT.md`** — OSS norm (add alongside CONTRIBUTING).
- **`SECURITY.md`** — vulnerability disclosure process (add before public release).
- **ADR log** — a lightweight Architecture Decision Record folder to capture D-series
  decisions as they resolve (recommended: `docs/PROJECT_BIBLE/02_Architecture/adr/`).
- **API reference** — auto-generated OpenAPI docs (exists only once the API is built, M2).
- **Runbooks** — backup/restore, incident, upgrade (M12).

## 3. Missing features (all planned; none built)

Everything from Milestone 1 onward is unbuilt. The load-bearing gaps, in dependency
order: monorepo/CI (M1) → domain model & API (M2) → auth & secrets (M3) → Notion (M4) →
GitHub (M5) → ingestion (M6) → search (M7) → knowledge graph (M8) → agents (M9) →
dashboard (M10) → automation (M11) → deployment hardening (M12). See
`PROJECT_BIBLE/09_Implementation/Development_Phases.md`.

## 4. Technical risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Scope vs capacity** | Very large surface (10+ subsystems) risks stalling. | Strict milestone sequencing + approval gates; ship vertical slices. |
| **Unvalidated performance targets** | Search P95 <500ms, dashboard <2s are asserted, not proven. | Benchmark early (M7); treat targets as hypotheses. |
| **Six datastores to operate** | Operational complexity for self-hosters. | Compose defaults, health checks, backups; allow trimming via plugins. |
| **Doc/code drift** | Design becomes fiction if code diverges. | Claude Code rules require updating Bible "Current State" each milestone. |
| **Provider/API churn** | LLM & integration APIs change. | Plugin seams isolate providers; conformance tests per port. |
| **Data consistency across stores** | Derived stores can drift from Postgres. | Transactional outbox + rebuildable projections + reconciliation jobs. |

## 5. Security concerns

- **No controls implemented yet** — the security *design* (RBAC, encrypted vault, audit,
  signed webhooks, agent least-privilege) exists only on paper until M3.
- **Secret handling** — envelope encryption + KMS/`age` key management must be built and
  reviewed; never store provider keys in plaintext or in `metadata`.
- **Agent blast radius** — autonomous, tool-using agents need enforced permission scopes,
  sandboxed code execution, and human-approval gates for mutating/external actions.
- **Untrusted ingestion input** — files/webhooks are hostile input; need sandboxing,
  size/type guards, archive-bomb protection, signature verification.
- **Supply chain** — pin dependencies, enable secret scanning, add `SECURITY.md` and
  dependency review in CI.
- **No secrets currently committed** — verified (only `.gitignore` guards `.env`).

## 6. Recommended improvements

1. **Establish `main`**, then proceed to Milestone 1 (runnable skeleton + CI + `.env.example`).
2. **Add an ADR log** and record D1–D10 as they resolve.
3. **Stand up the OpenAPI→TS contract early** to prevent frontend/backend drift.
4. **Benchmark retrieval and ingestion** on realistic data before over-optimizing.
5. **Introduce a `docker compose` "lite" profile** so self-hosters can run a reduced
   store set for evaluation.
6. **Add CODE_OF_CONDUCT.md and SECURITY.md** before any public release.
7. **Keep the "no empty scaffolding" discipline** — create folders only with real code.

---

### Change log for this file
- 2026-07-20: Created during the repository intelligence pass (audit of commit `ff45a54`).
