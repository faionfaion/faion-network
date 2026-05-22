---
slug: gcp-landing-zone
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A GCP landing zone (cloud foundation) is a modular configuration enabling enterprise adoption of Google Cloud.
content_id: "1e5e4d021896cbc6"
tags: [gcp, landing-zone, terraform, iam, organization]
---
# GCP Landing Zone Design

## Summary

**One-sentence:** A GCP landing zone (cloud foundation) is a modular configuration enabling enterprise adoption of Google Cloud.

**One-paragraph:** A GCP landing zone (cloud foundation) is a modular configuration enabling enterprise adoption of Google Cloud. It establishes resource hierarchy, IAM, network architecture, security controls, and monitoring as a reusable foundation before any workload is deployed.

## Applies If (ALL must hold)

- Starting a new GCP organization or migrating from another cloud.
- Setting up multi-environment (production, staging, development) project structures.
- Enforcing org-wide security policies (no SA keys, no public IPs, location restrictions).
- Deploying a Shared VPC host project for centralized network administration.
- Establishing FinOps foundations: billing export, budgets, cost labels.

## Skip If (ANY kills it)

- Single-project proofs of concept — org-level setup overhead is not justified.
- Personal/sandbox accounts without an organization — many controls require org node.

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
