---
slug: fco-commitment-pricing
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Commitment-based pricing (Reserved Instances and Savings Plans) delivers 60-75% discounts over on-demand for predictable steady-state workloads.
content_id: "96c598c57bef1b32"
tags: [finops, reserved-instances, savings-plans, cloud-cost, commitment-pricing]
---
# Reserved Instances and Savings Plans

## Summary

**One-sentence:** Commitment-based pricing (Reserved Instances and Savings Plans) delivers 60-75% discounts over on-demand for predictable steady-state workloads.

**One-paragraph:** Commitment-based pricing (Reserved Instances and Savings Plans) delivers 60-75% discounts over on-demand for predictable steady-state workloads. The key discipline is to rightsize before committing, target 70-80% of baseline compute, and start conservative with Convertible RIs to preserve flexibility while the commitment strategy matures.

## Applies If (ALL must hold)

- Production databases, application servers, and analytics clusters that run 24/7 without interruption.
- Workloads with at least 6 months of stable usage history to establish a reliable baseline.
- Any environment where on-demand compute exceeds $5,000/month — the break-even on a 1-year RI is typically 7-9 months.
- After rightsizing: always rightsize first, then commit to the correct size.

## Skip If (ANY kills it)

- Variable or bursty workloads with no stable baseline — commit only to the floor, use on-demand or Spot for burst.
- Workloads scheduled to be decommissioned or migrated within the commitment period.
- Environments where the architecture is actively evolving (consider shorter 1-year terms or Convertible RIs instead).

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

- parent skill: `pro/infra/cicd-engineer/`
