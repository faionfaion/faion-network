# Agent Integration — Eloquent Patterns (Laravel ORM)

## When to use
- Building a Laravel API/web app where the data layer is non-trivial (≥5 related entities, soft deletes, polymorphic relations).
- Refactoring controllers/services that build raw queries inline — extract to scopes, repositories, or query objects.
- Adding read-side optimizations (eager loading, chunking, lazy collections) in response to a measured N+1 problem.
- Multi-tenant or role-gated apps where global scopes + policies enforce data boundaries at the model layer.
- LLM-driven greenfield work where models are the primary "schema-of-truth" the agent reasons about.

## When NOT to use
- Read-heavy analytics workloads — use raw `DB::` query builder, `chunkById`, or jump to Postgres directly. Eloquent hydration is the bottleneck.
- High-throughput event ingestion (>5k req/s on a single box) — bypass Eloquent for inserts; use `DB::table()->insert()` or `LazyCollection`.
- Cross-database joins or non-RDBMS backends (Cassandra, DynamoDB, ClickHouse). Eloquent's relation API assumes a single SQL connection per query.
- Microservices where each service is <1k LOC and a single repository class adds more ceremony than it saves.

## Where it fails / limitations
- **N+1 by default.** Relations are lazy; agents copying examples without `->with()` ship N+1 bugs into prod. Detection requires Telescope/Debugbar in dev.
- **Mass assignment footguns.** `$fillable` vs `$guarded` mistakes leak fields agents weren't asked to expose (e.g., `is_admin`, `password_hash`).
- **Global scopes are invisible.** A global `tenant_id` scope hides rows; agents debugging "missing data" rarely think to call `withoutGlobalScopes()`.
- **Soft deletes silently mutate queries.** `forceDelete`, `withTrashed`, `onlyTrashed` are easy to forget — agents emit "delete works" tests that pass while data lingers.
- **Repository pattern is contested in Laravel.** Many maintainers consider it ceremony; only adopt when the team has a real swap-out case (multiple data sources, mocking strategy).
- **Accessor/mutator collisions.** New `Attribute::make()` API and old `getXAttribute` coexist; agents mixing both produce undefined behavior.
- **Polymorphic relation typos.** A bad morph map silently writes wrong class strings; integrity is not enforced at the DB level.

## Agentic workflow
Drive Eloquent work as: (1) a planner subagent reads the current models + migrations and emits a target schema diff; (2) a code-writer subagent generates models, migrations, factories, and seeders together; (3) a test subagent writes feature tests that hit real DB (sqlite in-memory) with `RefreshDatabase`; (4) a perf subagent runs the test suite under Laravel Debugbar/Clockwork and flags any query count >N or any single query >100ms. Persist context as `app/Models/*.php` plus `database/migrations/` — agents must edit these together or the schema drifts.

### Recommended subagents
- `faion-backend-agent` (referenced in README frontmatter) — primary implementer for model, scope, and repository code.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts each schema change or refactor into an SDD task with a quality gate (tests + `php artisan migrate:fresh --seed`).
- A purpose-built **eloquent-perf-agent** (worth creating): wraps `php artisan tinker` + Telescope query log to count queries per route and gate PRs on N+1 regressions.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub seed/test fixtures before sharing; factories often hard-code emails and tokens.

### Prompt pattern
Schema change pass:
```
You are a Laravel 11 backend engineer. Given <models/User.php> and
<migrations/>, add a `last_seen_at` timestamp to users. Update: model
$casts, migration up/down, factory, UserResource, and add a scope
`scopeRecentlySeen(int $minutes = 5)`. Output as a single diff. Do
not break existing tests; run `php artisan test --filter=User`.
```

N+1 review pass:
```
Run `php artisan test` with QUERY_LOG=true. For any test where the
SAME parameterized SQL fires more than 2 times, report the test, the
query, and propose an `->with()` fix on the relevant Eloquent call.
Do not fix tests; only fix the model/repository.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan make:model -mfs` | Scaffold model + migration + factory + seeder atomically | bundled with Laravel |
| `php artisan tinker` | Headless REPL for relation/scope smoke tests | bundled |
| `php artisan db:seed` / `migrate:fresh --seed` | Reset DB for agent test runs | bundled |
| `laravel/telescope` | Query log, N+1 detection, dispatched events | `composer require laravel/telescope --dev` |
| `barryvdh/laravel-debugbar` | Per-request query count in dev | `composer require barryvdh/laravel-debugbar --dev` |
| `nunomaduro/larastan` (PHPStan) | Static analysis for Eloquent magic methods | `composer require nunomaduro/larastan --dev` |
| `beyondcode/laravel-query-detector` | Auto-fail on N+1 in tests | `composer require beyondcode/laravel-query-detector --dev` |
| `laravel/pint` | Style fixer (PSR-12), runs in pre-commit | `composer require laravel/pint --dev` |
| `pestphp/pest` | Higher-signal test runner over PHPUnit | `composer require pestphp/pest --dev` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Laravel Forge | SaaS deploy | API yes | Spin up DB-backed apps; agents can drive deploys via `forge` CLI. |
| Laravel Vapor | SaaS serverless | API yes | RDS-backed Eloquent on Lambda; cold-start hits N+1 hard. |
| PlanetScale / Neon | Managed MySQL/Postgres | API yes | Branching DBs play well with Laravel migrations per branch. |
| Sentry / Bugsnag | SaaS errors | API yes | Catches `QueryException`; tag releases by migration version. |
| Honeybadger Insights | SaaS APM | API yes | Per-query timing surfaces Eloquent regressions agents missed. |
| Doctrine ORM | OSS alternative | n/a | Use when DDD-heavy or DataMapper preferred over ActiveRecord. |
| Eloquent (standalone via `illuminate/database`) | OSS | yes | Use Eloquent outside Laravel (workers, CLI tools) — same patterns apply. |

