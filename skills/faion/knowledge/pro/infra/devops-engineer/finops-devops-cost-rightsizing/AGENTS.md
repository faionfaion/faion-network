---
slug: finops-devops-cost-rightsizing
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Rightsizing reduces compute and database instance costs 15-25% by matching resource allocation to actual utilization.
content_id: "92e8d7cea203e0b2"
tags: [finops, rightsizing, cloud-cost, waste-elimination, cloud-optimization]
---
# Cloud Cost Rightsizing and Waste Elimination

## Summary

**One-sentence:** Rightsizing reduces compute and database instance costs 15-25% by matching resource allocation to actual utilization.

**One-paragraph:** Rightsizing reduces compute and database instance costs 15-25% by matching resource allocation to actual utilization. Waste elimination (unattached volumes, idle IPs, orphaned snapshots) delivers quick 10-20% savings with low risk. Together these are the highest-ROI first actions in any FinOps engagement.

## Applies If (ALL must hold)

- Average CPU utilization below 20% or memory below 30% across production instances — provider tools surface these automatically.
- Dev/test environments running 24/7 with no scheduling — scheduling to office hours yields 64% savings on dev compute.
- Unattached EBS volumes, unused Elastic IPs, orphaned snapshots older than 90 days present in the account.
- Post-migration environments where instance types were lifted-and-shifted from on-prem without rightsizing.
- Before purchasing Reserved Instances or Savings Plans — commit to rightsized baseline, not the current wasteful one.

## Skip If (ANY kills it)

- Instances with spiky, unpredictable CPU (e.g. event-driven services) — utilization averages are misleading; rightsize only after enabling autoscaling.
- Stateful services mid-migration — measure steady state first, then rightsize.
- Production databases before a load test validates the new size in staging.

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
