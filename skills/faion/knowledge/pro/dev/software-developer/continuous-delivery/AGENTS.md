---
slug: continuous-delivery
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Continuous Delivery is a software development practice where code changes are automatically prepared for release to production.
content_id: "358892d60eb7871d"
tags: [continuous-integration, continuous-delivery, deployment-pipeline, automation, feature-flags]
---
# Continuous Delivery (CD)

## Summary

**One-sentence:** Continuous Delivery is a software development practice where code changes are automatically prepared for release to production.

**One-paragraph:** Continuous Delivery is a software development practice where code changes are automatically prepared for release to production. It expands on Continuous Integration by ensuring that code is always in a deployable state. Every change that passes automated tests can be released to production with the push of a button.

## Applies If (ALL must hold)

- Web applications and SaaS products needing frequent releases.
- Teams aiming to reduce deployment risk through smaller batches.
- When manual deployments cause bottlenecks or slow iteration.
- Projects requiring rapid iteration and quick feedback loops.
- Organizations seeking to reduce deployment stress and enable rollback.
- Regulated environments where audited, automated, repeatable releases beat manual change-control toil.
- DORA elite targets: deploy daily+, lead-time less than 1 hour, change failure rate less than 15%, MTTR less than 1 hour.

## Skip If (ANY kills it)

- Batched manual release contexts like firmware on shipped hardware or medical devices with formal validation per release.
- Teams without comprehensive automated tests or with flaky test suites; fix tests first before CD.
- Pre-MVP or pre-product-market-fit when deployment cost is a single git push; the machinery costs more than the wins.
- Solo projects with one production environment and no customers; daily local push is sufficient.
- Schema changes that are not backward-compatible-by-construction; without expand/contract discipline, CD turns bad migrations into downtime.

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

- parent skill: `pro/dev/software-developer/`
