---
slug: cost-estimation
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured approach to producing a defensible project cost baseline: bottom-up estimation from a WBS, three-point (PERT) uncertainty modelling, risk-driven contingency reserve, and a separate management reserve.
content_id: "cfd9ea2bd6d65b5a"
tags: [estimation, budget, cost-baseline, wbs, pert]
---
# Cost Estimation

## Summary

**One-sentence:** Structured approach to producing a defensible project cost baseline: bottom-up estimation from a WBS, three-point (PERT) uncertainty modelling, risk-driven contingency reserve, and a separate management reserve.

**One-paragraph:** Structured approach to producing a defensible project cost baseline: bottom-up estimation from a WBS, three-point (PERT) uncertainty modelling, risk-driven contingency reserve, and a separate management reserve. Output is a Cost Baseline plus Budget at Completion (BAC), versioned through every change-control event.

## Applies If (ALL must hold)

- Producing an initial budget for a feature, project, or RFP response.
- Bottom-up estimation from a WBS (each work package gets labor + tools + infra cost).
- Build-vs-buy / build-vs-SaaS decisions where opportunity cost must be quantified.
- Updating the cost baseline after a change-control event.
- Solopreneur "true cost" analysis — own time at market rate vs. out-of-pocket spend.

## Skip If (ANY kills it)

- Agile teams estimating via story points + capacity-based run-rate — cost is derived from team-month spend, not bottom-up sums.
- Pre-discovery exploration where requirements are less than 30% defined — use ROM (rough order of magnitude, plus or minus 50%) instead; bottom-up output will be a fantasy.
- Fixed-fee contracts already signed — internal re-estimation has no contractual force and creates confusion.

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

- parent skill: `pro/pm/project-manager/`
