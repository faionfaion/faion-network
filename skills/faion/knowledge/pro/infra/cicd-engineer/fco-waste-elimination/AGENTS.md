---
slug: fco-waste-elimination
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud waste elimination targets idle and orphaned resources that generate cost with zero value: unattached EBS volumes, orphaned snapshots, stopped instances, unused Elastic IPs, and idle load balancers.
content_id: "9ba4153749baaaed"
tags: [finops, waste-elimination, cloud-cost, idle-resources, non-prod-scheduling]
---
# Cloud Waste Elimination and Non-Production Scheduling

## Summary

**One-sentence:** Cloud waste elimination targets idle and orphaned resources that generate cost with zero value: unattached EBS volumes, orphaned snapshots, stopped instances, unused Elastic IPs, and idle load balancers.

**One-paragraph:** Cloud waste elimination targets idle and orphaned resources that generate cost with zero value: unattached EBS volumes, orphaned snapshots, stopped instances, unused Elastic IPs, and idle load balancers. Non-production scheduling shuts down dev, staging, and QA environments during off-hours, achieving 65-70% savings on non-prod compute. These are the fastest FinOps quick wins — implementation in hours, savings immediate.

## Applies If (ALL must hold)

- First FinOps action in any environment — waste elimination has zero risk and immediate ROI.
- Non-production environments that are only used during business hours or weekdays.
- Any environment where a resource audit has not been performed in the past 30 days.
- Before a quarterly FinOps review — clean waste first, then analyze the remaining spend meaningfully.

## Skip If (ANY kills it)

- Automated deletion without a dry-run step first — always audit before destroying.
- Non-production environments that require 24/7 availability for on-call, customer demos, or automated overnight jobs — define explicit exceptions before enabling scheduling.

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
