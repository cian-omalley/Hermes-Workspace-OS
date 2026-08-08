# Knowledge Hub

The **single front door** to everything Hermes knows about itself. Every document in the
repository is catalogued here so nothing is lost or "missing." New files and links are
filed here by the **Knowledge Curator** agent (see below) under the rules in
[`CURATION_RULES.md`](./CURATION_RULES.md).

> **Design note:** the deep documents (Project Bible, numbered specs) stay in their
> established locations so `CLAUDE.md`'s required reading order and their cross-links keep
> working. This hub **indexes and links** them rather than moving them. Incoming external
> material lives under [`sources/`](./sources/).

## Start here (for humans and AI)

1. **[`AI_PRIMER.md`](./AI_PRIMER.md)** — the condensed, memorizable brief of the whole
   project. **If you read one file, read this.** Optimized for AI models to ingest fast.
2. **[`CURATION_RULES.md`](./CURATION_RULES.md)** — how files/links are sorted and rewritten.
3. This index — the full map of every document.

---

## 1. Governance & entry points (repo root)

| Document | Purpose |
|----------|---------|
| [`CLAUDE.md`](../../CLAUDE.md) | Entry point + non-negotiable rules for Claude Code sessions |
| [`README.md`](../../README.md) | Project introduction |
| [`CONTRIBUTING.md`](../../CONTRIBUTING.md) | Contribution guide |
| [`CHANGELOG.md`](../../CHANGELOG.md) | Release/milestone history |

## 2. Reports & orientation (`docs/`)

| Document | Purpose |
|----------|---------|
| [`PROJECT_MAP.md`](../PROJECT_MAP.md) | Single-page orientation to the repo & system |
| [`AUDIT_REPORT.md`](../AUDIT_REPORT.md) | Repository audit & findings |
| [`MISSING_INFORMATION.md`](../MISSING_INFORMATION.md) | Open decisions (D1–D10), gaps, risks |

## 3. Design specifications (`docs/00–15`)

The deep, canonical spec for each subsystem.

| # | Spec | # | Spec |
|---|------|---|------|
| 00 | [Roadmap](../00-ROADMAP.md) | 08 | [GitHub Integration](../08-GITHUB_INTEGRATION.md) |
| 01 | [Vision](../01-VISION.md) | 09 | [DeepWiki System](../09-DEEPWIKI_SYSTEM.md) |
| 02 | [Product Requirements](../02-PRODUCT_REQUIREMENTS.md) | 10 | [Agent System](../10-AGENT_SYSTEM.md) |
| 03 | [System Architecture](../03-SYSTEM_ARCHITECTURE.md) | 11 | [Knowledge Graph](../11-KNOWLEDGE_GRAPH.md) |
| 04 | [Tech Stack](../04-TECH_STACK.md) | 12 | [Search System](../12-SEARCH_SYSTEM.md) |
| 05 | [Database Design](../05-DATABASE_DESIGN.md) | 13 | [File Ingestion](../13-FILE_INGESTION.md) |
| 06 | [Plugin Architecture](../06-PLUGIN_ARCHITECTURE.md) | 14 | [Workflow System](../14-WORKFLOW_SYSTEM.md) |
| 07 | [Notion Integration](../07-NOTION_INTEGRATION.md) | 15 | [UI Design](../15-UI_DESIGN.md) |
| | | 16 | [Agent Departments](../16-AGENT_DEPARTMENTS.md) |

## 4. Project Bible (`docs/PROJECT_BIBLE/`) — the source of truth

The navigable knowledge base and governance layer. Index: [`PROJECT_BIBLE/README.md`](../PROJECT_BIBLE/README.md).

