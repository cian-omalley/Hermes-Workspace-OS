// Hermes Workspace OS — typed API client.
//
// Thin wrapper around `openapi-fetch`, typed by the generated OpenAPI `paths`. This is
// the frontend/backend contract seam: `schema.d.ts` is generated from the API's OpenAPI
// document (see scripts/dump_openapi.py + `pnpm generate`), so types can never drift.

import createClient, { type Client } from "openapi-fetch";

import type { paths } from "./schema";

export type HermesClient = Client<paths>;

export interface HermesClientOptions {
  /** Base URL of the Hermes API, e.g. http://localhost:8000 */
  baseUrl: string;
  /** Optional extra headers (e.g. Authorization once auth lands in Milestone 3). */
  headers?: Record<string, string>;
}

/** Create a fully-typed Hermes API client. */
export function createHermesClient(options: HermesClientOptions): HermesClient {
  return createClient<paths>({
    baseUrl: options.baseUrl,
    headers: options.headers,
  });
}

export type { paths, components } from "./schema";
