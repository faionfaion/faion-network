---
slug: finops-framework
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: FinOps is a cultural practice that brings financial accountability to cloud spending through cross-functional collaboration between Engineering, Finance, and Business teams.
content_id: "101019bb7330c2b6"
tags: [finops, cloud-cost, governance, framework, cost-management]
---
# FinOps Framework: Cloud Financial Operations

## Summary

**One-sentence:** FinOps is a cultural practice that brings financial accountability to cloud spending through cross-functional collaboration between Engineering, Finance, and Business teams.

**One-paragraph:** FinOps is a cultural practice that brings financial accountability to cloud spending through cross-functional collaboration between Engineering, Finance, and Business teams. It operates in three phases — INFORM (visibility), OPTIMIZE (efficiency), OPERATE (governance) — and addresses a market where 32% of $723.4B annual cloud spend is wasted.

## Applies If (ALL must hold)

- Cloud bill above $5k/month and growing 20%+ month-over-month with no per-team visibility.
- Multi-team or multi-product engineering org needing showback or chargeback reporting.
- Pre-IPO or due-diligence phase requiring credible unit economics ($/customer, $/transaction, $/inference).
- Reserved Instance or Savings Plan renewal approaching — need data-driven commitment sizing.
- Kubernetes cluster shared across teams where pods are unaccounted.
- CFO or board flagged cloud cost as a top-3 P&L concern.
- Untagged spend exceeds 20% of bill — allocation impossible without remediation.

## Skip If (ANY kills it)

- Cloud bill below $1k/month — FinOps tooling overhead exceeds savings; eyeball billing weekly instead.
- Workloads on flat-fee infrastructure (bare metal, fixed VPS) — no elastic cost to optimize.
- Crisis cost-cutting that cannot wait — apply blunt instruments first (turn off non-prod overnight, kill orphan resources), then formalize FinOps.
- Strictly regulated workloads where security/compliance trumps cost (dedicated HSMs, isolated tenancy).

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
