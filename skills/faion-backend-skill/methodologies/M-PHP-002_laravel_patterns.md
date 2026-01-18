# M-PHP-002: Laravel Patterns and Best Practices

## Metadata
- **Category:** Development/Backend/PHP
- **Difficulty:** Intermediate
- **Tags:** #dev, #php, #laravel, #patterns, #methodology
- **Agent:** faion-code-agent

---

## Problem

Laravel's convenience can lead to fat controllers and models. Business logic scatters across the codebase. Testing becomes difficult. You need patterns that keep Laravel applications clean and maintainable.

## Promise

After this methodology, you will build Laravel applications with clear separation of concerns. Your code will be testable, scalable, and follow Laravel best practices.

## Overview

Modern Laravel uses Actions, DTOs, and Repository patterns alongside Eloquent. This methodology covers patterns for APIs and web applications.

---

## Framework

### Step 1: Application Structure

```
app/
├── Actions/                  # Single-purpose classes
│   └── Users/
│       ├── CreateUserAction.php
│       └── UpdateUserAction.php
├── Data/                     # DTOs
│   └── UserData.php
├── Http/
│   ├── Controllers/
│   │   └── Api/
│   │       └── UserController.php
│   ├── Requests/
│   │   └── CreateUserRequest.php
│   └── Resources/
│       └── UserResource.php
├── Models/
│   └── User.php
├── Repositories/             # Data access
│   ├── Contracts/
│   │   └── UserRepositoryInterface.php
│   └── EloquentUserRepository.php
├── Services/                 # Complex business logic
│   └── PaymentService.php
├── Queries/                  # Query builders
│   └── UserQuery.php
└── Policies/
    └── UserPolicy.php
```

### Step 2: Form Requests

**app/Http/Requests/CreateUserRequest.php:**

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class CreateUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // Or check permissions
    }

    public function rules(): array
    {
        return [
            'email' => ['required', 'email', 'unique:users,email'],
            'name' => ['required', 'string', 'min:2', 'max:255'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ];
    }

    public function messages(): array
    {
        return [
            'email.unique' => 'This email is already registered.',
        ];
    }
}
```

### Step 3: Actions Pattern

**app/Actions/Users/CreateUserAction.php:**

```php
<?php

declare(strict_types=1);

namespace App\Actions\Users;

use App\Data\UserData;
use App\Models\User;
use App\Notifications\WelcomeNotification;
use Illuminate\Support\Facades\Hash;

class CreateUserAction
{
    public function execute(UserData $data): User
    {
        $user = User::create([
            'email' => $data->email,
            'name' => $data->name,
            'password' => Hash::make($data->password),
        ]);

        $user->notify(new WelcomeNotification());

        return $user;
    }
}
```

**app/Data/UserData.php:**

```php
<?php

declare(strict_types=1);

namespace App\Data;

use App\Http\Requests\CreateUserRequest;

readonly class UserData
{
    public function __construct(
        public string $email,
        public string $name,
        public string $password,
    ) {}

    public static function fromRequest(CreateUserRequest $request): self
    {
        return new self(
            email: $request->validated('email'),
            name: $request->validated('name'),
            password: $request->validated('password'),
        );
    }
}
```

### Step 4: Thin Controllers

**app/Http/Controllers/Api/UserController.php:**

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers\Api;

use App\Actions\Users\CreateUserAction;
use App\Actions\Users\UpdateUserAction;
use App\Data\UserData;
use App\Http\Controllers\Controller;
use App\Http\Requests\CreateUserRequest;
use App\Http\Requests\UpdateUserRequest;
use App\Http\Resources\UserResource;
use App\Models\User;
use App\Queries\UserQuery;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class UserController extends Controller
{
    public function index(UserQuery $query): AnonymousResourceCollection
    {
        $users = $query
            ->filter(request()->all())
            ->paginate();

        return UserResource::collection($users);
    }

    public function store(
        CreateUserRequest $request,
        CreateUserAction $action
    ): JsonResponse {
        $user = $action->execute(UserData::fromRequest($request));

        return UserResource::make($user)
            ->response()
            ->setStatusCode(201);
    }

    public function show(User $user): UserResource
    {
        return UserResource::make($user->load('orders'));
    }

    public function update(
        UpdateUserRequest $request,
        User $user,
        UpdateUserAction $action
    ): UserResource {
        $user = $action->execute($user, UserData::fromRequest($request));

        return UserResource::make($user);
    }

    public function destroy(User $user): JsonResponse
    {
        $user->delete();

        return response()->json(null, 204);
    }
}
```

### Step 5: API Resources

