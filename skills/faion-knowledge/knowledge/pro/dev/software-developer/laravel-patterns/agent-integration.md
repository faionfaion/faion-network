# Agent Integration — PHP Laravel Patterns

## When to use
- Scaffolding a new Laravel 11.x app or extending an existing one with models, migrations, controllers, FormRequests, Resources.
- Generating service / repository / action / DTO classes around Eloquent models.
- Authoring API resources (`JsonResource`, Resource Collections) with consistent envelopes.
- Reviewing PRs for N+1 issues, missing FormRequests, fat controllers, hidden global state.
- Adding queues + jobs (Horizon, database, Redis, SQS) and event/listener wiring.
- Auth flows: Sanctum (SPA), Passport (OAuth2), policies, gates, RBAC.

## When NOT to use
- Hot paths that need sub-millisecond latency — PHP-FPM round trip dominates.
- Heavy data engineering / streaming workloads — pick a JVM/Go pipeline.
- Real-time bidirectional protocols beyond Echo/Reverb scope.
- Greenfield where the team has no PHP — pick what they ship best.

## Where it fails / limitations
- LLMs mix Laravel 9/10/11 conventions (e.g., Kernel.php removal in 11, `bootstrap/app.php` style); pin the version.
- Agents over-use repositories where Eloquent is already a Repository/Active Record — adds dead abstraction.
- N+1 queries: generated code rarely uses `with()` / `loadMissing()`; Laravel Telescope/Debugbar must verify.
- Mass-assignment: agent forgets `$fillable` / `$guarded`, allowing IDOR via update endpoints.
- Migrations missing FK constraints, indexes, and `down()` reversibility.
- Background jobs: agents miss `ShouldBeUnique`, `WithoutOverlapping`, retry/backoff.

## Agentic workflow
Use a scaffolder to bootstrap models + migrations + factories + seeders + FormRequests + controllers + Resources + tests; a domain-coder to enrich models with scopes/casts/observers; a service-coder for Action / Service classes; a queues-coder for Jobs/Listeners with idempotency. A reviewer checks N+1, mass-assignment, policy coverage, validation rules, and migration reversibility. Sonnet is enough for most tasks; reserve Opus for auth design and complex multi-tenant scoping.

### Recommended subagents
- `laravel-scaffolder` (Haiku/Sonnet) — `php artisan make:*` + project layout.
- `eloquent-coder` (Sonnet) — models, scopes, casts, mutators, observers.
- `request-coder` (Sonnet) — FormRequests with Rule objects + custom messages.
- `action-coder` (Sonnet) — `app/Actions/*` single-purpose classes per Spatie convention.
- `policy-coder` (Sonnet) — Policies + Gates + multi-tenant scoping.
- `queues-coder` (Sonnet) — Jobs/Events/Listeners with backoff, retries, idempotency.
- `pest-or-phpunit-coder` (Sonnet) — Pest/PHPUnit feature/unit tests, RefreshDatabase.

### Prompt pattern
```
You are eloquent-coder. Laravel 11, PHP 8.3, Pest. Domain: <ERD>.
For each model emit: migration with FKs + indexes + down(); factory + seeder;
model with $fillable, $casts (use enum casts where applicable), relationships,
local scopes (active, search), observer if audit needed.
Force lazy relationships; never use get() inside accessors.
```

```
You are policy-coder. App is multi-tenant by organization_id. For every
model with create/update/delete actions: emit Policy methods using
$user->organization_id === $model->organization_id; map abilities in
AuthServiceProvider; cover unauthenticated case; tests in tests/Feature/Policies.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan` | Generators, migrations, queues, schedule | laravel.com/docs/artisan |
| `composer` | Dependencies, autoload | getcomposer.org |
| `php artisan tinker` | REPL for app | laravel.com/docs/artisan#tinker |
| `php artisan test` / `vendor/bin/pest` | Test runner | pestphp.com |
| `php artisan route:list` | Route table audit | laravel.com/docs/routing |
| `php artisan queue:work` / `horizon` | Worker + dashboard | laravel.com/docs/horizon |
| `pint` | Laravel-flavored PHP-CS-Fixer | laravel.com/docs/pint |
| `phpstan` / `larastan` | Static analysis | phpstan.org / github.com/larastan/larastan |
| `rector` | Automated refactors | getrector.com |
| `php artisan telescope` | Local request/query/job introspection | laravel.com/docs/telescope |
| `php artisan migrate:fresh --seed` | Reset DB | laravel.com/docs/migrations |
| `valet` / `herd` / `sail` / `octane` | Local + prod runtimes | laravel.com/docs/valet, herd.laravel.com, laravel.com/docs/sail, laravel.com/docs/octane |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Laravel Forge / Vapor / Cloud | SaaS | Yes | Forge for VPS, Vapor for serverless, Cloud (new) for managed. |
| Laravel Horizon | OSS | Yes | Redis queue dashboard; agent edits config/horizon.php. |
| Laravel Reverb | OSS | Yes | Native WebSockets; agent wires Echo client. |
| Laravel Pulse | OSS | Yes | App perf/observability dashboard. |
| Laravel Nova | SaaS | Partial | Admin panel; agent generates resources, custom fields need human design. |
| Laravel Sanctum / Passport | OSS | Yes | Token + OAuth2 auth. |
| Laravel Cashier | OSS | Yes | Stripe / Paddle billing. |
| Spatie packages (permissions, query-builder, media-library) | OSS | Yes | Industry-standard; agent integrates well. |
| Filament / Backpack | OSS | Yes | Admin panel scaffolds; agent generates Resources. |
| Inertia.js / Livewire | OSS | Yes | Frontend stacks; agent picks based on team skills. |
| Sentry / Bugsnag / Flare | SaaS | Yes | Error tracking; agent wires `app/Exceptions/Handler.php`. |
| Pusher / Ably | SaaS | Yes | Drop-in for Echo broadcasting. |

