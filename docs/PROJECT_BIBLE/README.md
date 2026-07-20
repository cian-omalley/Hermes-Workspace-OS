# Hermes Workspace OS — Project Bible

The **Project Bible** is the permanent source of truth for Hermes Workspace OS. It is the
navigable knowledge base and governance layer that every developer and every Claude Code
session should consult before working on the project.

## How the Bible relates to the numbered specs

- **Numbered specs** (`docs/00-ROADMAP.md` … `docs/15-UI_DESIGN.md`) are the deep
  **design specifications** for each subsystem.
- **The Project Bible** (this folder) is the **source of truth & operating manual**: it
  organizes knowledge into a stable structure, tracks *current state*, records decisions,
  and defines how development (including AI-assisted development) must proceed. Bible docs
  cross-reference the specs rather than duplicating their full depth.

See `docs/AUDIT_REPORT.md §8` for the rationale and the open consolidation decision (D4).

## Every Bible document follows the same shape

1. **Purpose** — why the document exists.
2. **Current State** — what actually exists in the repository today (honest; mostly
   "documented, not yet implemented" at this stage).
3. **Architecture Decisions** — important decisions and their reasoning.
4. **Alternatives Considered** — options weighed and why they were/weren't chosen.
5. **Future Improvements** — how the area can expand.
6. **Implementation Notes** — practical technical detail.

Unknowns are never left blank — they are marked **"Decision Required"** and explained,
with the master list in `docs/MISSING_INFORMATION.md`.

## Structure

| Section | Contents |
|---------|----------|
| **00_Overview** | Vision, Mission, Goals, Non-Goals, Glossary |
| **01_Product** | Product Requirements, Features, User Stories, User Workflows, Roadmap |
| **02_Architecture** | System, Technical, Technology Stack, Service, Data Flow, Security |
| **03_Core_Systems** | Core Systems, Agent, Memory, Knowledge, Search, Workflow |
| **04_Integrations** | Integrations, External Services, API Design, Third-Party Services |
| **05_Data** | Database Architecture, Data Models, Storage Design, Migration Strategy |
| **06_AI** | AI Architecture, Model Strategy, Prompt System, Agent Templates, Evaluation |
| **07_Interface** | UI Architecture, UX Principles, Dashboard, Design System |
| **08_Development** | Coding Standards, Git Workflow, Testing Strategy, Deployment, DevOps |
| **09_Implementation** | Development Phases, Milestones, Current Status, Task Breakdown |
| **10_Claude_Code** | Instructions, Architecture Rules, Coding Rules, Build Process |

## Start here

New to the project? Read in this order: **00_Overview/Vision → 02_Architecture/
System_Architecture → 09_Implementation/Current_Status → 10_Claude_Code/Instructions.**
