# Laravel Decomposition Patterns

LLM-friendly code organization for Laravel projects.

---

## Anti-Pattern: Fat Controllers

```php
// BAD: app/Http/Controllers/UserController.php (500+ lines)
class UserController extends Controller
{
    public function store(Request $request)
    {
        // 100 lines of validation
        // 50 lines of business logic
        // 30 lines of notification
        // 20 lines of response formatting
    }
}
```

---

## LLM-Friendly Structure

```
app/
├── Models/
│   ├── User.php                  # User model (50-80 lines)
│   └── Profile.php               # Profile model (40-60 lines)
├── Services/
│   └── User/
│       ├── UserService.php       # User CRUD (80-100 lines)
│       ├── AuthService.php       # Auth logic (60-80 lines)
│       └── ProfileService.php    # Profile logic (50-70 lines)
├── Repositories/
│   └── User/
│       ├── UserRepository.php        # User queries (60-80 lines)
│       └── UserRepositoryInterface.php  # Interface (20-30 lines)
├── Http/
│   ├── Controllers/
│   │   └── Api/
│   │       ├── UserController.php    # User endpoints (60-80 lines)
│   │       └── AuthController.php    # Auth endpoints (50-70 lines)
│   ├── Requests/
│   │   ├── CreateUserRequest.php     # Create validation (30-40 lines)
│   │   └── UpdateUserRequest.php     # Update validation (30-40 lines)
│   └── Resources/
│       ├── UserResource.php          # User JSON (30-50 lines)
│       └── UserCollection.php        # Users JSON (20-30 lines)
├── Actions/
│   └── User/
│       ├── CreateUserAction.php      # Create action (40-60 lines)
│       ├── UpdateUserAction.php      # Update action (40-60 lines)
│       └── DeleteUserAction.php      # Delete action (30-40 lines)
├── DTOs/
│   └── User/
│       ├── CreateUserDTO.php         # Create data (20-30 lines)
│       └── UpdateUserDTO.php         # Update data (20-30 lines)
└── Policies/
    └── UserPolicy.php                # Permissions (40-60 lines)
```

---

## Action Pattern

```php
// app/Actions/User/CreateUserAction.php (~50 lines)
<?php

namespace App\Actions\User;

use App\DTOs\User\CreateUserDTO;
use App\Models\User;
use App\Notifications\WelcomeNotification;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class CreateUserAction
{
    public function execute(CreateUserDTO $dto): User
    {
        return DB::transaction(function () use ($dto) {
            $user = User::create([
                'name' => $dto->name,
                'email' => $dto->email,
                'password' => Hash::make($dto->password),
            ]);

            $user->notify(new WelcomeNotification());

            return $user;
        });
    }
}
```

---

## DTO Pattern

```php
// app/DTOs/User/CreateUserDTO.php (~25 lines)
<?php

namespace App\DTOs\User;

use App\Http\Requests\CreateUserRequest;

class CreateUserDTO
{
    public function __construct(
        public readonly string $name,
        public readonly string $email,
        public readonly string $password,
    ) {}

    public static function fromRequest(CreateUserRequest $request): self
    {
        return new self(
            name: $request->validated('name'),
            email: $request->validated('email'),
            password: $request->validated('password'),
        );
    }
}
```

---

## Controller Pattern

```php
// app/Http/Controllers/Api/UserController.php (~70 lines)
<?php

namespace App\Http\Controllers\Api;

use App\Actions\User\CreateUserAction;
use App\Actions\User\UpdateUserAction;
use App\DTOs\User\CreateUserDTO;
use App\Http\Controllers\Controller;
use App\Http\Requests\CreateUserRequest;
use App\Http\Resources\UserResource;
use App\Models\User;

class UserController extends Controller
{
    public function index()
    {
        $users = User::query()
            ->when(request('search'), fn($q, $search) =>
                $q->where('name', 'like', "%{$search}%")
            )
            ->paginate();

        return UserResource::collection($users);
    }

    public function store(
        CreateUserRequest $request,
        CreateUserAction $action
    ) {
        $user = $action->execute(
            CreateUserDTO::fromRequest($request)
        );

        return new UserResource($user);
    }

    public function show(User $user)
    {
        $this->authorize('view', $user);
        return new UserResource($user);
    }

    public function update(
        UpdateUserRequest $request,
        User $user,
        UpdateUserAction $action
    ) {
        $this->authorize('update', $user);
        $user = $action->execute($user, UpdateUserDTO::fromRequest($request));
        return new UserResource($user);
    }
}
```

---

## Key Principles

1. **Action Classes** - Single-purpose business logic
2. **DTOs** - Explicit data transfer objects
3. **Form Requests** - Validation extracted
4. **Resources** - Response transformation
5. **Thin Controllers** - Only HTTP handling

---

## File Size Guidelines

| Type | Target | Max |
|------|--------|-----|
| Model | 50-80 | 150 |
| Action | 40-60 | 100 |
| Service | 80-100 | 200 |
| Controller | 60-80 | 150 |
| Request | 30-40 | 80 |
| Resource | 30-50 | 100 |
| Test | 100-150 | 300 |

---

## Related

- [framework-decomposition-patterns.md](framework-decomposition-patterns.md) - All frameworks
- [decomposition-django.md](decomposition-django.md) - Django patterns
- [decomposition-rails.md](decomposition-rails.md) - Rails patterns
- [decomposition-react.md](decomposition-react.md) - React patterns
- [php-laravel.md](php-laravel.md) - Laravel reference
- [php-laravel-patterns.md](php-laravel-patterns.md) - Laravel patterns
- [llm-friendly-architecture.md](llm-friendly-architecture.md) - LLM optimization
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement decomposition-laravel pattern | haiku | Straightforward implementation |
| Review decomposition-laravel implementation | sonnet | Requires code analysis |
| Optimize decomposition-laravel design | opus | Complex trade-offs |

