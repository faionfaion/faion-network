# Development Methodologies - Practices

Development practices, coding standards, and project structure patterns.

## Python Ecosystem

### Django Coding Standards

**Problem:** Inconsistent Django code across projects.

**Framework:**

1. **Import Style:**
```python
# Cross-app imports - ALWAYS with alias
from apps.orders import models as order_models
from apps.users import services as user_services

# Own modules (relative)
from .models import User
from . import constants
```

2. **Services = Functions:**
```python
# services/activation.py
def activate_user_item(
    user: User,
    item_code: str,
    *,
    activated_by: Admin,
) -> Item:
    """Activate item for user."""
    item = Item.objects.get(code=item_code)
    item.user = user
    item.is_active = True
    item.save(update_fields=['user', 'is_active', 'updated_at'])
    return item
```

3. **Multi-line Parameters:**
```python
def create_order(
    user: User,
    amount: Decimal,
    order_type: str,
    *,  # Keyword-only after
    item: Item | None = None,
    notify: bool = True,
) -> Order:
    ...
```

4. **Thin Views:**
```python
class ItemActivationView(APIView):
    def post(self, request):
        serializer = ItemActivationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = services.activate_user_item(
            user=request.user,
            item_code=serializer.validated_data['item_code'],
        )
        return Response(ItemResponse(item).data)
```

**Agent:** faion-code-agent

### Django Code Decision Tree

**Problem:** Unclear where to put code.

**Framework:**
```
What does the function do?
│
├─ Changes DB (CREATE/UPDATE/DELETE)?
│  └─ services/
├─ Makes external API calls?
│  └─ services/ or integrations/
├─ Pure function (validation, calculation)?
│  └─ utils/
└─ Data transformation?
   └─ utils/
```

**Agent:** faion-code-agent

### Django Base Model Pattern

**Problem:** Missing standard fields on models.

**Framework:**
```python
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

**Agent:** faion-code-agent

### FastAPI Standards

**Problem:** Inconsistent FastAPI patterns.

**Framework:**
```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.create_item(db, item, current_user)
```

**Agent:** faion-code-agent

### Python Project Structure

**Problem:** No standard project layout.

**Framework:**
```
project/
├── pyproject.toml
├── src/
│   └── package/
│       ├── __init__.py
│       ├── main.py
│       └── models/
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── .env.example
└── README.md
```

**Agent:** faion-code-agent

### Python Type Hints

**Problem:** Unclear function signatures.

**Framework:**
```python
from typing import Optional, List, Dict

def process_users(
    users: List[User],
    options: Optional[Dict[str, str]] = None,
) -> List[ProcessedUser]:
    ...
```

**Agent:** faion-code-agent

### Python Dependency Management

**Problem:** Dependency conflicts, no lockfile.

**Framework:**
- Use `pyproject.toml` for project config
- Use `poetry` or `uv` for dependency management
- Lock dependencies: `poetry.lock` or `uv.lock`
- Separate dev dependencies

**Agent:** faion-code-agent

---

## JavaScript/TypeScript Ecosystem

### React Component Pattern

**Problem:** Inconsistent component structure.

**Framework:**
```typescript
// src/components/Button/Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant,
  children,
  onClick,
}) => {
  return (
    <button className={styles[variant]} onClick={onClick}>
      {children}
    </button>
  );
};
```

**Agent:** faion-code-agent

### React Hooks Pattern

**Problem:** Logic duplicated across components.

**Framework:**
```typescript
// hooks/useUser.ts
export function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}
```

**Agent:** faion-code-agent

### TypeScript Strict Mode

**Problem:** Type errors caught too late.

**Framework:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

**Agent:** faion-code-agent

### Node.js Project Structure

**Problem:** No standard layout for Node.js.

**Framework:**
```
project/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── routes/
│   ├── services/
│   └── models/
├── tests/
│   └── *.test.ts
└── .env.example
```

**Agent:** faion-code-agent

### Next.js App Router Pattern

**Problem:** Unclear Next.js 13+ patterns.

**Framework:**
```
app/
├── layout.tsx       # Root layout
├── page.tsx         # Home page
├── (auth)/
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── dashboard/
│   ├── layout.tsx   # Dashboard layout
│   └── page.tsx
└── api/
    └── users/
        └── route.ts
```

**Agent:** faion-code-agent

### Frontend State Management

**Problem:** State scattered across components.

**Framework:**

| Solution | Use Case |
|----------|----------|
| useState | Local component state |
| useContext | Shared state (theme, auth) |
| Zustand | Medium complexity |
| Redux Toolkit | Large apps, time-travel debugging |
| TanStack Query | Server state caching |

**Agent:** faion-code-agent

### CSS Architecture

**Problem:** Unorganized styles.

**Framework:**

| Approach | Use Case |
|----------|----------|
| CSS Modules | Component isolation |
| Tailwind CSS | Rapid prototyping |
| styled-components | CSS-in-JS, dynamic styles |
| SCSS + BEM | Large traditional projects |

**Agent:** faion-code-agent

---

## Backend Languages

### Go Project Structure

**Problem:** No standard Go layout.

**Framework:**
```
project/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── handlers/
│   ├── services/
│   └── models/
├── pkg/           # Reusable packages
├── go.mod
└── go.sum
```

**Agent:** faion-code-agent

### Go Error Handling

**Problem:** Inconsistent error handling.

**Framework:**
```go
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

