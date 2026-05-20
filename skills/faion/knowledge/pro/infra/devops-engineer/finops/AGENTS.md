---
slug: finops
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Financial Operations: the Inform → Optimize → Operate cycle for cloud cost management.
content_id: "8661f3de323070e9"
tags: [finops, cloud-cost, aws, gcp, tagging]
---
# FinOps

## Summary

**One-sentence:** Cloud Financial Operations: the Inform → Optimize → Operate cycle for cloud cost management.

**One-paragraph:** Cloud Financial Operations: the Inform → Optimize → Operate cycle for cloud cost management. Organizations waste 32% of cloud spend (~$200B/year globally). FinOps teams achieve 10-20x ROI within 30-60 days by making cost visible (tagging), eliminating waste (rightsizing, idle resources), and committing (Savings Plans/Reserved Instances).

## Applies If (ALL must hold)

- Cloud monthly spend exceeds $10k and cost attribution is unclear
- Engineering teams have no visibility into their own cloud costs
- Preparing Savings Plan or Reserved Instance purchases (need 30+ days baseline)
- Rightsizing instances where avg CPU is below 20% or memory below 30%
- AI/ML training workloads where GPU instances run on-demand without checkpointing

## Skip If (ANY kills it)

- Pre-production environments with no steady-state usage patterns — optimization signal is noisy
- When cost data is less than 30 days old — too early for commitment recommendations
- As a substitute for architecture decisions (e.g., using FinOps to offset a fundamentally overprovisioned design)

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

- parent skill: `pro/infra/devops-engineer/`
