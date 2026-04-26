# Agent Integration — PHP Eloquent Patterns

## When to use
- Laravel 10/11 apps where models are gaining methods, scopes, accessors/mutators, and need either a Repository wrapper or a Query Object split.
- Migrating raw query builder code to Eloquent for readability and relationship eager-loading.
- Standardizing model conventions: `$fillable` discipline, `$casts`, soft deletes, observers vs events.
- API resources backed by eager-loaded Eloquent collections, paginated with `LengthAwarePaginator`.

## When NOT to use
- High-throughput hot paths where Eloquent's hydration cost matters — drop to `DB::table(...)` query builder.
- Reporting / OLAP — Eloquent over-fetches; use raw SQL or a dedicated read model.
- Bulk inserts/updates >10k rows — use `upsert`, `LazyCollection`, or chunked raw SQL; `Model::create` in a loop is the #1 perf trap.
- Domains with strict invariants (DDD aggregates) — Eloquent's Active Record style fights immutability and value objects.

## Where it fails / limitations
- The "Repository pattern over Eloquent" debate: a thin repo around `$model->find/create/update` adds indirection without domain benefit. Use only when you'll have multiple data sources or need to mock at boundaries.
- N+1 queries are silent — they show up as latency in prod, not as errors. Without `Model::preventLazyLoading()` (Laravel 9+), agents will ship N+1 by default.
- Soft deletes hide rows in default scopes; reports that bypass scopes (`withTrashed()`) silently include deleted data.
- `$casts` to `array` / `json` causes mass-assignment bypass if not also in `$fillable`.
- Accessors using new `Attribute::make(...)` syntax behave differently from old `getXAttribute` mutators when both exist — agents mix the two.

## Agentic workflow
A subagent should generate model + migration + factory + seeder + Pest/PHPUnit feature test in one diff. For repository pattern, add a `Contracts/<Name>Repository` interface, the `Eloquent<Name>Repository` impl, and bind in `AppServiceProvider`. Force `Model::preventLazyLoading()` in `AppServiceProvider::boot()` for non-prod, so N+1 explodes loudly during dev. Run `php artisan test` after every diff before committing.

### Recommended subagents
- `faion-sdd-executor-agent` — Pest test → model → controller cycle.
- A `laravel-resource` subagent (project-local) — generates the full HTTP resource (FormRequest, controller, model w/ relationships, factory, test).

### Prompt pattern
```
Generate the Order resource:
- migration create_orders_table with user_id FK, status enum, total_cents, soft deletes
- App\Models\Order with $fillable, $casts (status => OrderStatus enum), HasMany items
- OrderFactory + OrderItemFactory
- App\Http\Resources\OrderResource (eager-loads items)
- OrderController index/show/store with FormRequest + policy stub
- tests/Feature/OrderTest.php (Pest) covering 200/422/403
Bind no repository — go through model. Use ULIDs not auto-inc.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan make:model -mfsc` | Generates model+migration+factory+seeder+controller | https://laravel.com/docs/artisan |
| `php artisan db:seed`, `migrate:fresh --seed` | Reset dev DB | core |
| `php artisan tinker` | REPL — agents can verify queries before adding to code | core |
| Larastan / phpstan | Static analysis with Eloquent rules | https://github.com/larastan/larastan |
| Laravel Pint | Code style (PSR-12 + Laravel preset) | `composer require laravel/pint --dev` |
| Laravel Telescope / Debugbar | See N+1 queries in dev | https://laravel.com/docs/telescope |
| Pest | Test runner; `pest --parallel` | https://pestphp.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Laravel Forge / Vapor | SaaS | Yes | Deploy targets; `forge` CLI works for agents |
| Laravel Nova / Filament | SaaS / OSS | Yes (Filament more so) | Admin panels backed by Eloquent — agents can scaffold resources |
| Sentry / Bugsnag | SaaS | Yes | Capture model events / failed jobs |
| Horizon (Redis queues) | OSS | Yes | Pair with Eloquent for async writes |
| Scout + Meilisearch / Algolia | OSS / SaaS | Yes | Search index tied to Eloquent observers |

## Templates & scripts
See `templates.md` for full model+repository pair. Snippet — query object pattern (better default than thin repos):

```php
<?php
// app/Queries/UsersQuery.php
namespace App\Queries;

use App\Models\User;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Builder;

class UsersQuery
{
    public function __construct(private Builder $query) {}

    public static function make(): self { return new self(User::query()); }
    public function active(): self { $this->query->where('is_active', true); return $this; }
    public function withRole(string $r): self { $this->query->whereHas('roles', fn($q) => $q->where('name', $r)); return $this; }
    public function search(?string $term): self {
        if (filled($term)) $this->query->whereAny(['name','email'], 'LIKE', "%$term%");
        return $this;
    }
    public function paginate(int $per = 20): LengthAwarePaginator {
        return $this->query->with('roles')->latest()->paginate($per);
    }
}
```

## Best practices
- Enable `Model::preventLazyLoading(! app()->isProduction())` in `AppServiceProvider::boot()` to surface N+1.
- Always use `whereBelongsTo`, `whereHas`, `withCount`, `withSum`, `withExists` instead of manual joins for relationship filters.
- Cast everything that's not a string: enums, dates, arrays, decimals (`'price' => 'decimal:2'`).
- Prefer scopes for filters reused across endpoints; prefer query objects for multi-condition reports.
- Use `DB::transaction(fn () => ...)` over manual begin/commit. Eloquent observer callbacks run inside the same transaction by default.
- ULID/UUID PKs (`use HasUlids`) for any model exposed via API; auto-increment leaks counts.
- Pin `$with = []` to avoid hidden global eager loads — eager load explicitly per query instead.

## AI-agent gotchas
- Agents leave `$fillable = []` empty and use `$guarded = []` (mass-assignment foot-gun). Reject diffs with empty `$fillable` unless `$guarded` is set to specific fields.
- They generate `Model::all()` on user-facing endpoints. Always require pagination.
- Accessors generated as old `getXAttribute` style instead of new `Attribute::make(...)`; pick one and enforce.
- Agents add a `Repository` interface for trivial CRUD — challenge them: "is there a second implementation?" If no, drop it.
- They forget to add `WithoutScout` markers when seeding, causing thousands of search-index calls. Pin `Scout::withoutSyncingToSearch(...)`.
- Human-in-loop checkpoint: review eager-load list — wrong eager-load is silently slow, not broken. Use Telescope or Debugbar to verify query count before merging.

## References
- Laravel docs — Eloquent: https://laravel.com/docs/eloquent
- Spatie's "Laravel Beyond CRUD": https://laravel-beyond-crud.com
- Aaron Francis — "Mastering Postgres for Laravel": https://masteringpostgres.com
- Larastan rules: https://github.com/larastan/larastan/blob/master/docs/rules.md
- "Refactoring to Collections" — Adam Wathan
