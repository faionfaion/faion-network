---
slug: platform-engineering
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Internal Developer Platforms (IDP) reduce cognitive load and accelerate delivery.
content_id: "0a18b49bf05d9c57"
tags: [platform-engineering, idp, backstage, developer-experience, devops]
---
# Platform Engineering

## Summary

**One-sentence:** Internal Developer Platforms (IDP) reduce cognitive load and accelerate delivery.

**One-paragraph:** Internal Developer Platforms (IDP) reduce cognitive load and accelerate delivery. Developers spend 40%+ time on infrastructure instead of features. Tool fragmentation causes 75% of developers to lose 6+ hours weekly. Solution: make the right way the easy way by creating well-lit paths that guide developers toward good practices while allowing flexibility when needed.

## Applies If (ALL must hold)

- 50+ engineer org where DevOps tickets become a queue and onboarding takes weeks.
- Multi-tenant infrastructure with shared Kubernetes / cloud accounts and inconsistent provisioning.
- When standardizing "golden paths" — opinionated app templates, CI workflows, observability defaults.
- Compliance environments (SOC2, HIPAA) where guardrails must be enforced, not documented.
- Migrating from Heroku/render-style PaaS to in-house cloud, while keeping developer ergonomics.
- AI-agent fleets that need RBAC, quota, and scope just like humans (2026 pattern).

## Skip If (ANY kills it)

- Solo or <10-person teams. Building an IDP for 5 devs is over-engineering; pick a managed PaaS.
- When the actual bottleneck is product/discovery, not infra friction. Platform won't fix unclear roadmaps.
- Greenfield with no production workloads — wait until you have ≥3 services and ≥10 deploys/week to learn what to abstract.
- Strict regulatory environments where central infra team must own every change (platform abstraction can hide compliance-relevant detail).

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
