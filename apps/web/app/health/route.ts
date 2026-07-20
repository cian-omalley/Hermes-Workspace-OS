import { NextResponse } from "next/server";

import { fetchApiHealth, toStackStatus } from "@/lib/health";

// Web-tier health endpoint. Reports the web app as up and includes the upstream API
// status, so the compose healthcheck / CI can probe the frontend too.
export async function GET() {
  const api = await fetchApiHealth();
  return NextResponse.json({
    status: "ok",
    service: "hermes-web",
    api: toStackStatus(api),
  });
}
