---
slug: resource-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Plan to 70% utilisation (not 100%), map skills to tasks from a YAML roster in git, level resource load using critical-path analysis, and track allocations weekly against actuals.
content_id: "f79bfb8166391608"
tags: [resource-management, capacity-planning, pmbok, utilization, skill-matrix]
---
# Resource Management

## Summary

**One-sentence:** Plan to 70% utilisation (not 100%), map skills to tasks from a YAML roster in git, level resource load using critical-path analysis, and track allocations weekly against actuals.

**One-paragraph:** Plan to 70% utilisation (not 100%), map skills to tasks from a YAML roster in git, level resource load using critical-path analysis, and track allocations weekly against actuals. Agents propose reassignments; resource managers and individuals confirm. Rate cards live in a secrets store, not in the repo.

## Applies If (ALL must hold)

- Multi-team programs sharing scarce specialists (security, ML, SRE, designers) where allocation conflicts cause schedule slips
- Agency / consulting environments billing by utilisation with hard hourly budgets
- Programs spanning external contractors with rate cards and SOW linkage to deliverables
- Capacity planning across quarters when demand forecasts must align with hiring pipelines
- Workforce planning during reorgs where role mapping is non-trivial

## Skip If (ANY kills it)

- Stable single-team product squad with a tech lead doing capacity by feel — kanban WIP limits are sufficient
- Solopreneurs — calendar blocking covers it; resource matrices waste time
- Pre-PMF startups optimising for learning velocity — 100% of one engineer beats 60% of three
- Fixed-bid contracts where resource visibility is internal-only and not a deliverable
- Pure agile teams with stable sized backlogs — let the team self-organize within a fixed capacity

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
