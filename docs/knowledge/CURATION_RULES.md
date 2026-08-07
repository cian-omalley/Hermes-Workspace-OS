# Knowledge Curation Rules

The standing process for handling **any** new file, link, or note that enters the project.
Executed by the **Knowledge Curator** agent (`.claude/agents/knowledge-curator.md`), and by
any session doing curation. This is a **rule from now on**, referenced by `CLAUDE.md`.

## The rule (short form)
> Every incoming document or link is **filed** into the knowledge hub and **rewritten**
> into an AI-friendly, memorizable form. Nothing is left loose; nothing is destroyed.

## 1. Where things go

| Incoming item | Destination |
|---------------|-------------|
| External tool/link/reference | `docs/knowledge/sources/` (add to the right layer catalog + link) |
| Uploaded document (PDF/DOCX/MD/notes) | `docs/knowledge/sources/files/<slug>/` (original + an AI-friendly `.md` rewrite) |
| Project design/decision content | the relevant `docs/PROJECT_BIBLE/` section (do **not** duplicate into the hub — index it) |
| Anything else worth remembering | `docs/knowledge/` with an entry in `README.md` |

**Never** move or flatten the Project Bible or numbered specs — index and link them from
`docs/knowledge/README.md` instead (their paths are load-bearing for `CLAUDE.md`).

## 2. The AI-friendly rewrite format
When rewriting a source into `.md`, use this shape (front-loaded for fast AI ingestion):

```markdown
---
title: <human title>
source: <original URL or file path>
type: <web | pdf | doc | video | note | repo>
captured: <YYYY-MM-DD>
tags: [<topic>, <topic>]
status: <active | optional | reference | deferred>
---

# <title>

**TL;DR:** <1–3 sentences: what it is and why it matters here.>

## Key points
- <short, declarative facts — one idea per line>
- <define any term the first time it appears>

## How it relates to Hermes
- <where/how this informs the platform, if at all>

## Details
<only what's worth keeping; summarize, don't transcribe. Preserve exact commands, APIs,
or figures verbatim in code blocks.>

## Links
- <original> · <docs> · <repo>
```

### Rewrite principles (optimize for AI memory)
1. **Front-load** the TL;DR and key points; put detail last.
2. **Short declarative lines**, one fact each; prefer bullets/tables over paragraphs.
3. **Define terms** on first use; keep a consistent vocabulary (`00_Overview/Glossary.md`).
4. **Deduplicate** — if a fact already lives in the Bible/specs, link to it, don't restate.
5. **Preserve verbatim** anything that must be exact (commands, code, API shapes, numbers).
6. **Metadata header** on every file (title/source/type/captured/tags/status).
7. **Cite provenance**; never fabricate. Mark unknowns as "unverified" rather than guessing.
8. Keep each rewrite **self-contained and short** (aim < ~300 lines).

## 3. Always update the indexes
After filing/rewriting:
- Add/adjust the entry in `docs/knowledge/README.md`.
- For external tools, update the correct `sources/0X-*.md` catalog (Tool · Role · Links ·
  Status).
- If it changes project state, update `AI_PRIMER.md` and the Bible "Current State".

## 4. Safety
- Read a file fully before rewriting or relocating it.
- Fetch links read-only; respect the environment's network egress limits (some hosts are
  blocked). Record blocked/private links as reference-only entries.
- Do not commit secrets. Never publish/mirror content that shouldn't leave the repo.
