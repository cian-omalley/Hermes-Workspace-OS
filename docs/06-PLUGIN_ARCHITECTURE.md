# 06 — Plugin Architecture

**Principle:** *Everything replaceable is a plugin.* AI providers, storage backends,
search engines, and integrations sit behind stable interfaces. The core depends only on
the interface; concrete adapters are registered and selected by configuration.

This is the **ports & adapters (hexagonal)** pattern applied consistently across Hermes.

## 1. Goals

- Swap OpenAI ↔ Anthropic ↔ Gemini ↔ Ollama with a config change.
- Swap MinIO ↔ S3 ↔ local disk without touching business logic.
- Add a new integration (Slack, Jira, GDrive) without modifying core.
- Select providers **per workspace** (and, for AI, per agent/run).
- Ship built-in plugins in-tree; allow third-party plugins via entry points.

## 2. Categories of plugin (ports)

| Port | Interface | Built-in adapters |
|------|-----------|-------------------|
| **AI Provider** | chat, embeddings, (rerank) | OpenAI, Anthropic, Gemini, Ollama |
| **Storage Provider** | put/get/delete/presign | MinIO, S3, local FS |
| **Search Provider** | index/query (keyword) | Meilisearch |
| **Vector Provider** | upsert/search/delete | Qdrant |
| **Graph Provider** | upsert nodes/edges, query | Neo4j |
| **Integration** | connect, sync in/out, webhook | Notion, GitHub (Slack, GDrive later) |
| **Extractor** | can_handle, extract | PDF, DOCX, Markdown, image, ZIP, repo |
| **Auth Provider** | verify token, get identity | Auth.js/JWT, Authentik OIDC |
| **Automation Engine** | register/trigger workflow | n8n, native |

## 3. Interface contracts (illustrative)

Interfaces are defined with Python `Protocol`/ABCs in `packages/hermes-plugins`. Sketch:

```python
class AIProvider(Protocol):
    name: str
    async def chat(self, messages: list[Message], *, model: str,
                   tools: list[ToolSpec] | None = None,
                   stream: bool = False) -> ChatResult: ...
    async def embed(self, texts: list[str], *, model: str) -> list[list[float]]: ...
    def capabilities(self) -> ProviderCaps: ...   # models, max ctx, supports_tools...

class StorageProvider(Protocol):
    async def put(self, key: str, data: BinaryIO, *, content_type: str) -> StoredObject: ...
    async def get(self, key: str) -> BinaryIO: ...
    async def delete(self, key: str) -> None: ...
    async def presigned_url(self, key: str, *, expires: int) -> str: ...

class Extractor(Protocol):
    def can_handle(self, mime_type: str, filename: str) -> bool: ...
    async def extract(self, obj: StoredObject) -> ExtractionResult: ...  # text, meta, derivatives

class Integration(Protocol):
    provider: str
    async def connect(self, config: dict, secrets: SecretRef) -> ConnectionStatus: ...
    async def sync_out(self, change: DomainChange) -> SyncResult: ...
    async def sync_in(self, event: ExternalEvent) -> list[DomainChange]: ...
    def verify_webhook(self, headers: dict, body: bytes) -> bool: ...
```

Each interface has a matching set of typed DTOs and a documented error contract
(retryable vs. fatal), so the core handles failures uniformly.

## 4. Registry & selection

A central **plugin registry** discovers and instantiates adapters.

```python
registry.register(AIProvider, "openai", OpenAIProvider)
registry.register(StorageProvider, "minio", MinioProvider)
# ...

# resolution is config-driven, per workspace:
provider = registry.resolve(AIProvider, workspace.settings.ai.provider)
```

- **Discovery:** built-ins registered at startup; third-party plugins discovered via
  Python entry points (`hermes.plugins`) and an allowlist.
- **Selection precedence:** run-level override → agent config → project config →
  workspace config → global default.
- **Validation:** on registration, the registry checks the adapter implements the
  interface and declares `capabilities()`; incompatible selections fail fast with a
  clear error (e.g. choosing a provider that lacks tool support for a tool-using agent).

## 5. Configuration model

```yaml
# per-workspace settings (stored in workspaces.settings jsonb)
ai:
  chat:      { provider: anthropic, model: claude-sonnet-5 }
  embeddings:{ provider: ollama,    model: nomic-embed-text }
storage:  { provider: minio, bucket: hermes }
search:   { provider: meilisearch }
vector:   { provider: qdrant, collection: hermes_embeddings }
graph:    { provider: neo4j }
integrations:
  notion: { enabled: true }
  github: { enabled: true }
```

Secrets referenced here (API keys) are resolved from the encrypted **secret vault**
(`05` `secrets`, `03` security), never inlined.

## 6. Capabilities & feature detection

Adapters declare capabilities so the core can adapt:
- AI: `supports_tools`, `supports_streaming`, `max_context`, `embedding_dims`,
  `modalities`.
- Storage: `supports_presign`, `max_object_size`.
- Integration: `supports_webhooks`, `syncable_entities`.

Features gracefully degrade: e.g. if the selected AI provider can't stream, the
assistant falls back to non-streamed responses instead of erroring.

## 7. Lifecycle & isolation

- **Init/health:** each adapter exposes `health()`; startup and `/health` aggregate
  them. A failing optional provider degrades that feature, not the whole system.
- **Isolation:** third-party plugins run with restricted permissions and their own
  secret scope; a misbehaving integration cannot read another's secrets.
- **Versioning:** interfaces are versioned (`AIProvider@v1`); the registry records the
  interface version an adapter targets. Breaking interface changes bump the version and
  keep an adapter shim where feasible.

## 8. Testing contract

Every port ships a **conformance test suite** that any adapter must pass (a "provider
contract test"). This guarantees swapping providers is safe: a new Storage adapter runs
the same put/get/delete/presign suite; a new AI adapter runs chat/embed/capability
tests (with a recorded/mock backend). Built-in adapters run these in CI.

## 9. Extending Hermes with a new plugin (author flow)

1. Implement the relevant `Protocol` in a package exposing the `hermes.plugins` entry
   point.
2. Provide `capabilities()` and pass the port's conformance suite.
3. Declare required config + secret keys.
4. Register via entry point; enable in workspace settings.

No core code changes are required — this is the extensibility guarantee that keeps
Hermes maintainable for years.

## 10. Why this matters

The plugin layer is what makes Hermes an *operating system* rather than an app: the
core provides scheduling, data ownership, orchestration, and contracts, while the
"drivers" (providers/integrations) are swappable. It directly serves the vision — no
lock-in, open-source substitutability, and long-term evolvability.
