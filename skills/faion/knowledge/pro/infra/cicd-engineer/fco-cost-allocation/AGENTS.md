---
slug: fco-cost-allocation
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cost allocation assigns cloud spend to the teams, services, and environments that generate it.
content_id: "002c850a2a4ee296"
tags: [finops, cost-allocation, tagging, chargeback, cloud-governance]
---
# Cloud Cost Allocation and Tagging Strategy

## Summary

**One-sentence:** Cost allocation assigns cloud spend to the teams, services, and environments that generate it.

**One-paragraph:** Cost allocation assigns cloud spend to the teams, services, and environments that generate it. Without a mandatory tagging taxonomy enforced at resource creation time, cost accountability is impossible — teams cannot optimize what they cannot see. A 300-person engineering org that implemented cost allocation reduced total spend by 20% in 6 months, not by technical optimization, but by making each team responsible for its own bill.

## Applies If (ALL must hold)

- Organizations with more than one team sharing cloud accounts where cost accountability is unclear.
- Before implementing chargeback or showback models — tagging must precede attribution.
- When cloud spend exceeds $50,000/month and no team-level breakdowns exist.
- When implementing budget alerts and wanting to notify the correct team owner.

## Skip If (ANY kills it)

- Single-person teams or single-service accounts where the entire bill is already attributed to one owner — tagging overhead exceeds value.
- Temporary scratch accounts for R&D that are destroyed within days — enforce time-to-live instead of full tagging policy.

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
