---
slug: c4-model
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The C4 model is a hierarchical diagramming approach for software architecture: Context (system + users + external systems), Containers (deployable units + technology choices), Components (internal structure of one container), and Code (class diagrams, usually auto-generated).
content_id: "7394c763c6abec95"
tags: [c4-model, architecture, visualization, diagrams, documentation]
---
# C4 Model for Architecture Visualization

## Summary

**One-sentence:** The C4 model is a hierarchical diagramming approach for software architecture: Context (system + users + external systems), Containers (deployable units + technology choices), Components (internal structure of one container), and Code (class diagrams, usually auto-generated).

**One-paragraph:** The C4 model is a hierarchical diagramming approach for software architecture: Context (system + users + external systems), Containers (deployable units + technology choices), Components (internal structure of one container), and Code (class diagrams, usually auto-generated). Each level zooms into the previous one. Always start at Level 1; create Level 4 only from auto-generation tools. Keep each diagram to 5–10 elements — split rather than crowd.

## Applies If (ALL must hold)

- Onboarding new contributors: Level 1 (Context) and Level 2 (Container) are mandatory.
- Architecture review: create diagrams to communicate current and target state.
- Documenting microservices topology: Container diagram shows services, databases, message brokers.
- Recording decisions in ADRs: reference C4 diagrams for the affected components.
- Sprint planning for cross-team features that touch multiple containers or external systems.
- Deployment diagrams for mapping containers to cloud infrastructure.

## Skip If (ANY kills it)

- Single-developer scripts or single-container applications where a simple README suffices.
- When diagrams would be discarded immediately — invest only if they will be maintained.
- Level 4 (Code) diagrams done manually — use IDE class diagram generation instead.
- As a substitute for ADRs: C4 shows structure, ADRs document the decisions behind structure.
- When the team has agreed on a different diagramming standard already in use — do not introduce C4 mid-project without buy-in.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/software-architect/`
