---
slug: finops-devops-cost-commitments
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three commitment discount mechanisms cover different workload shapes: Reserved Instances (RI) for stable instance-family workloads (up to 75% savings), Savings Plans for flexible compute baseline (up to 72%), and Spot Instances for fault-tolerant batch/ML (70-90%).
content_id: "c36fd17b10f1c60a"
tags: [finops, reserved-instances, savings-plans, spot-instances, cloud-cost]
---
# Cloud Commitment Discounts: RIs, Savings Plans, and Spot

## Summary

**One-sentence:** Three commitment discount mechanisms cover different workload shapes: Reserved Instances (RI) for stable instance-family workloads (up to 75% savings), Savings Plans for flexible compute baseline (up to 72%), and Spot Instances for fault-tolerant batch/ML (70-90%).

**One-paragraph:** Three commitment discount mechanisms cover different workload shapes: Reserved Instances (RI) for stable instance-family workloads (up to 75% savings), Savings Plans for flexible compute baseline (up to 72%), and Spot Instances for fault-tolerant batch/ML (70-90%). Apply in that order after rightsizing; committing to oversized instances wastes both compute and discount opportunity.

## Applies If (ALL must hold)

- 30+ days of stable workload data available — required to identify baseline vs variable usage before committing.
- Baseline compute represents more than $5k/month On-Demand — below that, Savings Plan overhead outweighs savings.
- Batch jobs, CI/CD runners, or ML training that tolerate interruption — these are Spot candidates (70-90% savings).
- After rightsizing — commit to the rightsized baseline, never the over-provisioned original.

## Skip If (ANY kills it)

- Less than 30 days of usage data — commit to wrong baseline and you overpay or underbuy.
- Workloads under active architectural rethink — a refactor may eliminate the service entirely; committed RIs become stranded.
- Highly variable workloads with no stable floor — Savings Plans need a minimum hourly floor; if hourly spend varies 10x, even a conservative floor may underutilize.

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
