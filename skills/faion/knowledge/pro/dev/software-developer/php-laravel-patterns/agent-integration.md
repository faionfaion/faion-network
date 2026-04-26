# Agent Integration — Laravel Patterns

## When to use
- Greenfield Laravel 10/11/12 API where the team wants Controller → Service → Repository (or Action) layering instead of fat models or fat controllers.
- Brownfield Laravel monolith refactor: extract business logic from controllers into Service classes / single-action invokables, swap Eloquent leaks for Resources.
- Cross-cutting hardening: Form Requests for validation, Resources for response shaping, dedicated Service classes for transactions and side effects.
- Migrating from `Repository pattern with Eloquent` to leaner Action / Service classes following modern community practice (the Repository pattern over Eloquent is often pure overhead).
- Standardizing API versioning (`Api\V1\`) and authentication boundary (Sanctum / Passport / Laravel Auth) at controller layer.
- Generating CRUD slices (Controller + FormRequest + Resource + Service + tests) for new resources.

## When NOT to use
- Tiny Laravel apps (<10 routes) where Service + Repository is over-engineering — Eloquent inside controllers is fine.
- Laravel projects standardized on `Action`-only architecture (e.g., `lorisleiva/laravel-actions`) or `Spatie\LaravelData` + DDD — the README's Service+Resource pattern is one of several valid styles; check team standard first.
- Inertia / Livewire / Filament-heavy apps where the framework idiom (controller → view component) is the right boundary.
- Console-only artisan apps; the controller / FormRequest / Resource trio doesn't apply.
- Workloads where Laravel itself is the wrong tool (heavy stream processing, ML inference) — pattern adoption won't fix the fit.

## Where it fails / limitations
- **`UserRepository` over Eloquent is anti-pattern.** README's repository wraps `User::query()` and adds nothing. Eloquent is already a repository. Drop the wrapper unless you actually swap implementations (Postgres → ElasticSearch projection).
- **Service classes drift into `God` services.** Without a clear boundary (one action per service or one aggregate per service), `UserService` accumulates 30 methods.
- **Form Request authorization vs. policy duplication.** `authorize()` in Form Request and `Policy::create()` both run; teams forget which is the source of truth, get 403s in test, and disable both.
- **Resource collections forgetting pagination meta.** `UserResource::collection($users)` on a paginator drops `links` / `meta`. Use `(new UserCollection($paginator))` or `UserResource::collection($paginator)->additional([...])`.
- **`Eloquent::firstOrCreate` race conditions.** Concurrent requests both miss, both insert, unique constraint fails. Use `upsert` or wrap in `DB::transaction` + `lockForUpdate`.
- **N+1 in Resources.** Resource accesses `$this->profile->name`; if controller didn't `with('profile')`, every list item triggers a query. Telescope flags it; agents miss it.
- **`request()` helper in services.** Services that read `request()->user()` are not testable in isolation and break in queue context. Pass user explicitly.
- **Too many magic facades.** `Cache::`, `Mail::`, `Notification::` in services are hard to mock; favor injected contracts (`CacheRepository`, `Mailer`).
- **Transactions wrapping HTTP calls.** Services wrap `DB::transaction` around Stripe/SendGrid calls; locks held across network = deadlocks. External calls go BEFORE or AFTER the transaction, with idempotency keys.

## Agentic workflow
Drive Laravel pattern adoption as a four-stage pipeline: (1) a discovery agent inventories controllers/models/services and rates each against the README's controller/service/resource pattern; (2) a slice-gen agent emits Controller + FormRequest + Resource + Service for one resource per task; (3) a refactor agent moves business logic out of controllers, replaces array responses with Resources, replaces inline `validator()` with FormRequest, replaces `find()` with policy-aware service methods; (4) a test agent generates feature tests (`Pest` / PHPUnit) against routes and unit tests for services. Use `faion-sdd-executor-agent` to drive each resource per SDD task.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — opus model fits because Laravel boundary decisions (Service vs. Action, Resource vs. raw array, Policy vs. Gate) are decision-heavy.
- `faion-feature-executor` skill — sequential mode: FormRequest → Service → Controller → Resource → tests, gating on green.
- A purpose-built **laravel-anti-pattern-lint agent** (worth adding under `agents/`): linter for the README's banned patterns (Eloquent in controller actions, validation in controller, raw array responses, magic facades in services, `request()` calls in services, repositories that wrap Eloquent without value).
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before committing seeders, fixtures, and `.env.example`; agents constantly leak real-looking secrets and emails.
- For queue-heavy patterns, escalate to sibling `pro/dev/software-developer/php-laravel-queues/`.

### Prompt pattern
Resource slice generation:
```
You are scaffolding a CRUD slice for resource <Resource> on Laravel 11.
Output exactly:
1. app/Http/Controllers/Api/V1/<Resource>Controller.php — typed,
   constructor-injected <Resource>Service. NO Eloquent calls. Methods:
   index, store(StoreXRequest), show($id), update(UpdateXRequest, $id),
   destroy($id). Returns Resource / Collection / JsonResponse only.
2. app/Http/Requests/Store<Resource>Request.php — authorize() returns
   $this->user()->can('create', <Resource>::class); rules() typed.
3. app/Http/Requests/Update<Resource>Request.php similar.
4. app/Http/Resources/<Resource>Resource.php — explicit field list, no
   $this->resource->getAttributes() return-all.
5. app/Http/Resources/<Resource>Collection.php — extends ResourceCollection
   to preserve pagination meta.
6. app/Services/<Resource>Service.php — methods paginate(perPage),
   create(array $data), findOrFail($id), update($id, array $data),
   delete($id). NO request() helper. NO facades for Cache/Mail —
   inject contracts.
7. app/Policies/<Resource>Policy.php with viewAny, view, create,
   update, delete.
8. routes/api.php — Route::apiResource('v1/<resource>s', controller)
   ->middleware('auth:sanctum').
9. tests/Feature/<Resource>Test.php (Pest) covering all five
   endpoints.
NEVER add a <Resource>Repository unless asked — Eloquent is the
repository.
```

Anti-pattern review:
```
You are reviewing a PR with Laravel changes. Flag:
(1) Eloquent calls inside Controller methods (must be in Service),
(2) validator() / Validator::make in controller (use FormRequest),
(3) controller returning raw array / Eloquent model directly
   (must use Resource),
(4) UserRepository wrapping User::query without a second backing impl,
(5) request() helper inside Service classes,
(6) Cache:: / Mail:: / Notification:: facade inside Service (inject
   contract),
(7) DB::transaction wrapping external HTTP / queue dispatch,
(8) firstOrCreate / updateOrCreate without explicit lockForUpdate,
(9) Resource accessing relations not eager-loaded in controller (N+1),
(10) Policy missing for any model used in a controller.
Cite file:line. Do not propose fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan` | Laravel CLI (make:*, route:list, telescope, queue:work) | https://laravel.com/docs/artisan |
| `composer` | PHP dep mgmt | https://getcomposer.org |
| `laravel new` | Project scaffolding | https://laravel.com/docs/installation |
| `laravel pint` | Opinionated PHP-CS-Fixer for Laravel style | `composer require laravel/pint --dev` ; https://laravel.com/docs/pint |
| `phpstan` / `larastan` | Static analysis with Laravel rules | https://github.com/larastan/larastan |
| `psalm` | Alternative static analyzer with stricter inference | https://psalm.dev |
| `rector` + `RectorLaravel` | Automated upgrade / refactor | https://github.com/driftingly/rector-laravel |
| `pest` | Modern test runner; collapses PHPUnit ceremony | https://pestphp.com |
| `infection` | Mutation testing | https://infection.github.io |
| `php artisan ide-helper:*` (barryvdh) | IDE helpers + model docs for static analysis | https://github.com/barryvdh/laravel-ide-helper |
| `laravel telescope` / `pulse` / `horizon` | Local introspection: queries, jobs, queues | https://laravel.com/docs/telescope |
| `clockwork` | Request profiling, lightweight Telescope | https://underground.works/clockwork |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Laravel Forge | SaaS | yes | Provision + deploy; Forge API for agents; standard ops. |
| Laravel Vapor | SaaS (AWS) | yes | Serverless Laravel; agents can drive `vapor` CLI. |
| Laravel Cloud | SaaS | yes | New-2024 managed Laravel hosting; CLI / API. |
| GitHub Actions / GitLab CI | SaaS | yes | Native Pest + Pint + Larastan workflows. |
| Sentry / Bugsnag / Rollbar | SaaS | yes | Error tracking; Laravel package + breadcrumbs. |
| New Relic / Datadog / Honeycomb | SaaS | yes | APM; OTel-PHP path is the future. |
| Postmark / Mailgun / SES | SaaS | yes | Service classes call Mailer contract → driver swap. |
| Stripe / Cashier | SaaS / OSS | yes | Cashier handles billing service patterns. |
| Spatie Laravel packages (permission, query-builder, data, fractal) | OSS | yes | Common Laravel pattern accelerators. |
| Pulse / Telescope (self-hosted) | OSS | yes | Observability locally + staging. |
| Filament / Nova | OSS / commercial | yes | Admin panels; pattern: Resources mirror Eloquent. |
| Reverb / Pusher | OSS / SaaS | yes | Broadcasting; service classes dispatch events. |

## Templates & scripts

The methodology already ships Controller / FormRequest / Resource / Service / Policy templates in `README.md` and `templates.md`. Gap: a script that audits Laravel source for the README's banned patterns. Inline drop-in (≤50 lines) — `scripts/laravel-anti-pattern-lint.sh`:

```bash
#!/usr/bin/env bash
# laravel-anti-pattern-lint.sh — flag README banned patterns.
# Usage: laravel-anti-pattern-lint.sh <project-root>
set -euo pipefail
root="${1:?usage: laravel-anti-pattern-lint.sh PROJECT_ROOT}"
fail=0
echo "# Laravel pattern audit ($root)"

echo "## Eloquent calls inside Controllers"
grep -rEn '\b(User|Order|Post|Product)::(where|find|all|create|update|delete)\(' \
  "$root/app/Http/Controllers" --include='*.php' \
  | tee /tmp/lp.eloq-ctrl || true
[[ -s /tmp/lp.eloq-ctrl ]] && fail=1

echo "## validator() inside Controllers (must use FormRequest)"
grep -rEn 'Validator::make\(|\$request->validate\(' "$root/app/Http/Controllers" --include='*.php' \
  | tee /tmp/lp.val-ctrl || true
[[ -s /tmp/lp.val-ctrl ]] && fail=1

echo "## request() helper inside Services"
grep -rEn '\brequest\(\)' "$root/app/Services" --include='*.php' 2>/dev/null \
  | tee /tmp/lp.req-svc || true
[[ -s /tmp/lp.req-svc ]] && fail=1

echo "## Magic facades inside Services (Cache::, Mail::, Notification::)"
grep -rEn '\b(Cache|Mail|Notification|Bus|Event)::' "$root/app/Services" --include='*.php' 2>/dev/null \
  | tee /tmp/lp.facade-svc || true
[[ -s /tmp/lp.facade-svc ]] && fail=1

echo "## DB::transaction wrapping HTTP / queue dispatch"
grep -rEn -A 10 'DB::transaction' "$root/app" --include='*.php' \
  | grep -E 'Http::|dispatch\(|Stripe::|->charge\(' \
  | tee /tmp/lp.tx-http || true
[[ -s /tmp/lp.tx-http ]] && fail=1

echo "## Repository wrapping Eloquent without alternate impl"
for f in $(find "$root/app" -name '*Repository.php' 2>/dev/null); do
  grep -lE '::query\(\)|::where\(' "$f" >/dev/null && \
    grep -L 'interface\|implements\b' "$f" && \
    echo "  └ $f wraps Eloquent without abstraction"
done | tee /tmp/lp.repo || true

exit "$fail"
```

Pair with `pint --test`, `phpstan analyse`, `pest --parallel`. Wire into Husky / lefthook pre-commit.

## Best practices
- **Controllers thin and HTTP-only.** Receive Request, call Service, return Resource. No Eloquent, no business rules, no validation logic.
- **FormRequest = single source of validation.** Authorization in `authorize()`; rules in `rules()`. Policy methods called from FormRequest where possible.
- **Resources for every API response.** Even single-field responses. Explicit field list (`'id' => $this->id`), never spread `$this->resource->getAttributes()`.
- **Service per use-case or single-action invokable.** "ProcessOrderPayment" as `__invoke()`; resists the God-service drift better than "OrderService".
- **Inject contracts, not facades, in services.** `Mailer`, `CacheRepository`, `Dispatcher` — testable, swappable.
- **No `request()` in services.** Pass `auth()->user()` and explicit args.
- **`Eloquent::with(...)` based on Resource needs.** Eager-load in Service / Controller, never lazy-load in Resource.
- **`DB::transaction` only around DB writes.** External calls (Stripe, SES) go before/after with idempotency.
- **`firstOrCreate` / `updateOrCreate` need locking.** Wrap in transaction + `lockForUpdate` or use `upsert` with unique constraints.
- **Policies for every model.** `php artisan make:policy` per resource; FormRequest's authorize() delegates.
- **API versioning by namespace.** `Api\V1\` not query-string version.
- **Queue heavy work.** Email sends, third-party syncs, image processing — `dispatch(new SyncToCrm($user))`. Service stays sync-fast.
- **Pint + Larastan + Pest in CI.** Style + types + tests.
- **Telescope in local + staging only.** Disable in prod (`TELESCOPE_ENABLED=false`); it persists every request.

## AI-agent gotchas
- **Repository over Eloquent reflex.** Older Laravel tutorials lean on Repository pattern; agents emit it by default. Block in review unless there's a real second backing store.
- **Mass assignment in service.** Agents `User::create($request->all())` straight through the service, ignoring `$fillable`. Force `validated()` from FormRequest.
- **Eloquent::find returning null without `findOrFail`.** Agents return null → controller returns 200 with null body. Use `findOrFail` + handler that maps `ModelNotFoundException` to 404.
- **N+1 hidden in Resources.** Agents add a relation to `toArray()` without eager-loading in Service. Telescope catches in dev; CI must run a feature test that asserts query count.
- **Magic facades in services.** `Cache::remember`, `Notification::send` are easy to write, hard to test. Inject contracts.
- **`DB::transaction` swallowing exceptions.** Agents wrap and forget to log/rethrow; failures are silent.
- **`firstOrCreate` race conditions.** Agents accept the convenience; under load, duplicate records or unique-constraint failures appear in prod.
- **`auth()->user()` in service called from queue.** Queue context has no auth user; service crashes. Pass user explicitly.
- **Resources returning Eloquent dates as strings inconsistently.** Some PHP versions / locales differ. Force ISO-8601 via `$this->created_at->toIso8601String()`.
- **Policies forgotten.** Agents implement controller without `authorize()`. Linter must enforce a policy gate per CRUD endpoint.
- **Tests bind to Eloquent fixtures, not behaviors.** Agents factory + assertDatabaseHas. Add HTTP-level Pest tests that hit routes via `actingAs($user)->postJson(...)`.
- **Routes registered without middleware.** Agents add `Route::apiResource(...)` and forget `auth:sanctum` / `throttle`. Force a default middleware stack in `routes/api.php`.
- **CSRF disabled for "convenience".** Agents add routes to `$except` in `VerifyCsrfToken` for everything. Reject unless API token-auth is the only entry.
- **Outdated Lumen / Laravel <9 idioms.** Agents emit `array_get`, `array_first`, `Input::` facade. Pin Laravel version + reject deprecated.
- **Human-in-the-loop on schema migrations.** Migrations alter prod DB; never auto-merge. Require a separate review label / approver.

## References
- Laravel — https://laravel.com/docs (current LTS)
- Spatie — Guidelines for Laravel. https://spatie.be/guidelines/laravel-php
- Stitcher — Domain-Oriented Laravel. https://stitcher.io/blog/laravel-beyond-crud
- Lorisleiva — Actions in Laravel. https://laravelactions.com
- Eric L. Barnes / Freek Van der Herten / Christoph Rumpel — Laravel patterns blogs. https://laravel-news.com/topics/code-style
- Laracasts — "Laravel Anti-Patterns" series. https://laracasts.com
- Larastan — https://github.com/larastan/larastan
- Pest — https://pestphp.com
- Brent Roose — DDD with Laravel. https://stitcher.io/blog/laravel-beyond-crud
- Sibling methodologies in this repo: `pro/dev/software-developer/php-laravel/`, `php-laravel-queues/`, `php-eloquent/`, `php-phpunit-testing/`, `laravel-patterns/`.
