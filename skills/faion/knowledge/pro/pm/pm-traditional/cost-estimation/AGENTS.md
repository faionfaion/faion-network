---
slug: cost-estimation
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A bottom-up cost estimation process: decompose the WBS into work packages, apply three-point PERT estimation per package, load labor with a fully-loaded multiplier (1.
content_id: "cfd9ea2bd6d65b5a"
tags: [cost-estimation, budgeting, risk-management, project-management, pmbok]
---
# Cost Estimation

## Summary

**One-sentence:** A bottom-up cost estimation process: decompose the WBS into work packages, apply three-point PERT estimation per package, load labor with a fully-loaded multiplier (1.

**One-paragraph:** A bottom-up cost estimation process: decompose the WBS into work packages, apply three-point PERT estimation per package, load labor with a fully-loaded multiplier (1.3-2.0x depending on region and benefits), add tools and infrastructure costs, calculate risk-driven contingency (sum of probability x cost-exposure per open risk), separate contingency reserve from management reserve, and produce a cost baseline (BAC = Cost Baseline + Management Reserve). The agent is a calculator and auditor, not a decision-maker; humans approve all numbers before they enter the budget.

## Applies If (ALL must hold)

- Producing the initial budget from an approved WBS before kickoff
- Bottom-up cost roll-up for an RFP response requiring a defensible cost baseline
- Build-vs-buy / build-vs-SaaS decisions where opportunity cost matters
- Updating the cost baseline after an approved change-control event
- Solopreneur "true cost" analysis pricing own time at market rate

## Skip If (ANY kills it)

- Agile teams that fund team capacity by time-box, not by feature — use team-month run-rate, not bottom-up sum
- Pre-discovery with requirements <30% defined — output will have false precision; use ROM (±50%) instead
- Already-negotiated fixed-fee contracts — re-estimating internally has no contractual force
- Tasks under 1 week where estimate cost exceeds work cost

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
