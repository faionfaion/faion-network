---
slug: finops-devops-cost-tagging
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cost allocation accuracy depends entirely on tag compliance.
content_id: "908136142eb8d2e5"
tags: [finops, tagging, cost-allocation, policy-as-code, multi-cloud]
---
# Cloud Resource Tagging Policy and Cost Allocation

## Summary

**One-sentence:** Cost allocation accuracy depends entirely on tag compliance.

**One-paragraph:** Cost allocation accuracy depends entirely on tag compliance. Without tags, cloud bills are a lump sum with no attribution to team, project, or environment. The target is 95%+ tag compliance enforced at resource-creation time via provider-native policy mechanisms — SCPs on AWS, Azure Policy, GCP organization policies — not patched retroactively via audits.

## Applies If (ALL must hold)

- Setting up a new cloud account or subscription — enforce tags from day one before the untagged backlog accumulates.
- Tag compliance below 90% — implement SCPs/policies to enforce mandatory tags at creation.
- Multiple teams sharing a cloud account with no chargeback mechanism — tags are the basis for per-team cost visibility.
- Multi-cloud environments (AWS + Azure + GCP) — establish a unified tag schema across all providers.
- Before implementing cost dashboards — dashboards are only as good as the tag data feeding them.

## Skip If (ANY kills it)

- Single-team, single-project accounts with one budget line — tagging adds overhead with no allocation benefit.
- Enforcing tags on ephemeral infrastructure (Lambda invocations, auto-scaling replacements) that inherit tags from parent resources — enforce at the launch template/ASG level instead.

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
