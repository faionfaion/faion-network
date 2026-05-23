---
slug: php-laravel
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Umbrella Laravel 10/11 methodology — controller / service / Eloquent / queue / test layering, with sub-methodologies for patterns, Eloquent, queues, PHPUnit.
content_id: "a1d6ee772f52a974"
complexity: medium
produces: code
est_tokens: 3800
tags: [laravel, php, web-framework, backend]
---
# PHP Laravel Backend Development

## Summary

**One-sentence:** Umbrella Laravel 10/11 methodology — controller / service / Eloquent / queue / test layering, with sub-methodologies for patterns, Eloquent, queues, PHPUnit.

**One-paragraph:** Umbrella methodology that aggregates the four Laravel 10/11 sub-methodologies — `php-laravel-patterns` (controller / service / FormRequest decomposition), `php-eloquent` (ORM discipline), `php-laravel-queues` (Horizon + idempotency), `php-phpunit-testing` (Pest / PHPUnit layering). Use this entry point when an agent needs to plan a Laravel feature end-to-end (HTTP + persistence + tests + background work). Defaults: thin controllers, `$request->validated()`, `DB::transaction` for multi-write, `with(...)` eager-load, `Model::preventLazyLoading` in dev, `ShouldBeUnique` on mutating jobs, Pest feature tests with `RefreshDatabase`.

**Ефективно для:**

- New service or solo-dev SaaS where Laravel's batteries-included posture compresses delivery time.
- Internal tools, B2B SaaS, content sites, marketplaces — Laravel's sweet spot.
- Single entry point for an agent to plan a Laravel feature end-to-end (controller + Eloquent + tests + queue).
- Refactoring legacy Laravel app onto the canonical conventions before LLM agents touch it.

## Applies If (ALL must hold)

- New or existing Laravel 10/11 app on PHP 8.2+.
- HTTP API or full-stack web surface; background work via queue.
- Codebase ready to adopt canonical conventions across HTTP / ORM / queue / tests.

## Skip If (ANY kills it)

- Hard real-time / low-latency (<10 ms) APIs — PHP request lifecycle is per-request bootstrap; reach for Go / Rust or Laravel Octane only after benchmarking.
- Heavy CPU / data pipelines — use Python (pandas), Spark, or Go.
- Microservice mesh with strict contract boundaries — Laravel's Active Record + facades encourage shortcuts; pick a hexagonal stack.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Feature spec | Markdown | product |
| Eloquent model list | Markdown | data modelling |
| Test policy | text (Pest / PHPUnit) | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel-patterns]] | Sub-module for layered architecture. |
| [[php-eloquent]] | Sub-module for ORM discipline. |
| [[php-phpunit-testing]] | Sub-module for test layering. |
| [[decomposition-laravel]] | Sub-module for Action + DTO decomposition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: route-to-sub-methodology, php-version-floor, queue-driver-not-sync-in-prod, env-secrets-not-config-cache-leak, scheduler-runs-via-supervisor | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Laravel umbrella manifest + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: sync-queue-in-prod, env-in-vcs, scheduler-cron-not-supervised, php-version-floor-violated | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: route to sub-methodology → version + env check → install queue worker → wire scheduler → harden tests | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-feature` | sonnet | Picks the right sub-methodology mix. |
| `bootstrap-project` | sonnet | Multi-file scaffold. |
| `audit-conventions` | haiku | Mechanical scan against rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum viable Laravel project structure reference. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-laravel.py` | Validate the Laravel umbrella manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[php-laravel-patterns]]
- [[php-eloquent]]
- [[php-phpunit-testing]]
- [[decomposition-laravel]]
- [[laravel-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (feature shape — HTTP / queue / Eloquent / test) to the right sub-methodology + a rule from `01-core-rules.xml`. Use it before scaffolding a new feature.
