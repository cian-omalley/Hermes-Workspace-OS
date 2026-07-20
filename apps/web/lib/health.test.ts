import { describe, expect, it } from "vitest";

import { fetchApiHealth, toStackStatus, type ApiHealth } from "./health";

const okHealth: ApiHealth = {
  status: "ok",
  service: "hermes-api",
  version: "0.1.0",
  environment: "test",
};

describe("toStackStatus", () => {
  it("maps ok health to ok", () => {
    expect(toStackStatus(okHealth)).toBe("ok");
  });

  it("maps non-ok health to degraded", () => {
    expect(toStackStatus({ ...okHealth, status: "starting" })).toBe("degraded");
  });

  it("maps null (unreachable) to down", () => {
    expect(toStackStatus(null)).toBe("down");
  });
});

describe("fetchApiHealth", () => {
  it("returns the parsed payload on success", async () => {
    const fakeFetch = (async () =>
      new Response(JSON.stringify(okHealth), { status: 200 })) as typeof fetch;
    await expect(fetchApiHealth(fakeFetch)).resolves.toEqual(okHealth);
  });

  it("returns null on a non-2xx response", async () => {
    const fakeFetch = (async () => new Response("nope", { status: 503 })) as typeof fetch;
    await expect(fetchApiHealth(fakeFetch)).resolves.toBeNull();
  });

  it("returns null when fetch throws (API unreachable)", async () => {
    const fakeFetch = (async () => {
      throw new Error("ECONNREFUSED");
    }) as typeof fetch;
    await expect(fetchApiHealth(fakeFetch)).resolves.toBeNull();
  });
});
