---
slug: finops-governance
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The OPERATE phase makes cost efficiency self-sustaining through automated policies, budget alerts at multiple thresholds, scheduled dev/test automation, and cost gates embedded in CI/CD pipelines.
content_id: "47c513a09a508c2a"
tags: [finops, governance, budget-management, automation, cicd-cost-gates]
---
# FinOps Governance: Policies, Budgets, and CI/CD Cost Gates

## Summary

**One-sentence:** The OPERATE phase makes cost efficiency self-sustaining through automated policies, budget alerts at multiple thresholds, scheduled dev/test automation, and cost gates embedded in CI/CD pipelines.

**One-paragraph:** The OPERATE phase makes cost efficiency self-sustaining through automated policies, budget alerts at multiple thresholds, scheduled dev/test automation, and cost gates embedded in CI/CD pipelines. It converts one-time optimization into continuous governance so new workloads do not erode savings.

## Applies If (ALL must hold)

- INFORM phase complete — visibility and tagging are established.
- Teams deploying infrastructure via IaC (Terraform, CloudFormation, Pulumi) — cost gates are implementable.
- Dev/test environments running overnight and on weekends, generating avoidable spend.
- Budget overruns discovered only on monthly invoice — need proactive alerts.
- Engineering teams making architecture decisions without cost signal.

## Skip If (ANY kills it)

- INFORM phase incomplete — governance without visibility enforces the wrong things.
- Flat-fee infrastructure — no elastic costs to gate or automate.
- Strictly regulated environments where automated shutdown/modification requires change-control approval.

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
