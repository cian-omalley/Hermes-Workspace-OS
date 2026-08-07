"""External integrations (Milestone 4+).

Integrations are replaceable interfaces over Hermes' source-of-record database. Notion is
the first; all sync is idempotent and conflict-aware, and the core keeps working when an
integration is disconnected. See ``docs/07-NOTION_INTEGRATION.md``.
"""
