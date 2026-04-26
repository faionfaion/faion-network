# Agent Integration — PHP Laravel Patterns

## When to use
- New Laravel 10/11 application with full-stack web or JSON API requirements.
- Refactoring fat controllers into Service classes, Action classes (single-purpose `__invoke`), and Form Requests.
- Wiring queue-backed jobs (Horizon + Redis), Eloquent scopes, accessors/mutators (`Attribute` API), and Form Request validation.
- Standing up Pest/PHPUnit feature tests with `RefreshDatabase` and factories.
- Adding API Resources for response shaping and Sanctum/Passport for authentication.

## When NOT to use
- High-throughput async pipelines with strict tail latency — Laravel's per-request bootstrap is heavy; consider Octane only after profiling.
- Lambda-style functions where cold start matters; Laravel Vapor mitigates but isn't free.
- Microservice meshes where you need fine-grained per-service runtime — Symfony or Slim may be a better fit.
- Pure data-pipeline batch jobs — a CLI in Symfony Console or pure PHP without the framework is leaner.

## Where it fails / limitations
- N+1 queries via Eloquent relationships are the most common production issue; agents rarely add `with()` eager loads without prompting.
- Form Requests + DTOs duplicate work; LLMs often skip DTOs and pass `$request->validated()` arrays around, losing type safety.
- Mass assignment via `$model->fill($request->all())` is a security smell; agents reach for it by default.
- Service container auto-wiring works only via constructor type-hints — agents sometimes resolve via `app(Service::class)` and break testability.
- Queue jobs must be idempotent; agents write jobs that double-charge or double-send when a worker retries.
- Eloquent `update()` skips events; agents who refactor from `save()` to `update()` lose model observers and audit trails.

## Agentic workflow
Use a feature-spec → migration → model + factory → action/service → controller + form request → resource + test loop. Each task: run `php artisan migrate:fresh --seed`, `php artisan test`, `vendor/bin/phpstan analyse`. Reviewer agent must check for N+1 (Telescope or `Barryvdh\Debugbar` SQL count assertions), missing `Authorize` policies on routes, and queue-job idempotency. Ban `$request->all()` in service-layer code.

### Recommended subagents
- `faion-sdd-executor-agent` — drive feature tasks; run `artisan test` and PHPStan per task.
- `faion-feature-executor` — feature-level execution with quality gates.
- General reviewer subagent — flag N+1, mass assignment, missing policies, non-idempotent jobs.
- `password-scrubber-agent` — strip secrets from job payloads and exception messages before they hit Horizon.

### Prompt pattern
Plan: "Feature `<name>`: produce migration, Eloquent model with $fillable + relationships + scopes, factory, Form Request with rules and authorize(), Action class with `handle()` returning DTO, Controller using the Action, API Resource, Pest feature test covering happy path + 422 + 403."

Review: "Run `php artisan test` and `vendor/bin/phpstan analyse --level=max`. Inspect query log: any relation accessed inside a `foreach` without prior `with()` is N+1 — list and propose eager loads."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan` | Make/migrate/test/queue commands | shipped with Laravel |
| Laravel Pint | Opinionated PHP CS Fixer wrapper | `composer require laravel/pint --dev` |
| PHPStan + Larastan | Static analysis tuned for Laravel | larastan.dev |
| Rector | Automated upgrade/refactor rules | getrector.com |
| Pest | Expressive testing framework | pestphp.com |
| Laravel Telescope | In-app request/query/job inspector | laravel.com/docs/telescope |
| Laravel Horizon | Redis queue dashboard + config | laravel.com/docs/horizon |
| `php artisan db:show` / `db:table` | Inspect DB schema during agent loops | Laravel 9+ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Forge | SaaS | Partial | Provisioning + deploys; CLI exists but UI is primary |
| Vapor | SaaS | Yes | Serverless deploys; `vapor deploy` is scriptable |
| Envoyer | SaaS | Yes | Zero-downtime deploys; webhook + CLI |
| Sentry | SaaS | Yes | `sentry/sentry-laravel` autodiscovers; one config |
| Bugsnag | SaaS | Yes | Drop-in package |
| Flare (Spatie) | SaaS | Yes | Pairs with Ignition error pages |
| Pusher / Ably | SaaS | Yes | Broadcasting driver, env-var only |

## Templates & scripts
See `templates.md` for Action class, ServiceResult-style DTO, Form Request, and Pest test layout. Agent guard against N+1 in CI:

```php
// tests/TestCase.php — fail tests that produce N+1
use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;

protected function failOnNPlusOne(int $max = 10): void
{
    $count = 0;
    DB::listen(function (QueryExecuted $q) use (&$count, $max) {
        if (++$count > $max) {
            throw new \RuntimeException("Query budget exceeded ({$max})");
        }
    });
}
```

## Best practices
- Keep controllers thin: validate via Form Request, delegate to an Action or Service, return an API Resource.
- Eager-load relationships at the query layer (`User::with(['organization', 'posts'])`), never inside loops.
- Use `Attribute::make(get: ..., set: ...)` (Laravel 9+) instead of legacy `getXxxAttribute` methods.
- Wrap multi-step writes in `DB::transaction(function () { ... })`; do not rely on `save()` ordering.
- Make queue jobs idempotent: derive a unique key, check before performing the side effect, use `ShouldBeUnique` if Laravel 8+.
- Use Policies (`php artisan make:policy`) and `authorize()` in Form Requests; never rely on controller-level checks alone.
- Pin versions of `php`, Laravel, and key packages in `composer.json`; agents sometimes regenerate lock files with major bumps.

## AI-agent gotchas
- Agents reach for `$request->all()` and `$model->fill(...)` — always require a Form Request and `validated()`.
- Eloquent's lazy loading produces invisible N+1; agents writing `foreach ($users as $u) { echo $u->organization->name; }` need `with('organization')` enforced by review.
- LLMs often place HTTP concerns (status codes, response shapes) inside services; keep services HTTP-agnostic and shape responses in API Resources.
- Generated jobs often lack `tries`, `backoff()`, and `failed()`; require these on every job class.
- `Storage::disk('public')` paths agents generate may collide; require UUID-prefixed paths.
- Agents may create routes outside `Route::middleware('auth:sanctum')` groups — confirm middleware coverage on protected routes.
- Mailable classes generated by AI commonly send synchronously inside requests; require `ShouldQueue` for transactional emails.

## References
- Laravel docs — https://laravel.com/docs
- Laravel News (patterns/articles) — https://laravel-news.com/
- Spatie blog (Laravel patterns) — https://spatie.be/blog
- Laracasts — https://laracasts.com
- Larastan — https://github.com/larastan/larastan
- "Laravel Beyond CRUD" — https://laravel-beyond-crud.com/
- Pest docs — https://pestphp.com