## Templates & scripts
See `templates.md` for full model/service/job templates. Inline gate that fits in CI:

```bash
#!/usr/bin/env bash
# laravel-pr-gate.sh
set -euo pipefail
composer install --no-progress --prefer-dist
vendor/bin/pint --test
vendor/bin/phpstan analyse --memory-limit=1G --no-progress
php artisan config:clear
php artisan route:list --json > /tmp/routes.json
# enforce FormRequest usage on POST/PUT/PATCH/DELETE
jq -r '.[] | select(.method | test("POST|PUT|PATCH|DELETE")) | .action' /tmp/routes.json |
  grep -v 'FormRequest' | grep -v 'Closure' | grep . && {
    echo "ERROR: route handler without FormRequest"; exit 1; } || true
# eager-loading regression: scan controllers for ::all() and ::get()
grep -RIn --include='*.php' '::all()\|->get()' app/Http/Controllers && {
  echo "WARN: explicit get() / all() — verify eager-load with()"; }
# enforce $fillable
grep -RIn --include='*.php' 'extends Model' app/Models | while read -r line; do
  f=${line%%:*}
  grep -q '\$fillable\|\$guarded' "$f" || {
    echo "ERROR: $f missing fillable/guarded"; exit 1; }
done
# pest
vendor/bin/pest --parallel --coverage --min=70
echo "Laravel gate OK"
```

## Best practices
- Pin Laravel + PHP version in the prompt (Laravel 11 + PHP 8.3 is current target).
- Controllers stay thin: validate via FormRequest, dispatch to Action/Service, return Resource. No business logic inline.
- Always declare `$fillable` (preferred) or `$guarded = []` with explicit access policies; never both blank.
- Use enum casts (`'status' => StatusEnum::class`) instead of string columns + manual checks.
- For migrations: every FK has `cascadeOnDelete()` or `restrictOnDelete()` explicit; every `down()` is reversible.
- Wrap multi-step writes in `DB::transaction(fn () => ...)` — agent often forgets and partial writes persist.
- Use `$model->loadMissing(...)` in services + `with(...)` in controllers; never `$model->relation` in tight loops.
- Queue jobs default to `tries=3`, `backoff=[10,30,60]`, `ShouldBeUnique` if mutating; idempotency keys for external calls.
- Auth: prefer Policies + Gates over inline checks; always cover unauthenticated case in policy tests.

## AI-agent gotchas
- Laravel 11 removed `app/Http/Kernel.php`; agent still emits middleware registrations there.
- Validation rule arrays vs Rule objects: agent mixes them, causing duplicate keys.
- API Resources: agent forgets `JsonResource::withoutWrapping()` and breaks frontend expectations.
- `Cache::remember` keys without tenant scope leak data across orgs in multi-tenant apps.
- Queues without `WithoutOverlapping` retry simultaneously and hammer external APIs.
- Human checkpoint REQUIRED before: running `migrate:fresh` in non-local, rotating `APP_KEY`, changing queue connection in prod, enabling Telescope in prod, modifying `auth.php` providers.
- `Schema::dropIfExists` in `down()` without recreating dependent FKs leaves orphaned constraints.
- Agent uses `Auth::user()` in jobs (no session) — must inject user-id and refetch.
- `Eloquent::whereHas()` generates correlated subqueries; for hot paths use `whereIn` + IDs.
- Storage paths default to `local` disk; agent forgets to switch to `s3` / `gcs` for prod.

## References
- Laravel docs: https://laravel.com/docs/.
- Spatie best practices guide: https://spatie.be/guidelines/laravel.
- Laravel Bootcamp: https://bootcamp.laravel.com/.
- "Laravel: Up & Running", Matt Stauffer (3rd ed.).
- Pest PHP: https://pestphp.com/.
- Larastan: https://github.com/larastan/larastan.
- Adam Wathan, "Refactoring to Collections".
