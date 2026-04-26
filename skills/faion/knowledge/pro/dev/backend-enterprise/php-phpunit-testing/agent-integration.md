# Agent Integration — PHPUnit Testing (Laravel)

## When to use
- Writing Laravel feature tests against HTTP endpoints (`getJson`, `postJson`, `assertJson*`).
- Unit tests for services, value objects, and domain logic that should not boot the full framework.
- Database integration tests with `RefreshDatabase` or `DatabaseTransactions`.
- Pre-merge regression suites that gate CI.

## When NOT to use
- Browser/end-to-end UI tests — use Laravel Dusk or Playwright.
- Performance/load testing — use k6, Locust, or Apache Bench.
- Tests that need real third-party APIs hit live — use VCR-style cassettes (`spatie/laravel-http-recorder`) or contract tests.
- Code that has no business logic (thin Eloquent calls only) — testing here is low-value; cover at integration level instead.

## Where it fails / limitations
- `RefreshDatabase` is per-test reset — slow on large schemas. `DatabaseTransactions` is faster but breaks for code that opens its own transactions.
- `Mockery` overlap with PHPUnit's mocking creates two ways to do the same thing; pick one per repo.
- `assertJsonStructure` checks keys exist, not types or values — easy false positives. Prefer `assertJsonPath` or `assertJson` with explicit values.
- Tests that hit `Mail::fake()`, `Queue::fake()`, `Bus::fake()`, `Event::fake()` must call the fake before the action — agent often inverts the order.
- `TestCase` boots the full app — heavy for unit tests. Use plain PHPUnit `TestCase` (not Laravel's) for pure logic.
- Pest and PHPUnit syntax cohabit awkwardly — agents mix them within one file.

## Agentic workflow
A coding subagent should: (1) classify the test as Feature (HTTP-driven) or Unit (single class) before writing, (2) place under `tests/Feature/` or `tests/Unit/` accordingly, (3) use `RefreshDatabase` only on Feature tests touching DB, (4) fake the right facade (`Queue::fake()`, `Mail::fake()`, `Notification::fake()`, `Bus::fake()`, `Event::fake()`, `Storage::fake('public')`, `Http::fake()`) before the act, (5) assert on the strongest available API (`assertJsonPath` over `assertJsonStructure`), (6) factory-driven setup via `User::factory()->has(Order::factory()->count(3))->create()`, (7) one behavior per test, name `test_<state>_<action>_<expected>`. Run `php artisan test --parallel` and `vendor/bin/phpstan analyse tests/` after each batch.

### Recommended subagents
- `general-purpose` Claude subagent — test scaffolding from controller signatures and existing factories.
- Code-review subagent (Sonnet) — flags weak assertions, missing fakes, leaky DB state, slow `RefreshDatabase` on Unit tests.

### Prompt pattern
```
Generate Feature test tests/Feature/<Resource>ControllerTest.php covering: index (auth + pagination), store (valid + validation failures per field), show (existing + 404), update (auth + ownership), destroy (auth + soft delete). Use RefreshDatabase. Use User::factory(). Use postJson/getJson/putJson/deleteJson. Assert with assertOk/assertCreated/assertUnprocessable + assertJsonPath. No assertJsonStructure unless asserting array shapes alongside paths.
```
```
Generate Unit test tests/Unit/Services/<Service>Test.php for <method>: arrange via factory or stub, act, assert. Mock dependencies via Mockery::mock(<Interface>::class). Use Event::fake() before service call to assert dispatched events. Do NOT use RefreshDatabase here — it's a unit test.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan test --parallel --recreate-databases` | Parallel run with isolated DBs | bundled |
| `php artisan test --filter=<TestMethod>` | Single test selector | bundled |
| `php artisan test --coverage --min=80` | Code coverage with threshold gate | requires Xdebug or PCOV |
| `vendor/bin/pest --parallel` | Pest runner (alternative syntax) | https://pestphp.com |
| `vendor/bin/phpstan analyse tests/` (Larastan) | Static analysis on tests | https://github.com/larastan/larastan |
| `vendor/bin/infection` | Mutation testing — measure assertion strength | https://infection.github.io |
| `vendor/bin/paratest` | Parallel runner without Laravel wrapper | https://github.com/paratestphp/paratest |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions / GitLab CI | SaaS/OSS | Yes | Standard Laravel matrix: PHP × DB × Redis |
| Codecov / Coveralls | SaaS | Yes | Coverage badges + PR diff coverage |
| Testcontainers PHP | OSS | Yes | Real Postgres/MySQL/Redis in CI without docker-compose juggling |
| Laravel Dusk | OSS | Yes | Browser/UI tests — adjacent, complementary |
| Mockery / Prophecy | OSS | Yes | Mocking libraries; pick one per project |
| Mockoon / WireMock | OSS | Yes | Mock external APIs at the network layer when `Http::fake()` is too coarse |

## Templates & scripts
See `templates.md` for Feature and Unit test skeletons. Inline `phpunit.xml` excerpt the agent should ensure exists for fast, deterministic test runs:

```xml
<phpunit colors="true" stopOnFailure="false"
         cacheDirectory=".phpunit.cache" executionOrder="random"
         beStrictAboutTestsThatDoNotTestAnything="true"
         beStrictAboutOutputDuringTests="true"
         failOnRisky="true" failOnWarning="true">
  <testsuites>
    <testsuite name="Unit"><directory>tests/Unit</directory></testsuite>
    <testsuite name="Feature"><directory>tests/Feature</directory></testsuite>
  </testsuites>
  <php>
    <env name="APP_ENV" value="testing"/>
    <env name="DB_CONNECTION" value="sqlite"/>
    <env name="DB_DATABASE" value=":memory:"/>
    <env name="QUEUE_CONNECTION" value="sync"/>
    <env name="CACHE_STORE" value="array"/>
    <env name="MAIL_MAILER" value="array"/>
    <env name="SESSION_DRIVER" value="array"/>
    <env name="BCRYPT_ROUNDS" value="4"/>
  </php>
</phpunit>
```

## Best practices
- One behavior per test. Name describes the behavior, not the method (`test_listing_returns_paginated_users`, not `test_index`).
- Prefer `assertJsonPath('data.0.email', $expected)` over `assertJsonStructure([...])`. Path checks values; structure only checks keys.
- Always call `*::fake()` before the action under test; assertions go after.
- Use factories with relationships: `User::factory()->has(Post::factory()->count(3))->create()` over manual chaining.
- Mark slow integration tests with PHPUnit groups (`@group slow`) and exclude from default CI.
- Use `actingAs($user)` for auth, not manual `Auth::login` — it short-circuits middleware correctly.
- Keep DB tests on SQLite `:memory:` for speed, but run nightly on the real DB driver to catch dialect-specific bugs.

## AI-agent gotchas
- LLM forgets `RefreshDatabase` and tests pollute each other when run in random order.
- Generated assertions favor `assertJsonStructure` (low signal) — review must upgrade to `assertJsonPath`/`assertJson`.
- LLM places fake() calls AFTER the action — the assertion then sees an empty fake, false positives. Hard rule: fakes go at the top of the test method.
- `Mail::fake()` plus `Mail::send` inside a queued job — fake captures only sync sends. For queued mail, use `Notification::fake()` or `Queue::fake()` and assert the job was pushed.
- LLM mixes Pest and PHPUnit syntax in one file. Detect by extension/namespace and stick to one.
- `expectsExceptionMessage` matches substring — agent sometimes uses unstable strings (timestamps, IDs). Use `expectExceptionMessageMatches` with a regex.
- Coverage targets the LLM proposes (often 100%) lead to brittle tests. Pick semantic coverage: every public method has at least one happy + one failure path.
- Human checkpoint: changing CI failure thresholds (`--min=`), removing `failOnWarning`, or adding `--no-coverage` to default runs.

## References
- https://laravel.com/docs/testing
- https://laravel.com/docs/http-tests
- https://docs.phpunit.de/en/11.0/
- https://pestphp.com (alternative)
- https://infection.github.io (mutation testing)
- https://github.com/spatie/laravel-http-recorder (HTTP cassettes)
