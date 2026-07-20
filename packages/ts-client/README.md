# @hermes/ts-client

The **generated TypeScript client** for the Hermes Workspace OS API — the frontend/backend
**contract seam** (see `docs/PROJECT_BIBLE/04_Integrations/API_Design.md`).

- `openapi.json` — the API's OpenAPI document, dumped from FastAPI (`scripts/dump_openapi.py`).
- `src/schema.d.ts` — TypeScript types generated from `openapi.json` by `openapi-typescript`.
- `src/index.ts` — a thin, fully-typed client built on `openapi-fetch`.

Both `openapi.json` and `schema.d.ts` are committed, and CI regenerates them and fails on
any diff — so the client can never silently drift from the API.

## Regenerate
```bash
just gen-client        # dump OpenAPI (from the API) + regenerate schema.d.ts
```

## Usage
```ts
import { createHermesClient } from "@hermes/ts-client";

const api = createHermesClient({ baseUrl: "http://localhost:8000" });
const { data, error } = await api.GET("/api/v1/workspaces");
```
