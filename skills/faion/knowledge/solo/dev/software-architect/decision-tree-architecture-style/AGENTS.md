---
slug: decision-tree-architecture-style
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use this decision tree to choose between Monolith, Modular Monolith, and Microservices based on team size, DevOps maturity, and deployment frequency.
content_id: "7c01b3bb97f8a49e"
tags: [architecture, decision-tree, microservices, monolith, modular-monolith]
---
# Architecture Style Decision Tree

## Summary

**One-sentence:** Use this decision tree to choose between Monolith, Modular Monolith, and Microservices based on team size, DevOps maturity, and deployment frequency.

**One-paragraph:** Use this decision tree to choose between Monolith, Modular Monolith, and Microservices based on team size, DevOps maturity, and deployment frequency. The tree encodes 2025 industry evidence: 42% of organizations that adopted microservices have consolidated back (CNCF 2025).

## Applies If (ALL must hold)

- Starting a new project and need to pick an architecture style before any code is written.
- Evaluating whether to migrate a monolith to microservices — use the tree to confirm the preconditions are met.
- Onboarding non-architect contributors that need a defensible answer without a full ATAM cycle.
- Filtering architecture options before a heavier trade-off analysis or ADR.

## Skip If (ANY kills it)

- Genuinely novel constraints (regulatory, contractual) that gate the choice — the tree obscures the hard constraint.
- High-stakes irreversible decisions with unique context — use trees to shortlist, then full trade-off analysis to choose.
- After the architecture is already deployed — revisit only at planned review intervals.

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
