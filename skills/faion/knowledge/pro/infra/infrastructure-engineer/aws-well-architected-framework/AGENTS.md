---
slug: aws-well-architected-framework
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The AWS Well-Architected Framework defines 6 pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) for evaluating production workloads.
content_id: "96c9e3137ce84f44"
tags: [aws, well-architected, cloud-architecture, review, governance]
---
# AWS Well-Architected Framework Review

## Summary

**One-sentence:** The AWS Well-Architected Framework defines 6 pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) for evaluating production workloads.

**One-paragraph:** The AWS Well-Architected Framework defines 6 pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) for evaluating production workloads. Use it to score existing deployments, identify gaps, and produce a prioritized remediation plan backed by IaC evidence.

## Applies If (ALL must hold)

- Before a major release or compliance audit — establish a baseline score per pillar.
- Quarterly hygiene reviews for production workloads.
- Pre-migration assessment when moving a workload from on-prem or another cloud to AWS.
- Post-incident review where the root cause crosses multiple pillars (e.g., Reliability + Operational Excellence gap).
- When a team inherits an undocumented AWS environment and needs a structured starting point.

## Skip If (ANY kills it)

- Single-account hobby or prototype projects — overhead of a 6-pillar review outweighs the value.
- Pure application-layer decisions (DB schema, framework choice) — use dev skills instead.
- Day-2 incident response — use AIOps / observability runbooks; the WAFR is a planning tool, not an ops tool.
- Non-AWS clouds — GCP has its own Architecture Framework; use gcp-arch-basics instead.

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
