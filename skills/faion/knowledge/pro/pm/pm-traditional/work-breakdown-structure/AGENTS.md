---
slug: work-breakdown-structure
tier: pro
group: pm
domain: pm-traditional
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A hierarchical decomposition of total project scope into deliverable-oriented (noun-led) work packages.
content_id: "c3bcfc94a7e4ecc3"
tags: [wbs, scope-management, work-packages, project-decomposition, baseline]
---
# Work Breakdown Structure (WBS)

## Summary

**One-sentence:** A hierarchical decomposition of total project scope into deliverable-oriented (noun-led) work packages.

**One-paragraph:** A hierarchical decomposition of total project scope into deliverable-oriented (noun-led) work packages. Each leaf is assignable to one owner, estimable in 8–80 hours, and produces a tangible output. The 100% rule requires every parent to equal the sum of its children with no overlap or gaps.

## Applies If (ALL must hold)

- Establishing a contractual scope baseline for fixed-bid or government-style work.
- Cost estimation for proposals where each work package needs an hours/$ line.
- Programs spanning multiple teams or vendors needing a single ID schema (1.2.3) for integration.
- Compliance or audit contexts where every deliverable must be traceable to a parent objective.

## Skip If (ANY kills it)

- Backlog-driven product teams — the product backlog plus epics already plays the WBS role.
- Discovery or R&D where deliverables are emergent and unknowable up front.
- Sub-2-week tasks — a checklist or kanban swimlane suffices.
- Steady-state operations work — use a service catalog, not a WBS.

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

- parent skill: `pro/pm/pm-traditional/`
