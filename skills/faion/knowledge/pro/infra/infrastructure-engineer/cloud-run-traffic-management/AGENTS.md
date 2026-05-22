---
slug: cloud-run-traffic-management
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Run supports revision-based traffic splitting: deploy a new revision without traffic, test it via a tagged URL, then gradually shift traffic using update-traffic commands.
content_id: "c884ea2b355774d1"
tags: [gcp, cloud-run, traffic-management, blue-green, canary]
---
# Cloud Run Traffic Management

## Summary

**One-sentence:** Cloud Run supports revision-based traffic splitting: deploy a new revision without traffic, test it via a tagged URL, then gradually shift traffic using update-traffic commands.

**One-paragraph:** Cloud Run supports revision-based traffic splitting: deploy a new revision without traffic, test it via a tagged URL, then gradually shift traffic using update-traffic commands. Revisions are immutable; rollback is instant via --to-revisions pointing to a prior revision. Tags give stable preview URLs independent of traffic allocation.

## Applies If (ALL must hold)

- Releasing a new version of a Cloud Run service with zero-downtime.
- Testing a new revision before routing production traffic to it.
- Implementing canary releases with gradual traffic percentages.
- Rolling back a bad deployment to a prior revision instantly.
- Running A/B tests across two revisions of the same service.

## Skip If (ANY kills it)

- Cloud Run Jobs — Jobs do not have HTTP traffic; use task execution and retry controls instead.
- Service deployment configuration — see cloud-run-deployment for gcloud flags and Terraform.
- Autoscaling and concurrency tuning — see cloud-run-autoscaling.

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

- parent skill: `pro/infra/infrastructure-engineer/`
