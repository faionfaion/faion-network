---
slug: php-phpunit-testing
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Laravel PHPUnit test patterns: feature tests via Tests\TestCase + RefreshDatabase covering happy path, validation failures, auth/authorization failures, and 404s; unit tests mocking dependencies; and Http::fake() / Queue::fake() / Mail::fake() for all outgoing side effects.
content_id: "02351dbb4c5f90ef"
tags: [php, phpunit, laravel, testing, feature-tests]
---
# PHPUnit Testing (Laravel)

## Summary

**One-sentence:** Laravel PHPUnit test patterns: feature tests via Tests\TestCase + RefreshDatabase covering happy path, validation failures, auth/authorization failures, and 404s; unit tests mocking dependencies; and Http::fake() / Queue::fake() / Mail::fake() for all outgoing side effects.

**One-paragraph:** Laravel PHPUnit test patterns: feature tests via Tests\TestCase + RefreshDatabase covering happy path, validation failures, auth/authorization failures, and 404s; unit tests mocking dependencies; and Http::fake() / Queue::fake() / Mail::fake() for all outgoing side effects. One assertion concept per test method. Use $response->assertOk() (Laravel-flavored assertions), assertJsonPath for field-level contracts, and Carbon::setTestNow() for time-sensitive assertions.

## Applies If (ALL must hold)

- Any Laravel/PHP project shipping to production — feature tests are the bedrock.
- API regression suites (status code, JSON shape, validation, auth).
- Service-layer unit tests for business rules independent of HTTP.
- CI pipelines requiring coverage thresholds and failure tracking.

## Skip If (ANY kills it)

- Browser / end-to-end flows — use Laravel Dusk (Playwright) instead.
- Performance tests — use k6 or Octane benchmarks.
- When the team has migrated to Pest — same underlying PHPUnit but the DSL differs; tell the agent which one.
- Pure static-analysis questions — PHPStan/Larastan catch type bugs faster than a test.

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
