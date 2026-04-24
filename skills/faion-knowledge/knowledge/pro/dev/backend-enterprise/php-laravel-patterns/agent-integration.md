# Agent Integration — Laravel Patterns

## When to use
- Greenfield Laravel 10/11/12 service that will scale beyond the "fat controller" stage and needs Controller → FormRequest → Service → Repository → Resource layering.
- Brownfield refactor where business logic is leaking into controllers, models, or Blade — split into a service layer the agent can target safely.
- API-first apps where `JsonResource` + `ResourceCollection` shape the contract and need to stay stable across releases.

## When NOT to use
- One-off scripts, prototypes, or admin tooling — Laravel's defaults (Eloquent in controller, Artisan command, Livewire) are faster and the abstraction tax is wasted.
- Domains that demand DDD aggregates and explicit domain events at scale — Laravel patterns get in the way; consider Symfony + a hexagonal layout or extract the bounded context.
- Code that is essentially CRUD and already uses Filament/Nova — extra service layer is dead weight.

## Where it fails / limitations
- Repository-over-Eloquent is controversial: Eloquent is already an Active Record. Repositories add value only when you genuinely have multiple data sources, want to mock without a DB, or enforce query encapsulation.
- Agents often duplicate validation between FormRequest and Service — pick one source of truth (FormRequest) and have the service trust validated data.
- `DB::transaction` closures swallow type info: agent-generated code may miss return-type hints, breaking static analysis.
- `readonly` constructor promotion requires PHP 8.1+; check `composer.json` `"php"` constraint before generating.

## Agentic workflow
A coding subagent should scaffold one resource at a time: migration → model → factory → FormRequest(s) → Resource → Service → Repository (optional) → Controller → Feature test. Drive with `php artisan make:*` to keep stub conventions, then have the agent fill in business logic. Run `vendor/bin/pint`, `vendor/bin/phpstan analyse`, and `php artisan test --filter=<Resource>` after each step. Insert a human checkpoint before generating Repository — confirm it is actually needed.

### Recommended subagents
- `general-purpose` Claude subagent — scaffolding via Artisan + filling controller/service/test bodies.
- Code-review subagent (Sonnet) — verifies layer boundaries (no Eloquent in controller, no HTTP concerns in service).

### Prompt pattern
```
Generate REST resource <Name>: migration, model with $fillable/$casts/relationships, factory, StoreXRequest + UpdateXRequest with rules, XResource, XService with paginate/find/create/update/delete using DB::transaction, Api/V1/XController returning Resources. Add Feature test covering all 5 endpoints + validation failure. Run: composer test, ./vendor/bin/pint, ./vendor/bin/phpstan analyse.
```
```
Refactor <Controller>::<method> by extracting business logic into <Service>::<method>. Keep validation in FormRequest. Controller must only: call service, wrap in Resource, return JsonResponse. Add unit test for the service.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan make:{model,controller,request,resource,service,repository}` | Scaffold layer files | bundled |
| `vendor/bin/pint` | Opinionated code style (Laravel preset) | `composer require laravel/pint --dev` |
| `vendor/bin/phpstan` (Larastan) | Static analysis with Laravel awareness | https://github.com/larastan/larastan |
| `vendor/bin/rector` | Automated refactors (PHP version upgrades, dead code) | https://getrector.com |
| `php artisan test --parallel` | Parallel feature tests | bundled (PHPUnit/Pest) |
| `php artisan ide-helper:generate` | Eloquent magic-method type stubs for the agent | https://github.com/barryvdh/laravel-ide-helper |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Laravel Forge | SaaS | Limited | Server provisioning; agents drive via Forge API |
| Laravel Pulse | OSS | Yes | Live ops dashboard, exposes `/pulse` JSON |
| Laravel Telescope | OSS | Yes (dev) | Inspect requests/queries; agents can scrape entries |
| Sentry | SaaS | Yes | Error tracking; SDK auto-installs middleware |
| Bagisto / Filament | OSS | Yes | Skip the service layer pattern, use admin generators |

## Templates & scripts
See `templates.md` and `examples.md` for Controller/Service skeletons. Inline base service the agent can extend per resource:

```php
abstract class BaseService
{
    public function __construct(protected readonly BaseRepository $repository) {}

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->repository->paginate($perPage);
    }

    public function findOrFail(int $id): Model
    {
        return $this->repository->findOrFail($id);
    }

    public function delete(int $id): bool
    {
        return DB::transaction(fn () => $this->repository->delete($id));
    }
}
```

## Best practices
- Bind `RepositoryInterface → RepositoryImpl` only if you actually have an alternative implementation; otherwise inject the concrete class and skip the interface ceremony.
- Use `FormRequest::validated()` (not `all()`) when passing to service — eliminates mass-assignment risk.
- Never call `request()` from a service. Pass primitives or DTOs; keep services framework-light enough to test without booting Laravel.
- Return Resources from controllers, models from services. Never leak `JsonResponse` into the service layer.
- Use `DB::transaction(fn () => …)` not the manual begin/commit/rollback — exception handling is automatic.
- Cache invalidation: tag caches per resource (`Cache::tags(['users'])`) so the agent has a clear hook to flush after writes.

## AI-agent gotchas
- LLM frequently emits `Eloquent::find()` in controllers despite the service-layer prompt — review must catch this.
- Generated FormRequest rules drift from migration constraints. Have the agent diff `Schema::table` against `rules()` after editing either.
- `private readonly` syntax breaks on PHP < 8.1; agent must read `composer.json` constraint first.
- LLM tends to write `try/catch` blocks that hide errors — for transactions, let exceptions propagate; the framework rolls back.
- Repository pattern is overprescribed by LLMs. Add a checkpoint prompt: "Is a repository justified for this resource? If not, inject the model directly." 
- For multi-tenant apps, agents forget `tenant_id` scopes in repository queries — explicit prompt + global scope required.

## References
- https://laravel.com/docs/structure
- https://laravel.com/docs/eloquent-resources
- https://laravel.com/docs/validation#form-request-validation
- "Laravel Beyond CRUD" (spatie.be/laravel-beyond-crud) — the de-facto enterprise Laravel pattern guide
- https://github.com/larastan/larastan
