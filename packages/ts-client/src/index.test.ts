import { describe, expect, it } from "vitest";

import { createHermesClient } from "./index";

describe("createHermesClient", () => {
  it("creates a client exposing the openapi-fetch verbs", () => {
    const client = createHermesClient({ baseUrl: "http://localhost:8000" });
    // Typed methods from openapi-fetch are present.
    expect(typeof client.GET).toBe("function");
    expect(typeof client.POST).toBe("function");
    expect(typeof client.PATCH).toBe("function");
    expect(typeof client.DELETE).toBe("function");
  });
});
