---
slug: gcp-billing-cost
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GCP billing is structured around billing accounts linked to projects, with costs attributed via resource labels.
content_id: "3db8a9f995bba80f"
tags: [gcp, billing, cost-management, budgets, cost-allocation]
---
# GCP Billing and Cost Management

## Summary

**One-sentence:** GCP billing is structured around billing accounts linked to projects, with costs attributed via resource labels.

**One-paragraph:** GCP billing is structured around billing accounts linked to projects, with costs attributed via resource labels. Budget alerts at 50%, 90%, and 100% thresholds prevent surprise overspend. BigQuery billing exports enable custom dashboards and per-team chargeback via label-based queries. Labels are the only mechanism for cost allocation — enforce them from day one via org policy.

## Applies If (ALL must hold)

- Setting up billing for a new GCP organization, project, or environment.
- Implementing cost chargeback by team, cost center, or application.
- Configuring budget alerts before launching production workloads.
- Analyzing and optimizing existing GCP spend (rightsizing, CUDs, storage class).

## Skip If (ANY kills it)

- Personal sandbox projects with minimal spend — a single $10/month alert is sufficient; full export pipeline is over-engineering.
- Network cost analysis (egress, interconnect) — those require Traffic Analytics and billing exports combined with VPC Flow Logs.

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
