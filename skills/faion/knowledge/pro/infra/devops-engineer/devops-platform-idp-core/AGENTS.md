---
slug: devops-platform-idp-core
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An IDP is a self-service layer between developers and infrastructure.
content_id: "20d7d9aa49dda9f6"
tags: [platform-engineering, idp, developer-experience, self-service, cognitive-load]
---
# Internal Developer Platform (IDP) Core Concepts

## Summary

**One-sentence:** An IDP is a self-service layer between developers and infrastructure.

**One-paragraph:** An IDP is a self-service layer between developers and infrastructure. It absorbs infrastructure complexity so developers provision resources, deploy applications, and manage services without becoming infrastructure experts. By 2026, 80% of large software engineering orgs have platform teams (Gartner).

## Applies If (ALL must hold)

- Engineering org with 20+ developers where infrastructure requests are a bottleneck.
- Multiple teams repeatedly solving the same infrastructure problems independently.
- Onboarding time for new developers exceeds 1 week due to environment setup complexity.
- DevOps/Ops ticket queue dominates team capacity (over 30% of requests are repetitive).
- Need to enforce security, compliance, or cost standards across many services consistently.

## Skip If (ANY kills it)

- Teams under 10 developers — overhead of building a platform exceeds value; shared runbooks suffice.
- Single-service or single-language projects — a Makefile and a CI template provide equivalent self-service at near-zero cost.
- Early-stage startups pre-product-market-fit — platform investment delays product iteration; standardize later.
- Orgs without dedicated platform team capacity — an unmaintained IDP becomes a blocker, not an enabler.

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
