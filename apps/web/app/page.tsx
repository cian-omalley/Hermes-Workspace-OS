import { fetchApiHealth, toStackStatus } from "@/lib/health";

// Server component: on render, check the API health so the landing page doubles as a
// minimal stack health dashboard (Milestone 1 exit criteria). Richer dashboard widgets
// arrive in Milestone 10.
export default async function Home() {
  const health = await fetchApiHealth();
  const status = toStackStatus(health);

  const label =
    status === "ok" ? "All systems operational" : status === "degraded" ? "Degraded" : "API unreachable";

  return (
    <main>
      <h1>Hermes Workspace OS</h1>
      <p className="muted">Self-hostable AI Workspace Operating System</p>

      <div className="card">
        <div className="status">
          <span className={`dot ${status}`} aria-hidden="true" />
          <span>{label}</span>
        </div>
        {health ? (
          <p className="muted">
            API <code>{health.service}</code> v{health.version} · env {health.environment}
          </p>
        ) : (
          <p className="muted">
            The API is not reachable yet. Start the stack with <code>just up</code> and{" "}
            <code>just api</code>.
          </p>
        )}
      </div>

      <p className="muted" style={{ marginTop: "2rem" }}>
        This is the Milestone 1 skeleton. See <code>docs/PROJECT_BIBLE</code> for the plan.
      </p>
    </main>
  );
}