**Agent:** faion-code-agent

### Go Interface Pattern

**Problem:** Tight coupling between components.

**Framework:**
```go
// Define interface where it's used
type UserRepository interface {
    Find(id string) (*User, error)
    Save(user *User) error
}

// Implementation
type PostgresUserRepo struct {
    db *sql.DB
}

func (r *PostgresUserRepo) Find(id string) (*User, error) {
    // implementation
}
```

**Agent:** faion-code-agent

### Go Concurrency Patterns

**Problem:** Race conditions, goroutine leaks.

**Framework:**
```go
// Worker pool pattern
func worker(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        results <- process(job)
    }
}

func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)

    for w := 1; w <= 3; w++ {
        go worker(jobs, results)
    }
}
```

**Agent:** faion-code-agent

### Ruby on Rails Patterns

**Problem:** Fat controllers, thin models.

**Framework:**
- **Thin Controllers:** Only HTTP handling
- **Service Objects:** Business logic
- **Form Objects:** Complex validations
- **Query Objects:** Complex queries
- **Presenters:** View logic

**Agent:** faion-code-agent

### PHP Laravel Patterns

**Problem:** Inconsistent Laravel code.

**Framework:**
```php
// Service Pattern
class UserService
{
    public function create(array $data): User
    {
        return User::create($data);
    }
}

// Controller
class UserController extends Controller
{
    public function store(CreateUserRequest $request, UserService $service)
    {
        $user = $service->create($request->validated());
        return new UserResource($user);
    }
}
```

**Agent:** faion-code-agent

### Java Spring Boot Patterns

**Problem:** Inconsistent Spring code.

**Framework:**
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public User createUser(CreateUserDto dto) {
        User user = User.builder()
            .name(dto.getName())
            .email(dto.getEmail())
            .build();
        return userRepository.save(user);
    }
}
```

**Agent:** faion-code-agent

### C# .NET Patterns

**Problem:** Inconsistent .NET code.

**Framework:**
```csharp
public class UserService : IUserService
{
    private readonly IUserRepository _repository;

    public UserService(IUserRepository repository)
    {
        _repository = repository;
    }

    public async Task<User> CreateAsync(CreateUserDto dto)
    {
        var user = new User { Name = dto.Name, Email = dto.Email };
        return await _repository.AddAsync(user);
    }
}
```

**Agent:** faion-code-agent

### Rust Project Structure

**Problem:** No standard Rust layout.

**Framework:**
```
project/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── lib.rs
│   └── modules/
│       ├── mod.rs
│       └── user.rs
├── tests/
│   └── integration_test.rs
└── examples/
```

**Agent:** faion-code-agent

### Rust Error Handling

**Problem:** Panic vs Result confusion.

**Framework:**
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user not found: {0}")]
    NotFound(String),
    #[error("database error")]
    Database(#[from] sqlx::Error),
}

pub fn get_user(id: &str) -> Result<User, UserError> {
    db.find_user(id)
        .map_err(|e| UserError::Database(e))?
        .ok_or(UserError::NotFound(id.to_string()))
}
```

**Agent:** faion-code-agent

### Rust Async Patterns

**Problem:** Async complexity.

**Framework:**
```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("{:?}", result);
}

async fn fetch_data() -> Result<Data, Error> {
    let response = reqwest::get("https://api.example.com/data").await?;
    response.json().await
}
```

**Agent:** faion-code-agent

---

## Frontend Components

### Storybook Setup

**Problem:** No component documentation.

**Framework:**
```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Click me',
  },
};
```

**Agent:** faion-storybook-agent

### Design Tokens

**Problem:** Inconsistent design values.

**Framework:**
```typescript
// tokens/
export const colors = {
  primary: {
    50: '#f0f9ff',
    500: '#3b82f6',
    900: '#1e3a8a',
  },
  semantic: {
    success: '#22c55e',
    error: '#ef4444',
    warning: '#f59e0b',
  },
};

export const spacing = {
  0: '0',
  1: '0.25rem',
  2: '0.5rem',
  4: '1rem',
  8: '2rem',
};
```

**Agent:** faion-frontend-component-agent

### Component File Structure

**Problem:** Scattered component files.

**Framework:**
```
src/components/{Name}/
├── {Name}.tsx           # Component
├── {Name}.stories.tsx   # Storybook
├── {Name}.test.tsx      # Tests
├── {Name}.module.css    # Styles
└── index.ts             # Export
```

**Agent:** faion-frontend-component-agent

### CLAUDE.md Documentation

**Problem:** No AI-readable context.

**Framework:**
```markdown
# {Folder Name}

{One-sentence description}

## Overview
{2-3 sentences explaining what this folder contains}

## Structure
| Path | Purpose |
|------|---------|
| `file.py` | Description |

## Key Concepts
- **Concept1**: Explanation

## Entry Points
- `main_file.py` — Primary entry point

## Common Operations
### Operation 1
```bash
command example
```

## Dependencies
- dep1: purpose
```

**Size Guidelines:**
- Target: 100-150 lines
- Maximum: 200 lines

**Agent:** faion-code-agent

---

*Development Practices - 40 Patterns*
