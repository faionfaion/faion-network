# Agent Integration — PHP Laravel Backend

## When to use
- Greenfield CRUD-heavy backends with a clear request → controller → service → repository → Eloquent flow.
- Multi-tenant SaaS, content sites, e-commerce, internal tools — Laravel's batteries (auth, queues, mail, broadcasting, scheduler) reduce glue code.
- Teams of 1-5 where convention-over-configuration speeds ramp-up.
- API-first products that pair Laravel Sanctum/Passport for auth and Resource classes for serialization.
- Migrating away from raw PHP / WordPress / CodeIgniter when shipping speed matters more than micro-perf.

## When NOT to use
- Sub-millisecond hot paths (HFT, ad serving) — PHP request bootstrap (~30-80ms cold) is a floor.
- Heavy CPU/ML workloads — Python/Go/Rust are better. Use Laravel as the front door, offload via queues.
- WebSocket-first apps with persistent connections — use Laravel Reverb only as a complement, not the core runtime.
- Stateful, long-lived processes (game servers, media transcoders) — wrong runtime model.
- When the team has zero PHP experience and the project has a hard deadline.

## Where it fails / limitations
- Magic everywhere (facades, service container resolution, `Auth::user()`) — IDE navigation, static analysis, and onboarding suffer without Larastan + IDE Helper.
- N+1 queries are easy to write in Blade/JSON resources; ship `\DB::enableQueryLog()` checks or Telescope to catch them.
- Eloquent's "active record + magic relations" makes domain modeling messy at scale → consider DDD + repositories or jump to a dedicated query layer.
- `Request::all()` mass-assignment exposes you to property injection unless `$fillable`/Form Requests are disciplined.
- Default cache + session use the file driver — fine for one host, broken behind a load balancer. Switch to Redis early.

## Agentic workflow
Drive Laravel features with a subagent that owns the full slice: route → controller → form request → service → repository → Eloquent model + migration → API resource → feature test. The agent must run `php artisan migrate:fresh --seed && php artisan test` as a quality gate and `vendor/bin/pint --test` + `vendor/bin/phpstan analyse` to catch style/type drift. For larger features, brainstorm first (`faion-brainstorm`), then execute slice-by-slice.

### Recommended subagents
- `faion-feature-executor` — sequential SDD task execution; fits Laravel slice work cleanly.
- `faion-sdd-executor-agent` — quality gates (tests, lint, type checks).
- A custom `laravel-backend-agent` (not present): would own `make:*` artisan generators, route registration, and Sanctum/Passport setup.

### Prompt pattern
```
Implement <feature> as a Laravel slice: migration + Eloquent model with $fillable/$casts, FormRequest, Resource, Service, Controller, route in routes/api.php (versioned). Test: Tests\Feature with RefreshDatabase covering happy path + 1 validation failure + 1 auth failure. Run pint + phpstan + test before reporting done.
```

```
Audit <Module> for N+1: enable query log in a feature test, assert SELECT count <= N, fix via with()/load(). Output diff only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `composer` | Dep manager | https://getcomposer.org |
| `php artisan` | Generators, migrate, test runner, tinker, route:list | Built-in |
| `vendor/bin/pint` | Code style (Laravel-flavored PHP-CS-Fixer) | `composer require --dev laravel/pint` |
| `vendor/bin/phpstan` | Static analysis | `composer require --dev nunomaduro/larastan` |
| `vendor/bin/phpunit` / `php artisan test` | Test runner | Built-in |
| `php artisan ide-helper:generate` | Facade/Eloquent autocompletion stubs | `barryvdh/laravel-ide-helper` |
| `php artisan route:list` | Inspect registered routes (vital before agent commits) | Built-in |
| `php artisan tinker` | REPL — ideal for agent verification steps | Built-in |
| `php artisan migrate:fresh --seed` | Reset DB to known state | Built-in |
| `php artisan optimize` / `optimize:clear` | Cache config/routes/views for prod | Built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Laravel Forge | SaaS | Yes | Provisions servers, sets up nginx + PHP-FPM + Horizon + queue workers via API. |
| Laravel Vapor | SaaS | Yes | Serverless on AWS Lambda + RDS + SQS. CLI-driven (`vapor deploy`). |
| Laravel Cloud | SaaS (preview) | Yes | First-party hosted runtime. |
| Laravel Pulse | OSS | Yes | Dashboard for queues, slow queries, exceptions; queryable via DB. |
| Laravel Telescope | OSS (dev) | Yes | Inspect requests, jobs, queries, mail. Disable in prod. |
| Sentry, Bugsnag, Flare | SaaS | Yes | Native Laravel SDKs auto-capture exceptions + queue failures. |
| Faion starter-kit | OSS (in monorepo) | Yes | `projects/faion-net/faion-starter-laravel` for new projects. |
| Pusher / Laravel Reverb | SaaS / OSS | Yes | Broadcasting backend. |

## Templates & scripts
See templates.md (controller/service/repo skeletons) and README sections (Controller Structure, Service Layer, Eloquent Patterns, Repository Pattern, PHPUnit). Use the faion starter at `projects/faion-net/faion-starter-laravel/` to bootstrap.

## Best practices
- Treat controllers as thin HTTP adapters (10-30 lines). Push branching/validation into Form Requests, business logic into services.
- Use Form Requests (`StoreXRequest`/`UpdateXRequest`) for all writes — never call `$request->all()` raw.
- Wrap multi-step writes in `DB::transaction(fn () => …)`. Pair with `DB::afterCommit()` for queued jobs to avoid race conditions.
- Use Eloquent API Resources for output — never return models directly (they leak hidden fields, dates in wrong formats).
- Adopt UUIDv7/ULID primary keys early for distributed systems; Eloquent supports them via `HasUlids`/`HasUuids` traits.
- Cache routes + config in production (`php artisan optimize`), invalidate during deploy.
- Pin PHP version via `composer.json` `"php": ">=8.3"` and CI matrix.
- Run Larastan at level 8 and treat new violations as build failures.

## AI-agent gotchas
- Agents pattern-match `Request::all()` from old tutorials. Always require Form Requests; reject PRs that bypass them.
- Mass-assignment: agents add new columns to migrations but forget `$fillable` on the model — silent insert failure or, worse, allow client to set protected columns. Check both files in the same diff.
- Agents tend to instantiate concrete classes via `new` instead of using the container. Force constructor injection (typed) so the test harness can swap mocks.
- `RefreshDatabase` trait recreates schema per test class — agents writing 50+ tests slow CI dramatically. Steer toward `DatabaseTransactions` for read-only suites.
- Eloquent's automatic timestamps and soft-deletes interact poorly with bulk inserts (`insert()` skips events). Agents must use `upsert()` or `Model::create()` if events matter.
- Human checkpoint: review every new policy/gate; agents default to `return true` placeholders. Authorization regressions are silent.
- Default `.env` shipped by agents often has `APP_DEBUG=true`, `APP_KEY=`, `DB_PASSWORD=root` — block via pre-commit if these reach `production` env files.

## References
- https://laravel.com/docs (current major version)
- https://laravel-news.com/category/laravel
- https://github.com/larastan/larastan
- https://laraveldaily.com/best-practices
- https://stitcher.io/blog/laravel-without-facades (architecture critique)
