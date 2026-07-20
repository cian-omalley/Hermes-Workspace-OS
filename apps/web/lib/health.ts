// Small, framework-independent helpers for talking to the Hermes API health endpoint.
// Kept pure so it is unit-testable without a running server.

export interface ApiHealth {
  status: string;
  service: string;
  version: string;
  environment: string;
}

export type StackStatus = "ok" | "degraded" | "down";

/** Resolve the API base URL from the environment, with a sensible dev default. */
export function apiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
}

/** Map an API health payload (or a failure) to a coarse stack status. */
export function toStackStatus(health: ApiHealth | null): StackStatus {
  if (health === null) return "down";
  return health.status === "ok" ? "ok" : "degraded";
}

/** Fetch API health; returns null if the API is unreachable or unhealthy. */
export async function fetchApiHealth(
  fetchImpl: typeof fetch = fetch,
): Promise<ApiHealth | null> {
  try {
    const res = await fetchImpl(`${apiBaseUrl()}/health`, { cache: "no-store" });
    if (!res.ok) return null;
    return (await res.json()) as ApiHealth;
  } catch {
    return null;
  }
}
