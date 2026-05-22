---
slug: php-laravel
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Laravel backend patterns for production-grade applications: controller structure, service layer, repository pattern, testing, and job queues.
content_id: "2bb6a9d655536100"
tags: [laravel, php, web-framework, backend]
---
# PHP Laravel Backend Development

## Summary

**One-sentence:** Laravel backend patterns for production-grade applications: controller structure, service layer, repository pattern, testing, and job queues.

**One-paragraph:** Laravel backend patterns for production-grade applications: controller structure, service layer, repository pattern, testing, and job queues. This is an umbrella methodology encompassing four sub-methodologies: php-laravel-patterns, php-eloquent, php-laravel-queues, and php-phpunit-testing.

## Applies If (ALL must hold)

- New service or solo-dev SaaS where Laravel's batteries-included posture materially compresses delivery time.
- Internal tools, B2B SaaS, content sites, marketplaces — Laravel's sweet spot.
- You need a single entry point for an agent to plan a Laravel feature end-to-end (controller + Eloquent + tests + queue), pulling from the four sub-methodologies in this group.

## Skip If (ANY kills it)

- Hard real-time / low-latency (<10 ms) APIs — PHP request lifecycle is per-request bootstrap; reach for Go, Rust, or Laravel Octane only after benchmarking.
- Heavy CPU/data pipelines — use Python (pandas), Spark, or Go.
- Microservice mesh with strict contract boundaries — Laravel's Active Record + facades encourage shortcuts that break contracts; pick a hexagonal stack.

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

- parent skill: `pro/dev/backend-enterprise/`
