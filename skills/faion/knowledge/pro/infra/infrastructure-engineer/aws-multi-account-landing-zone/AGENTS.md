---
slug: aws-multi-account-landing-zone
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A landing zone is the foundational multi-account AWS environment: an Organizations structure, OU hierarchy, Control Tower (or Landing Zone Accelerator), service control policies, centralized logging, and IAM Identity Center integration.
content_id: "abbb7b4bb342efb9"
tags: [aws, multi-account, landing-zone, organizations, control-tower]
---
# AWS Multi-Account Landing Zone Design

## Summary

**One-sentence:** A landing zone is the foundational multi-account AWS environment: an Organizations structure, OU hierarchy, Control Tower (or Landing Zone Accelerator), service control policies, centralized logging, and IAM Identity Center integration.

**One-paragraph:** A landing zone is the foundational multi-account AWS environment: an Organizations structure, OU hierarchy, Control Tower (or Landing Zone Accelerator), service control policies, centralized logging, and IAM Identity Center integration. It isolates blast radius, enforces governance at scale, and enables consistent security posture across all workloads.

## Applies If (ALL must hold)

- Bootstrapping a new AWS organization from scratch or formalizing an ad-hoc multi-account setup.
- Compliance requirements (GDPR, HIPAA, PCI-DSS, SOC2) that mandate environment isolation and centralized logging.
- Organizations with 3+ development teams where quota and billing isolation is necessary.
- Any production workload requiring auditable org-level CloudTrail and immutable log storage.

## Skip If (ANY kills it)

- Single-account hobby or prototype projects — Control Tower and LZA overhead is wasteful for a solo developer or throwaway environment.
- Pure application-layer decisions — use dev skills instead.
- Non-AWS clouds — this pattern is AWS-specific; use gcp-arch-basics for GCP equivalents.

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
