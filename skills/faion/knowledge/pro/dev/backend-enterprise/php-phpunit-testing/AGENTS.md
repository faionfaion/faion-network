---
slug: php-phpunit-testing
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Layered PHPUnit/Pest testing for Laravel: Feature tests drive HTTP endpoints via getJson/postJson/assertJsonPath; Unit tests cover services and value objects without booting Laravel.
content_id: "02351dbb4c5f90ef"
tags: [phpunit, pest, laravel, testing, feature-tests]
---
# PHPUnit Testing for Laravel

## Summary

**One-sentence:** Layered PHPUnit/Pest testing for Laravel: Feature tests drive HTTP endpoints via getJson/postJson/assertJsonPath; Unit tests cover services and value objects without booting Laravel.

**One-paragraph:** Layered PHPUnit/Pest testing for Laravel: Feature tests drive HTTP endpoints via getJson/postJson/assertJsonPath; Unit tests cover services and value objects without booting Laravel. *::fake() calls go before the action under test. assertJsonPath over assertJsonStructure — path checks values, structure only checks key existence. One behavior per test method; name describes the behavior.

## Applies If (ALL must hold)

- Feature tests against Laravel HTTP endpoints (getJson, postJson, etc.).
- Unit tests for services, value objects, or domain logic that should not boot the full framework.
- Database integration tests with RefreshDatabase on Feature tests touching real DB.
- CI regression suites gating PRs with --coverage --min=80.

## Skip If (ANY kills it)

- Browser/end-to-end UI tests — use Laravel Dusk or Playwright.
- Performance/load testing — use k6, Locust, or Apache Bench.
- Code with no business logic (thin Eloquent calls only) — testing here is low-value; cover at integration level instead.
- Tests that need real third-party APIs hit live — use VCR-style cassettes (spatie/laravel-http-recorder) or contract tests.

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