| Section | Documents |
|---------|-----------|
| 00 Overview | [Vision](../PROJECT_BIBLE/00_Overview/Vision.md) · [Mission](../PROJECT_BIBLE/00_Overview/Mission.md) · [Goals](../PROJECT_BIBLE/00_Overview/Goals.md) · [Non-Goals](../PROJECT_BIBLE/00_Overview/Non_Goals.md) · [Glossary](../PROJECT_BIBLE/00_Overview/Glossary.md) |
| 01 Product | [Product Requirements](../PROJECT_BIBLE/01_Product/Product_Requirements.md) · [Features](../PROJECT_BIBLE/01_Product/Features.md) · [User Stories](../PROJECT_BIBLE/01_Product/User_Stories.md) · [User Workflows](../PROJECT_BIBLE/01_Product/User_Workflows.md) · [Roadmap](../PROJECT_BIBLE/01_Product/Roadmap.md) |
| 02 Architecture | [System](../PROJECT_BIBLE/02_Architecture/System_Architecture.md) · [Technical](../PROJECT_BIBLE/02_Architecture/Technical_Architecture.md) · [Technology Stack](../PROJECT_BIBLE/02_Architecture/Technology_Stack.md) · [Service](../PROJECT_BIBLE/02_Architecture/Service_Architecture.md) · [Data Flow](../PROJECT_BIBLE/02_Architecture/Data_Flow.md) · [Security Model](../PROJECT_BIBLE/02_Architecture/Security_Model.md) |
| 03 Core Systems | [Core Systems](../PROJECT_BIBLE/03_Core_Systems/Core_Systems.md) · [Agent](../PROJECT_BIBLE/03_Core_Systems/Agent_System.md) · [Agent Departments](../PROJECT_BIBLE/03_Core_Systems/Agent_Departments.md) · [Memory](../PROJECT_BIBLE/03_Core_Systems/Memory_System.md) · [Knowledge](../PROJECT_BIBLE/03_Core_Systems/Knowledge_System.md) · [Search](../PROJECT_BIBLE/03_Core_Systems/Search_System.md) · [Workflow](../PROJECT_BIBLE/03_Core_Systems/Workflow_System.md) |
| 04 Integrations | [Integrations](../PROJECT_BIBLE/04_Integrations/Integrations.md) · [External Services](../PROJECT_BIBLE/04_Integrations/External_Services.md) · [API Design](../PROJECT_BIBLE/04_Integrations/API_Design.md) · [Third-Party Services](../PROJECT_BIBLE/04_Integrations/Third_Party_Services.md) |
| 05 Data | [Database Architecture](../PROJECT_BIBLE/05_Data/Database_Architecture.md) · [Data Models](../PROJECT_BIBLE/05_Data/Data_Models.md) · [Storage Design](../PROJECT_BIBLE/05_Data/Storage_Design.md) · [Migration Strategy](../PROJECT_BIBLE/05_Data/Migration_Strategy.md) |
| 06 AI | [AI Architecture](../PROJECT_BIBLE/06_AI/AI_Architecture.md) · [Model Strategy](../PROJECT_BIBLE/06_AI/Model_Strategy.md) · [Prompt System](../PROJECT_BIBLE/06_AI/Prompt_System.md) · [Agent Templates](../PROJECT_BIBLE/06_AI/Agent_Templates.md) · [Evaluation](../PROJECT_BIBLE/06_AI/Evaluation_System.md) |
| 07 Interface | [UI Architecture](../PROJECT_BIBLE/07_Interface/UI_Architecture.md) · [UX Principles](../PROJECT_BIBLE/07_Interface/UX_Principles.md) · [Dashboard](../PROJECT_BIBLE/07_Interface/Dashboard.md) · [Design System](../PROJECT_BIBLE/07_Interface/Design_System.md) |
| 08 Development | [Coding Standards](../PROJECT_BIBLE/08_Development/Coding_Standards.md) · [Git Workflow](../PROJECT_BIBLE/08_Development/Git_Workflow.md) · [Testing Strategy](../PROJECT_BIBLE/08_Development/Testing_Strategy.md) · [Deployment](../PROJECT_BIBLE/08_Development/Deployment.md) · [DevOps](../PROJECT_BIBLE/08_Development/DevOps.md) |
| 09 Implementation | [Development Phases](../PROJECT_BIBLE/09_Implementation/Development_Phases.md) · [Milestones](../PROJECT_BIBLE/09_Implementation/Milestones.md) · [Current Status](../PROJECT_BIBLE/09_Implementation/Current_Status.md) · [Task Breakdown](../PROJECT_BIBLE/09_Implementation/Task_Breakdown.md) |
| 10 Claude Code | [Instructions](../PROJECT_BIBLE/10_Claude_Code/Instructions.md) · [Architecture Rules](../PROJECT_BIBLE/10_Claude_Code/Architecture_Rules.md) · [Coding Rules](../PROJECT_BIBLE/10_Claude_Code/Coding_Rules.md) · [Build Process](../PROJECT_BIBLE/10_Claude_Code/Build_Process.md) |

## 5. External reference library (`sources/`)

Curated external tools/projects that inform the Hermes vision (the *MRZ Hermes Knowledge
Stack*). Index: [`sources/README.md`](./sources/README.md).

## 6. Component READMEs (code)

[`apps/web`](../../apps/web/README.md) · [`services/api`](../../services/api/README.md) ·
[`services/worker`](../../services/worker/README.md) ·
[`packages/hermes-domain`](../../packages/hermes-domain/README.md) ·
[`packages/ts-client`](../../packages/ts-client/README.md) ·
[`database`](../../database/README.md) · [`tests`](../../tests/README.md)

---

## 7. Agent departments & orchestration (Claude Code tooling)

A team of real Claude Code subagents, organized into departments, builds and maintains this
repo. Canonical design: [`docs/16-AGENT_DEPARTMENTS.md`](../16-AGENT_DEPARTMENTS.md); governance:
[`Agent_Departments.md`](../PROJECT_BIBLE/03_Core_Systems/Agent_Departments.md).

- **Engineering (Core):** [`product-manager`](../../.claude/agents/product-manager.md) ·
  [`researcher`](../../.claude/agents/researcher.md) ·
  [`engineer`](../../.claude/agents/engineer.md) ·
  [`code-reviewer`](../../.claude/agents/code-reviewer.md) ·
  [`qa-tester`](../../.claude/agents/qa-tester.md) ·
  [`release-manager`](../../.claude/agents/release-manager.md)
- **Knowledge & Operations:** [`orchestrator`](../../.claude/agents/orchestrator.md) ·
  [`knowledge-curator`](../../.claude/agents/knowledge-curator.md) *(the sorter)* ·
  [`deepwiki-brain`](../../.claude/agents/deepwiki-brain.md) ·
  [`memory-keeper`](../../.claude/agents/memory-keeper.md)
- **Coordination protocol & durable state:**
  [`.claude/orchestration/`](../../.claude/orchestration/README.md) — the shared blackboard and
  worklog that let a single task run across many sessions and be resumed.

## The Knowledge Curator agent

A dedicated project agent — [`.claude/agents/knowledge-curator.md`](../../.claude/agents/knowledge-curator.md)
— files incoming documents/links here and rewrites them into the AI-friendly format
defined in [`CURATION_RULES.md`](./CURATION_RULES.md). Invoke it whenever new source
material arrives. It is the **sorter** of the Knowledge & Operations department (above).
