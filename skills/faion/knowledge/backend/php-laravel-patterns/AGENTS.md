# Laravel Patterns

## Summary

**One-sentence:** Clean-architecture layering for Laravel — thin Controller → FormRequest → Service (DB::transaction) → optional Repository → JsonResource; controllers contain no Eloquent or business logic.

**One-paragraph:** Clean-architecture layering for Laravel 10/11/12 services. Controllers stay thin: validate via FormRequest, call one service method, wrap output in a JsonResource, return `JsonResponse`. Services accept primitives or DTOs (never `request()`), encapsulate business rules, and use `DB::transaction(fn() => ...)` for multi-write paths. Services return Eloquent models or DTOs — never `JsonResponse`. Repositories are introduced ONLY when there is a real abstraction need (multiple data sources, query encapsulation); interfaces are skipped for single-implementation repositories.

**Ефективно для:**

- Greenfield Laravel 10/11/12 service that will grow beyond simple CRUD.
- Brownfield refactor where business logic leaks into controllers or models.
- API-first apps where `JsonResource` + `ResourceCollection` must stay stable across releases.
- LLM-assisted teams that need a contract for what each layer is allowed to do.

## Applies If (ALL must hold)

- Laravel 10/11/12 service that grows beyond simple CRUD.
- HTTP API or full-stack web surface.
- Business logic exists that should be unit-testable without booting HTTP.

## Skip If (ANY kills it)

- Prototypes, admin tooling, or one-off scripts — the abstraction tax is wasted; keep Eloquent in the controller.
- Domains requiring DDD aggregates and explicit bounded contexts — use Symfony + hexagonal layout.
- Essentially-CRUD apps already using Filament / Nova — extra service layer is dead weight.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case catalogue | Markdown verb list | product |
| Eloquent model list | Markdown | data modelling |
| API contract | OpenAPI YAML or Markdown | API design |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Umbrella for queue / scheduler discipline. |
| [[php-eloquent]] | ORM rules that controllers / services rely on. |
| [[decomposition-laravel]] | Action + DTO + FormRequest decomposition. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: thin-controller-no-eloquent, service-no-request-globals, validated-only, jsonresource-from-controller-only, db-transaction-closure, repository-only-when-needed, policy-required | 1300 |
| `content/02-output-contract.xml` | essential | JSON Schema for the layered-Laravel manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: controller-with-eloquent, service-calling-request, transaction-with-swallow-catch, premature-repository, jsonresponse-from-service, inline-authorization, inline-validation-duplication | 1100 |
| `content/04-procedure.xml` | essential | 6-step procedure: FormRequest → Service with DB::transaction → optional Repository → JsonResource → tests → layering audit + documented rules | 950 |
| `content/05-examples.xml` | essential | Worked 612-line fat-controller migration + the audit signals to act on | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-service-from-controller` | sonnet | Reading legacy controller + extracting logic. |
| `decide-repository-need` | opus | Premature-abstraction risk. |
| `enforce-layer-discipline` | haiku | Mechanical scan for Eloquent in controllers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/BaseService.php` | Service base class with `DB::transaction` helper. |
| `templates/UserController.php` | Thin controller skeleton (validate → service → Resource). |
| `templates/UserService.php` | Service skeleton with constructor injection + transactional method. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-laravel-patterns.py` | Validate the layered-Laravel manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |
| `scripts/laravel-anti-pattern-lint.sh` | Count fat controller methods, inline `validate()`, controller-level `DB::transaction`, raw model returns and inline `abort(403)`. | Before and after a layering refactor; CI on Laravel projects. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[php-laravel]]
- [[php-eloquent]]
- [[laravel-patterns]]
- [[decomposition-laravel]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (project shape, abstraction need, layer concern) to a rule from `01-core-rules.xml`. Use it before scaffolding or refactoring a feature.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/BaseService.php`

```php
// Abstract base service — extend per resource to share paginate/find/delete
// Only use when ≥2 resources share the same CRUD shape

namespace App\Services;

use App\Repositories\BaseRepository;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;

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
        return DB::transaction(fn (): bool => $this->repository->delete($id));
    }
}
```

### `templates/UserController.php`

```php
// Thin controller skeleton — Route → FormRequest → Service → Resource
// Replace: User, UserService, StoreUserRequest, UpdateUserRequest, UserResource, UserCollection

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUserRequest;
use App\Http\Requests\UpdateUserRequest;
use App\Http\Resources\UserCollection;
use App\Http\Resources\UserResource;
use App\Services\UserService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Response;

class UserController extends Controller
{
    public function __construct(private readonly UserService $userService) {}

    public function index(): UserCollection
    {
        $users = $this->userService->paginate(
            perPage: request()->integer('per_page', 20)
        );
        return new UserCollection($users);
    }

    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = $this->userService->create($request->validated());
        return (new UserResource($user))->response()->setStatusCode(Response::HTTP_CREATED);
    }

    public function show(int $id): UserResource
    {
        return new UserResource($this->userService->findOrFail($id));
    }

    public function update(UpdateUserRequest $request, int $id): UserResource
    {
        return new UserResource($this->userService->update($id, $request->validated()));
    }

    public function destroy(int $id): JsonResponse
    {
        $this->userService->delete($id);
        return response()->json(null, Response::HTTP_NO_CONTENT);
    }
}
```

### `templates/UserService.php`

```php
// Service layer skeleton — no request(), no JsonResponse, no Eloquent in controller
// Replace: User, UserRepository

namespace App\Services;

use App\Events\UserCreated;
use App\Models\User;
use App\Repositories\UserRepository;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class UserService
{
    public function __construct(private readonly UserRepository $repository) {}

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->repository->paginate($perPage);
    }

    public function findOrFail(int $id): User
    {
        return $this->repository->findOrFail($id);
    }

    public function create(array $data): User
    {
        return DB::transaction(function () use ($data): User {
            $data['password'] = Hash::make($data['password']);
            $user = $this->repository->create($data);
            event(new UserCreated($user));
            return $user;
        });
    }

    public function update(int $id, array $data): User
    {
        return DB::transaction(function () use ($id, $data): User {
            if (isset($data['password'])) {
                $data['password'] = Hash::make($data['password']);
            }
            return $this->repository->update($id, $data);
        });
    }

    public function delete(int $id): bool
    {
        return DB::transaction(fn (): bool => $this->repository->delete($id));
    }
}
```