## Templates & scripts
See `templates.md` for model, scope, and repository skeletons. Add to CI a query-budget check (≤50 lines):

```bash
#!/usr/bin/env bash
# query-budget.sh — fail CI if any feature test exceeds N queries.
# Usage: query-budget.sh BUDGET (default 15)
set -euo pipefail
BUDGET="${1:-15}"
LOG=$(mktemp)
DB_LOG_QUERIES=true php artisan test --log-junit "$LOG" \
  --testdox 2>&1 | tee /tmp/test.out
python3 - "$BUDGET" <<'PY'
import re, sys
budget = int(sys.argv[1])
text = open("/tmp/test.out").read()
fails = []
for m in re.finditer(r"^\s*✓?\s*([\w\\:]+).*?queries:\s*(\d+)", text, re.M):
    name, n = m.group(1), int(m.group(2))
    if n > budget:
        fails.append((name, n))
if fails:
    print(f"\nQuery budget {budget} exceeded:")
    for n,q in fails: print(f"  {n}: {q} queries")
    sys.exit(1)
print(f"OK: all tests within {budget} queries")
PY
```

Pair with `beyondcode/laravel-query-detector` in `tests/TestCase.php` to fail hard on N+1.

## Best practices
- **Eager-load by default in repositories.** Keep raw lazy access only inside the model layer; controllers/resources should never trigger fresh queries.
- **Use `Attribute::make()` only.** Do not mix legacy `getFooAttribute` with the new API in the same model — agents copy whichever pattern they saw last.
- **Whitelist `$fillable`, never use `$guarded = []`.** Guarded-empty is a recurring CVE source in agent-generated code.
- **Always pair model change with migration + factory + resource.** Agents that touch only the model produce drift that surfaces in CI an hour later.
- **Wrap multi-write paths in `DB::transaction(fn () => ...)`.** Eloquent does not autorun transactions for `create + relation->attach`.
- **Prefer `firstOrCreate` / `updateOrCreate` over manual `where → save`.** Avoids race conditions in concurrent writers.
- **Disable lazy loading in non-prod.** `Model::preventLazyLoading(! $this->app->isProduction())` makes agent N+1 mistakes throw, not silently slow.
- **Resource classes are the API contract.** Never return raw models from controllers — agents leak `password_hash`, `remember_token`, soft-delete columns otherwise.
- **Index every `where`/`orderBy` column in migrations.** Eloquent makes it cheap to query unindexed columns; the bill arrives in prod.

## AI-agent gotchas
- **Magic relation typos pass static analysis.** `$user->postss` returns `null` (or a `BelongsTo` for a non-existent table) without raising — Larastan needs `_ide_helper_models.php` generated to catch it. Run `php artisan ide-helper:models -W` after every model change.
- **Agent assumes column exists.** LLMs invent columns from variable names (`$user->avatar_url`) when the migration only has `avatar`. Force the agent to `Read` the latest migration before referencing a field.
- **`with` chains hide cost.** Agents add `->with(['posts.comments.author', 'roles.permissions'])` to "be safe" — this loads the entire object graph. Cap nesting depth at 2 in code review.
- **Mass assignment regressions during refactor.** Adding a column without updating `$fillable` makes `User::create($validated)` silently drop the field. Add a Larastan rule.
- **Soft delete + unique index conflict.** Agents add `unique('email')` migrations on soft-deleted models — re-creating a deleted user fails. Use `unique('email')->whereNull('deleted_at')` (Postgres) or restore-on-conflict logic.
- **Polymorphic morph map drift.** Agents rename a model and forget the `Relation::enforceMorphMap` registry; existing rows now point at a missing class. Always update morph map in `AppServiceProvider` alongside class renames.
- **Test DB ≠ prod DB.** Agents run tests on sqlite, ship to mysql/postgres; `JSON_EXTRACT`, full-text, and case-sensitivity differ. Force the test suite onto the prod DB engine in CI.
- **Factory state explosion.** Agents create per-test factories instead of factory states; the next agent can't find them. Standardize `UserFactory::admin()`, `UserFactory::withPosts(int $n)` and document.
- **Repository over-abstraction.** Agents wrap Eloquent in a repo, then bypass it 50% of the time. Either commit fully (no `Model::query()` outside repo) or skip the pattern.
- **Policy bypass via `find`.** Agents forget `$this->authorize` in show/update endpoints; multi-tenant data leaks. Default to `findOrFail` in the policy itself, not the controller.

## References
- Laravel docs — Eloquent ORM. https://laravel.com/docs/eloquent
- Laravel docs — Eloquent Relationships. https://laravel.com/docs/eloquent-relationships
- Laravel docs — Mass Assignment. https://laravel.com/docs/eloquent#mass-assignment
- Mohamed Said — "Lazy Loading in Eloquent." https://themsaid.com/eloquent-lazy-loading
- Spatie blog — Repository pattern critique. https://spatie.be/docs/laravel-medialibrary
- Beyond Code — `laravel-query-detector`. https://github.com/beyondcode/laravel-query-detector
- Larastan docs (Eloquent magic). https://github.com/larastan/larastan
- Sibling methodologies in this repo: `pro/dev/backend-enterprise/php-laravel/`, `pro/dev/backend-enterprise/php-laravel-patterns/`, `pro/dev/backend-enterprise/decomposition-laravel/`.
