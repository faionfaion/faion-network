# PHPUnit Testing for Laravel

## Summary

**One-sentence:** Layered PHPUnit/Pest testing for Laravel — Feature tests drive HTTP via getJson/postJson + assertJsonPath, Unit tests cover services without booting Laravel, RefreshDatabase + factories + fakes wired before the SUT runs.

**One-paragraph:** Layered PHPUnit / Pest testing for Laravel 10/11. Feature tests drive HTTP endpoints via `getJson`, `postJson`, `assertJsonPath`. Unit tests cover services and value objects without booting Laravel. `Mail::fake()`, `Queue::fake()`, `Event::fake()`, `Http::fake()` are called before the action under test. Assertions use `assertJsonPath` (value check) over `assertJsonStructure` (key-existence only). Each test exercises one behaviour; the method name describes the behaviour. Feature tests touching DB use `RefreshDatabase`. CI gates PRs at `--coverage --min=80`.

**Ефективно для:**

- Feature tests against Laravel HTTP endpoints (`getJson`, `postJson`, etc.).
- Unit tests for services, value objects, or domain logic that should not boot the full framework.
- Database integration tests with `RefreshDatabase` on Feature tests touching real DB.
- CI regression suites gating PRs with `--coverage --min=80`.

## Applies If (ALL must hold)

- Laravel 10/11 service standardised on Pest 2+ or PHPUnit 10+.
- HTTP API surface with at least one mutating endpoint.
- Test DB available (sqlite for unit, postgres / mysql for integration).

## Skip If (ANY kills it)

- Browser / end-to-end UI tests — use Laravel Dusk or Playwright.
- Performance / load testing — use k6, Locust, or Apache Bench.
- Code with no business logic (thin Eloquent calls only) — testing here is low-value; cover at integration level instead.
- Tests that need real third-party APIs hit live — use VCR-style cassettes (`spatie/laravel-http-recorder`) or contract tests.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Endpoint list under test | Markdown | API contract |
| Factory definitions | PHP factory classes | data modelling |
| Coverage threshold | int | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Umbrella for queue / scheduler setup. |
| [[php-laravel-patterns]] | Layering that drives Feature vs Unit boundary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: feature-vs-unit-boundary, refreshdatabase-on-feature, fakes-before-action, assertjsonpath-not-structure, one-behaviour-per-test, coverage-gate-in-ci | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the test-plan manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: unit-tests-booting-laravel, fake-after-action, assertjsonstructure-misuse, shared-mutable-fixture, time-based-flakes | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold suite → factories + fakes → feature tests → unit tests → coverage gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-feature-test` | sonnet | HTTP path + assertions synthesis. |
| `generate-unit-test` | sonnet | Pure logic test design. |
| `audit-fake-placement` | haiku | Mechanical scan for fakes called after action. |

## Templates

| File | Purpose |
|------|---------|
| `templates/FeatureTest.php` | Feature test skeleton with RefreshDatabase + Mail::fake + assertJsonPath. |
| `templates/UnitServiceTest.php` | Plain Pest unit test skeleton (no Laravel boot). |
| `templates/phpunit.xml` | phpunit.xml configuration with coverage + bootstrapping. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-phpunit-testing.py` | Validate the test-plan manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[php-laravel]]
- [[php-laravel-patterns]]
- [[php-eloquent]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (layer under test, persistence dependency, third-party calls) to a rule from `01-core-rules.xml`. Use it before authoring a test class.
