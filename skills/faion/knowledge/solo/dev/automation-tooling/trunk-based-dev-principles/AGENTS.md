---
slug: trunk-based-dev-principles
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Trunk-Based Development (TBD) is a source-control branching model where developers collaborate on code in a single branch called "trunk" (or "main/master"), resisting any pressure to create long-lived development branches.
content_id: "df85cfb7c256085d"
tags: [trunk-based-development, branching-strategy, continuous-integration, devops, high-performance]
---
# Trunk-Based Development: Principles

## Summary

**One-sentence:** Trunk-Based Development (TBD) is a source-control branching model where developers collaborate on code in a single branch called "trunk" (or "main/master"), resisting any pressure to create long-lived development branches.

**One-paragraph:** Trunk-Based Development (TBD) is a source-control branching model where developers collaborate on code in a single branch called "trunk" (or "main/master"), resisting any pressure to create long-lived development branches. Small, frequent commits to trunk enable Continuous Integration and reduce merge conflicts.

## Applies If (ALL must hold)

- Teams practicing CI/CD and rapid iteration.
- Projects requiring fast feedback and frequent releases.
- When merge conflicts are blocking productivity.
- High-performing DevOps teams aiming for DORA metrics improvement.
- When feature flag infrastructure exists to hide incomplete work.
- Strong automated testing in place to gate merges.

## Skip If (ANY kills it)

- Weak test coverage or no automated tests — TBD without tests is "trunk is always broken".
- No CI/CD pipeline — you need automated gates.
- Regulatory compliance requiring branch isolation or long audit trails per branch.
- Open-source projects with external contributors who need review cycles.

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

- parent skill: `solo/dev/automation-tooling/`
