---
slug: iac-patterns-testing
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A four-level testing pyramid for Terraform modules: static analysis catches syntax and policy errors in seconds, native terraform test validates module contracts with plan-only or mock providers, Terratest deploys real resources for integration verification, and OPA/Conftest enforces compliance policies as code.
content_id: "448727c735a38286"
tags: [terraform, testing, terratest, opa, iac]
---
# IaC Testing Patterns

## Summary

**One-sentence:** A four-level testing pyramid for Terraform modules: static analysis catches syntax and policy errors in seconds, native terraform test validates module contracts with plan-only or mock providers, Terratest deploys real resources for integration verification, and OPA/Conftest enforces compliance policies as code.

**One-paragraph:** A four-level testing pyramid for Terraform modules: static analysis catches syntax and policy errors in seconds, native terraform test validates module contracts with plan-only or mock providers, Terratest deploys real resources for integration verification, and OPA/Conftest enforces compliance policies as code. Each level has a distinct cost/confidence tradeoff.

## Applies If (ALL must hold)

- Any reusable module — add at minimum static analysis + a plan-only terraform test before publishing.
- Modules that create security-sensitive resources (IAM, security groups, S3 buckets) — add OPA/Conftest policy tests.
- Modules consumed by multiple teams — add integration tests (Terratest) to validate real resource behavior.
- Pre-merge CI gates — run static analysis and plan tests on every PR; integration tests on merge to main.

## Skip If (ANY kills it)

- One-off root modules not intended for reuse — static analysis only is sufficient.
- Integration tests (Terratest) in a tight inner loop — they create real cloud resources; use plan-only tests for fast feedback during development.
- Policy tests when no compliance requirements exist — OPA rules need maintenance; don't add them speculatively.

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
