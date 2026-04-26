# PHPUnit Testing (Laravel)

## Summary

Laravel PHPUnit test patterns: feature tests via `Tests\TestCase` + `RefreshDatabase` covering happy path, validation failures, auth/authorization failures, and 404s; unit tests mocking dependencies; and `Http::fake()` / `Queue::fake()` / `Mail::fake()` for all outgoing side effects. One assertion concept per test method. Use `$response->assertOk()` (Laravel-flavored assertions), `assertJsonPath` for field-level contracts, and `Carbon::setTestNow()` for time-sensitive assertions.

## Why

Feature tests that hit routes via `actingAs($user)->postJson(...)` give the highest confidence for the lowest mocking cost. Laravel's test helpers (`RefreshDatabase`, `Http::fake()`, factory system) make it practical to write full-stack tests without hitting real external services. Mutation testing (Infection) catches logic bugs that coverage percent misses. Pairing each new endpoint with a test in the same commit prevents coverage drift.

## When To Use

- Any Laravel/PHP project shipping to production — feature tests are the bedrock.
- API regression suites (status code, JSON shape, validation, auth).
- Service-layer unit tests for business rules independent of HTTP.
- CI pipelines requiring coverage thresholds and failure tracking.

## When NOT To Use

- Browser / end-to-end flows — use Laravel Dusk (Playwright) instead.
- Performance tests — use k6 or Octane benchmarks.
- When the team has migrated to Pest — same underlying PHPUnit but the DSL differs; tell the agent which one.
- Pure static-analysis questions — PHPStan/Larastan catch type bugs faster than a test.

## Content

| File | What's inside |
|------|---------------|
| `content/01-feature-tests.xml` | Feature test structure, assertOk/assertCreated/assertUnprocessable, assertJsonPath, factory usage |
| `content/02-unit-tests.xml` | Service unit tests, mock repositories, event assertions, password hashing verification |
| `content/03-antipatterns.xml` | assertEquals(200) vs assertOk, WithoutMiddleware hiding auth, raw assertJson, Carbon without setTestNow |

## Templates

| File | Purpose |
|------|---------|
| `templates/phpunit.xml` | phpunit.xml.dist with parallel-safe env: SQLite in-memory, array cache/mail/queue, BCRYPT_ROUNDS=4 |
| `templates/feature-test.php` | Feature test skeleton: RefreshDatabase, Http::fake, five test methods per endpoint |
