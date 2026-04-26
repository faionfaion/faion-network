# PHPUnit Testing (Laravel)

## Summary

Layered PHPUnit/Pest testing for Laravel: Feature tests drive HTTP endpoints via `getJson`/`postJson`/`assertJsonPath`; Unit tests cover services and value objects without booting Laravel. `*::fake()` calls go before the action under test. `assertJsonPath` over `assertJsonStructure` — path checks values, structure only checks key existence. One behavior per test method; name describes the behavior.

## Why

Feature tests are the highest-value signal for API correctness: they exercise routing, middleware, validation, and the service layer together via the HTTP interface. Separating Feature (`tests/Feature/`) from Unit (`tests/Unit/`) keeps the `RefreshDatabase` trait off pure logic tests, which cuts suite time significantly. `assertJsonPath('data.email', $expected)` is specific enough to fail on wrong values; `assertJsonStructure` passes even if all values are null. Calling `*::fake()` after the action is a silent false positive — the fake captures nothing.

## When To Use

- Feature tests against Laravel HTTP endpoints (`getJson`, `postJson`, etc.).
- Unit tests for services, value objects, or domain logic that should not boot the full framework.
- Database integration tests with `RefreshDatabase` on Feature tests touching real DB.
- CI regression suites gating PRs with `--coverage --min=80`.

## When NOT To Use

- Browser/E2E UI tests — use Laravel Dusk or Playwright.
- Performance/load testing — use k6, Locust, or Apache Bench.
- Code with no business logic (thin Eloquent calls only) — cover at integration level instead.
- Tests needing live third-party APIs — use `spatie/laravel-http-recorder` cassettes or contract tests.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Feature vs Unit classification, fake-before-act rule, `assertJsonPath` preference, factory patterns. |
| `content/02-examples.xml` | Feature test covering CRUD endpoints, Unit test with `Event::fake()` and Mockery. |
| `content/03-antipatterns.xml` | `assertJsonStructure` overuse, fake after act, `RefreshDatabase` on Unit tests, mixed Pest/PHPUnit syntax. |

## Templates

| File | Purpose |
|------|---------|
| `templates/FeatureTest.php` | Feature test skeleton: `RefreshDatabase`, `actingAs`, `assertJsonPath`, all HTTP verbs. |
| `templates/UnitServiceTest.php` | Unit test skeleton: Mockery mock, `Event::fake()` before act, no `RefreshDatabase`. |
| `templates/phpunit.xml` | PHPUnit config: SQLite in-memory, sync queue, random execution order, strict warnings. |
