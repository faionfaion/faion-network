# Agent Integration — PHPUnit Testing (Laravel)

## When to use
- Any Laravel/PHP project that ships to production — feature tests via `Tests\TestCase` + `RefreshDatabase` are the bedrock.
- API regression suites (status code, JSON shape, validation, auth).
- Service-layer unit tests for business rules independent of HTTP.
- Snapshot-style tests for serialized resources / mailables.
- CI pipelines where you want failure tracking and code coverage thresholds.

## When NOT to use
- Browser / end-to-end flows — use Laravel Dusk (or Playwright) instead.
- Performance tests — use Laravel Octane benchmarks or k6.
- When the team has migrated to Pest — Pest sits on top of PHPUnit but the DSL differs; agents should be told which one to follow.
- Pure static-analysis questions — PHPStan/Larastan catch type bugs faster than a PHPUnit test ever will.

## Where it fails / limitations
- `RefreshDatabase` runs migrations per test class; on >100 test classes it dominates CI time. Switch to `DatabaseTransactions` for read-heavy suites.
- Tests sharing a single Redis/queue mean parallel runs (`--parallel`) collide unless each suite namespaces keys.
- `Mail::fake()` / `Queue::fake()` don't interact — you must call them in the right order before triggering the action.
- Tests that hit external APIs flap; agents may write tests with raw `Http::get(...)` (no `Http::fake()`) and CI breaks on network blip.
- `assertJsonStructure` is permissive — it only checks keys, not types or extra fields. Combine with `assertJsonPath` and `assertJsonMissing` for tight contracts.
- Time-sensitive tests fail at midnight UTC unless `Carbon::setTestNow()` is used.

## Agentic workflow
A subagent writes the test alongside the feature it tests, in the same commit. For each new endpoint: a feature test that exercises the happy path, validation failures, and at least one auth/authorization failure. For each new service: a unit test mocking dependencies. The agent must run `php artisan test --parallel --coverage --min=80` and fail the commit if coverage drops below threshold. Use `--filter` for tight feedback loops while iterating.

### Recommended subagents
- `faion-sdd-executor-agent` — pairs implementation with mandatory tests as a quality gate.
- `/faion` (sdd-batch-orchestrator workflow) — slice work where the test step is non-skippable.

### Prompt pattern
```
Write Tests\Feature\<Name>Test covering the new <route>. Include: happy path, missing-field validation, type-validation failure, unauthorized (no token), forbidden (wrong policy), 404 not-found. Use RefreshDatabase, Http::fake() for any outgoing call, Mail::fake() for mailables. Do NOT hit any real network. Run php artisan test --filter=<Name> and report.
```

```
Audit the test for hidden coupling: list every global state it mutates (cache, session, config, Carbon::now) and add a setUp/tearDown reset for each.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan test` | Wraps PHPUnit with Laravel niceties (`--parallel`, `--coverage`, `--filter`) | Built-in |
| `vendor/bin/phpunit` | Raw runner | Composer |
| `vendor/bin/pest` | Pest DSL on top of PHPUnit | `composer require --dev pestphp/pest` |
| `vendor/bin/phpunit --coverage-html` | HTML coverage report | Requires Xdebug or PCOV |
| `vendor/bin/infection` | Mutation testing | https://infection.github.io |
| `vendor/bin/paratest` | Parallel PHPUnit (older alternative to `--parallel`) | Composer |
| `vendor/bin/phpstan` (with strict) | Type checking, complementary to tests | Composer |
| `php artisan dusk` | Browser tests | `composer require --dev laravel/dusk` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | `actions/setup-php` + cached `vendor/`. |
| Codecov / Coveralls | SaaS | Yes | Upload `coverage.xml`; PR comments. |
| Chipper CI / GitLab CI | SaaS / OSS | Yes | Laravel-aware runners. |
| Laravel Dusk Selenium grid | OSS | Yes | For browser tests adjacent to PHPUnit. |
| Mockery | OSS | Yes | Bundled with Laravel; preferred over PHPUnit's mock builder. |
| HTTP Faker / WireMock | OSS | Yes | When `Http::fake()` is too coarse. |
| Faker / Laravel Factories | OSS | Yes | Already configured per Laravel skeleton. |

## Templates & scripts
See templates.md and the README's Feature Tests + Unit Tests sections. Inline `phpunit.xml.dist` snippet emphasizing parallel-safe defaults:

```xml
<phpunit bootstrap="vendor/autoload.php" colors="true" cacheDirectory=".phpunit.cache">
    <testsuites>
        <testsuite name="Unit"><directory>tests/Unit</directory></testsuite>
        <testsuite name="Feature"><directory>tests/Feature</directory></testsuite>
    </testsuites>
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="BCRYPT_ROUNDS" value="4"/>
        <env name="CACHE_DRIVER" value="array"/>
        <env name="MAIL_MAILER" value="array"/>
        <env name="QUEUE_CONNECTION" value="sync"/>
        <env name="SESSION_DRIVER" value="array"/>
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE" value=":memory:"/>
    </php>
</phpunit>
```

## Best practices
- One assertion concept per test method; share setup via factories or `setUp()`.
- Use factories (`User::factory()->create(...)`) over inline arrays — keeps tests resilient to schema changes.
- Always `Http::fake()` outgoing HTTP and assert on the recorded requests with `Http::assertSent`.
- `Bus::fake()` / `Queue::fake()` / `Mail::fake()` / `Notification::fake()` / `Event::fake()` — fake what you don't want to fire, then assert dispatch.
- Pin `BCRYPT_ROUNDS=4` in `phpunit.xml.dist` — bcrypt cost dominates auth-heavy suites otherwise.
- Use SQLite `:memory:` for unit-y suites; for migrations relying on Postgres/MySQL syntax, use the real DB via Docker.
- Run mutation testing (Infection) on critical modules monthly — coverage % alone hides logic bugs.
- Treat `assertJsonPath` as the default; reserve `assertJson` for exact-shape contracts.

## AI-agent gotchas
- Agents write `assertEquals(200, $response->status())` instead of `$response->assertOk()`. Force the Laravel-flavored assertions — they produce better error diffs.
- Tests that pass locally but fail in CI: usually because the agent forgot `RefreshDatabase` or `WithoutMiddleware` shadows real auth checks. Reject `WithoutMiddleware` unless explicitly justified.
- Mocking Eloquent: agents mock query builders with `Mockery` and produce brittle, false-positive tests. Steer toward integration tests with `RefreshDatabase` + factories — the DB is fast enough.
- Snapshot-like tests via `assertJson` with full payload break on every minor change. Use `assertJsonPath` to assert only the fields the test cares about.
- Time-dependent tests: agents call `now()->addDay()` in production code and don't `Carbon::setTestNow()` in tests, leading to flaky failures. Always freeze time at the start of the test.
- Human checkpoint: review every `actingAs($user)` — agents bypass authorization checks and don't realize the test no longer covers the policy. Add a separate "non-owner gets 403" test.
- Coverage gaming: agents add asserts on the response status only to lift coverage. Require at least one body/structure assertion per request test.

## References
- https://laravel.com/docs/testing
- https://laravel.com/docs/http-tests
- https://phpunit.de/documentation.html
- https://pestphp.com (modern alternative DSL)
- https://infection.github.io (mutation testing)