**app/Http/Resources/UserResource.php:**

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'email' => $this->email,
            'name' => $this->name,
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),

            // Conditional relationships
            'orders' => OrderResource::collection($this->whenLoaded('orders')),
            'orders_count' => $this->whenCounted('orders'),

            // Conditional attributes
            'admin_notes' => $this->when(
                $request->user()?->isAdmin(),
                $this->admin_notes
            ),
        ];
    }
}
```

### Step 6: Query Objects

**app/Queries/UserQuery.php:**

```php
<?php

declare(strict_types=1);

namespace App\Queries;

use App\Models\User;
use Illuminate\Database\Eloquent\Builder;

class UserQuery
{
    public function __construct(
        private Builder $query = new User()
    ) {
        $this->query = User::query();
    }

    public function filter(array $filters): self
    {
        return $this
            ->filterBySearch($filters['search'] ?? null)
            ->filterByStatus($filters['status'] ?? null)
            ->filterByDateRange($filters['from'] ?? null, $filters['to'] ?? null)
            ->orderBy($filters['sort'] ?? 'created_at', $filters['order'] ?? 'desc');
    }

    public function filterBySearch(?string $search): self
    {
        if ($search) {
            $this->query->where(function ($q) use ($search) {
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('email', 'like', "%{$search}%");
            });
        }

        return $this;
    }

    public function filterByStatus(?string $status): self
    {
        if ($status) {
            $this->query->where('status', $status);
        }

        return $this;
    }

    public function filterByDateRange(?string $from, ?string $to): self
    {
        if ($from) {
            $this->query->where('created_at', '>=', $from);
        }

        if ($to) {
            $this->query->where('created_at', '<=', $to);
        }

        return $this;
    }

    public function orderBy(string $column, string $direction = 'asc'): self
    {
        $allowed = ['created_at', 'name', 'email'];

        if (in_array($column, $allowed, true)) {
            $this->query->orderBy($column, $direction);
        }

        return $this;
    }

    public function paginate(int $perPage = 15)
    {
        return $this->query->paginate($perPage);
    }

    public function get()
    {
        return $this->query->get();
    }
}
```

---

## Templates

### Service Provider for Repositories

```php
<?php
// app/Providers/RepositoryServiceProvider.php

namespace App\Providers;

use App\Repositories\Contracts\UserRepositoryInterface;
use App\Repositories\EloquentUserRepository;
use Illuminate\Support\ServiceProvider;

class RepositoryServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->bind(
            UserRepositoryInterface::class,
            EloquentUserRepository::class
        );
    }
}
```

### Error Handler

```php
<?php
// app/Exceptions/Handler.php

use Illuminate\Http\JsonResponse;
use Symfony\Component\HttpKernel\Exception\HttpException;

public function render($request, Throwable $e): JsonResponse
{
    if ($request->expectsJson()) {
        return $this->handleApiException($request, $e);
    }

    return parent::render($request, $e);
}

private function handleApiException($request, Throwable $e): JsonResponse
{
    $status = $e instanceof HttpException ? $e->getStatusCode() : 500;

    return response()->json([
        'error' => [
            'message' => $e->getMessage(),
            'code' => $status,
        ],
    ], $status);
}
```

---

## Examples

### Repository Pattern

```php
<?php
// app/Repositories/Contracts/UserRepositoryInterface.php

interface UserRepositoryInterface
{
    public function findById(int $id): ?User;
    public function findByEmail(string $email): ?User;
    public function create(array $data): User;
    public function update(User $user, array $data): User;
    public function delete(User $user): bool;
}

// app/Repositories/EloquentUserRepository.php

class EloquentUserRepository implements UserRepositoryInterface
{
    public function findById(int $id): ?User
    {
        return User::find($id);
    }

    public function findByEmail(string $email): ?User
    {
        return User::where('email', $email)->first();
    }

    public function create(array $data): User
    {
        return User::create($data);
    }

    public function update(User $user, array $data): User
    {
        $user->update($data);
        return $user->fresh();
    }

    public function delete(User $user): bool
    {
        return $user->delete();
    }
}
```

---

## Common Mistakes

1. **Fat controllers** - Use Actions and Services
2. **Business logic in models** - Keep models for data
3. **N+1 queries** - Use eager loading
4. **Raw request data** - Always use Form Requests
5. **Direct model output** - Use Resources for APIs

---

## Checklist

- [ ] Controllers are thin
- [ ] Form Requests for validation
- [ ] Actions for single operations
- [ ] Resources for API output
- [ ] Query objects for complex filters
- [ ] Policies for authorization
- [ ] Events for side effects

---

## Next Steps

- M-PHP-003: PHP Testing with PHPUnit
- M-PHP-004: PHP Code Quality
- M-API-001: REST API Design

---

*Methodology M-PHP-002 v1.0*
