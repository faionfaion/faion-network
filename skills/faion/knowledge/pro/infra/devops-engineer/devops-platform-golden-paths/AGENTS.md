---
slug: devops-platform-golden-paths
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Golden paths are pre-built, opinionated templates for the most common developer tasks (new service, database provisioning, API gateway).
content_id: "fe8d7bc3755713b4"
tags: [golden-paths, platform-engineering, scaffolding, developer-experience, templates]
---
# Golden Paths: Opinionated Self-Service Templates for Developer Platforms

## Summary

**One-sentence:** Golden paths are pre-built, opinionated templates for the most common developer tasks (new service, database provisioning, API gateway).

**One-paragraph:** Golden paths are pre-built, opinionated templates for the most common developer tasks (new service, database provisioning, API gateway). They bundle CI/CD, observability, security scanning, and environment configs into a single form-submit action. Developer effort drops from days to minutes while best practices are enforced by default, not by policy review.

## Applies If (ALL must hold)

- Creating a new microservice, API, worker process, or frontend application in a team with established infrastructure patterns.
- Provisioning a database or cache with standard security, backup, and monitoring requirements.
- Setting up an API gateway with authentication, rate limiting, and OpenAPI documentation.
- Any repeated infrastructure setup task performed more than 5 times per month across teams.

## Skip If (ANY kills it)

- One-off or experimental infrastructure with no future reuse — template overhead exceeds value.
- Highly customized architectures that deviate from org standards — use the escape hatch and document the deviation.
- Prototype or throwaway services — use the simplest possible setup; golden paths assume production lifecycle.

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
