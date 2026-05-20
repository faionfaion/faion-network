---
slug: solution-assessment
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Evaluates a solution's ability to meet the business need and deliver expected value across four assessment types: design, implementation, deployment, and post-implementation.
content_id: "5f84aa75055f6434"
tags: [solution, assessment, evaluation, bakok, value]
---
# Solution Assessment

## Summary

**One-sentence:** Evaluates a solution's ability to meet the business need and deliver expected value across four assessment types: design, implementation, deployment, and post-implementation.

**One-paragraph:** Evaluates a solution's ability to meet the business need and deliver expected value across four assessment types: design, implementation, deployment, and post-implementation. Structured five-step framework: define criteria → assess vs requirements → evaluate business value → identify limitations → recommend action.

## Applies If (ALL must hold)

- Stage-gate of the BAKOK Solution Evaluation knowledge area: "does the solution deliver enterprise value?" against the original business need.
- Design and implementation assessments inside the build phase ("are we still on the right path?").
- Pre go-live deployment readiness review where multiple workstreams must produce one accept/reject row.
- 30/90/365-day post-implementation reviews scoring requirements compliance and benefit realization.
- Solution limitations capture for compliance, audit, or vendor-renewal files.
- Lessons-learned input to the next iteration's strategy analysis (current state → future state).

## Skip If (ANY kills it)

- Continuous-discovery pre-PMF work where requirements are still being invented every sprint — "REQ-001 met" is meaningless when REQ-001 was wrong.
- Throwaway prototypes, spikes, internal tools used by a handful of people — a 15-minute retro replaces the whole template.
- Pure SRE/platform tuning (latency, cost, capacity) — use SLOs and error budgets.
- When no baseline exists — without a measured "before," the variance column is vibes; back-fill the baseline first.
- When the assessor reports to the project sponsor whose bonus depends on the result — route to an independent reviewer.

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

- parent skill: `pro/ba/ba-core/`
