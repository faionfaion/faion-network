---
slug: fco-rightsizing
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Rightsizing matches instance sizes to actual workload requirements.
content_id: "6d566b12295871e8"
tags: [finops, rightsizing, cloud-cost, compute-optimization, graviton]
---
# Cloud Instance Rightsizing

## Summary

**One-sentence:** Rightsizing matches instance sizes to actual workload requirements.

**One-paragraph:** Rightsizing matches instance sizes to actual workload requirements. Most teams overprovision to ensure systems do not crash during peak hours, leaving CPU utilization below 30% and memory below 40%. A systematic 4-week analysis followed by phased downsizing consistently delivers 20-40% compute savings with zero performance impact.

## Applies If (ALL must hold)

- Any cloud environment that has been running for 4+ weeks and has not been rightsized in the past quarter.
- Instances upgraded "just in case" for an anticipated traffic spike that never arrived.
- B2B SaaS or microservices platforms with 10+ instances where even 10% savings is significant at scale.
- Before purchasing Reserved Instances — rightsize first, then commit to correct sizing.
- Post-migration: newly migrated workloads are commonly oversized due to lift-and-shift conservatism.

## Skip If (ANY kills it)

- Instances with highly variable or spiky CPU (peak exceeds 70%) — downsizing risks throttling under load.
- Latency-sensitive production services where a 5-10% CPU headroom matters — require load testing first.
- Fewer than 4 weeks of monitoring data — insufficient to distinguish baseline from anomaly.

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
