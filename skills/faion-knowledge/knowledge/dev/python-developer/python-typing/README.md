# Python Type Hints and Static Typing

**Type safety, static analysis, better IDE support, bug prevention**

---

## Overview

Python type hints provide static type checking without sacrificing Python's dynamic nature. They enable:

- **IDE Support** - Autocomplete, refactoring, navigation
- **Bug Prevention** - Catch errors before runtime
- **Documentation** - Self-documenting code
- **Team Collaboration** - Clear contracts between components

## Python Version Support

| Feature | Python Version | Import |
|---------|---------------|--------|
| Basic hints (`int`, `str`) | 3.5+ | Built-in |
| `list[T]`, `dict[K,V]` syntax | 3.9+ | Built-in |
| Union syntax `X \| Y` | 3.10+ | Built-in |
| `ParamSpec`, `Concatenate` | 3.10+ | `typing` |
| New generic syntax `class Foo[T]:` | 3.12+ | Built-in |
| TypeVar defaults | 3.13+ | Built-in |
| `ReadOnly` for TypedDict | 3.13+ | `typing` |
| Closed TypedDict (PEP 728) | 3.15+ | `typing_extensions` |

## Type Checkers Comparison

### mypy

**The reference implementation** - most widely adopted (58% in 2025 survey)

Strengths:
- Strict PEP adherence
- Custom plugin system (Django, SQLAlchemy support)
- Mature ecosystem
- Gradual typing support

Weaknesses:
- Slower on large codebases
- Skips unannotated functions by default
- Uses Python's built-in parser (no error recovery)

### Pyright / Pylance

**Microsoft's type checker** - fastest option, excellent IDE integration

Strengths:
- 3-5x faster than mypy
- Checks all code by default (including unannotated)
- Custom parser with error recovery
- Excellent VS Code integration via Pylance
- Often implements new features first

Weaknesses:
- No plugin system
- Sometimes more lenient than mypy

### ty (Emerging - 2025)

**Astral's Rust-based type checker** - 10-60x faster than alternatives

Strengths:
- Extreme speed
- Modern architecture
- Growing adoption

Weaknesses:
- Newer, less mature ecosystem
- Still catching up on edge cases

### Recommendation

| Scenario | Recommendation |
|----------|----------------|
| VS Code development | Pyright/Pylance |
| CI/CD pipeline | mypy (stricter) |
| Large monorepo | Pyright or ty |
| Django projects | mypy with django-stubs |
| Maximum strictness | Both mypy + Pyright |

## Core Concepts

### 1. Basic Type Hints

```python
# Variables (Python 3.6+)
name: str = "John"
age: int = 30
is_active: bool = True
scores: list[int] = [1, 2, 3]  # Python 3.9+
data: dict[str, int] = {"key": 1}

# Functions
def greet(name: str) -> str:
    return f"Hello, {name}"

def process(items: list[str]) -> None:
    for item in items:
        print(item)
```

### 2. Optional and Union Types

```python
# Python 3.10+ syntax (preferred)
def get_user(user_id: int) -> User | None:
    return User.objects.filter(id=user_id).first()

def process(value: int | str | float) -> str:
    return str(value)

# Legacy syntax (pre-3.10)
from typing import Optional, Union

def get_user(user_id: int) -> Optional[User]:
    return User.objects.filter(id=user_id).first()
```

### 3. Generic Types (Python 3.12+ Syntax)

```python
# New syntax (Python 3.12+) - RECOMMENDED
class Repository[T]:
    def get(self, id: int) -> T | None:
        raise NotImplementedError

    def list(self) -> list[T]:
        raise NotImplementedError

    def create(self, item: T) -> T:
        raise NotImplementedError

# With bounds
class NumberContainer[T: (int, float)]:
    def __init__(self, value: T) -> None:
        self.value = value

# Legacy syntax (pre-3.12)
from typing import TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    def get(self, id: int) -> T | None:
        raise NotImplementedError
```

### 4. Type Aliases

```python
# Python 3.12+ syntax (preferred)
type UserId = int
type UserDict = dict[str, Any]
type Callback = Callable[[int, str], bool]
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

# Generic type alias
type ListOrSet[T] = list[T] | set[T]

# Legacy syntax
from typing import TypeAlias

UserId: TypeAlias = int
UserDict: TypeAlias = dict[str, Any]
```

### 5. Protocol (Structural Subtyping)

```python
from typing import Protocol, runtime_checkable

class Sendable(Protocol):
    """Protocol for objects that can send messages."""
    def send(self, message: str) -> bool: ...

# Any class with matching method signature satisfies the protocol
class EmailClient:
    def send(self, message: str) -> bool:
        # Send email
        return True

class SMSClient:
    def send(self, message: str) -> bool:
        # Send SMS
        return True

def notify(client: Sendable, message: str) -> bool:
    """Works with any object having send() method."""
    return client.send(message)

# Runtime checking (optional)
@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

resource = SomeResource()
if isinstance(resource, Closeable):  # Works at runtime
    resource.close()
```

### 6. TypedDict

```python
from typing import TypedDict, NotRequired, Required, ReadOnly

# Basic TypedDict
class UserData(TypedDict):
    id: int
    email: str
    name: str

# With optional fields (Python 3.11+)
class UserProfile(TypedDict):
    id: int
    email: str
    bio: NotRequired[str]  # Optional field
    avatar_url: NotRequired[str | None]

# total=False with Required fields
class Config(TypedDict, total=False):
    debug: bool
    log_level: str
    api_key: Required[str]  # This one is required

# ReadOnly fields (Python 3.13+)
class ImmutableUser(TypedDict):
    id: ReadOnly[int]
    name: str  # Mutable
```

### 7. Callable and ParamSpec

```python
from collections.abc import Callable, Awaitable
from typing import ParamSpec, TypeVar, Concatenate

P = ParamSpec('P')
T = TypeVar('T')

# Basic callable
Handler = Callable[[Request], Response]
AsyncHandler = Callable[[Request], Awaitable[Response]]

# Decorator preserving signature
def logged[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Adding argument with Concatenate
def with_context[**P, T](
    func: Callable[Concatenate[Context, P], T]
) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        ctx = get_context()
        return func(ctx, *args, **kwargs)
    return wrapper
```

### 8. Dataclasses with Types

```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool = True
    tags: list[str] = field(default_factory=list)

    # Class variable (not an instance field)
    _registry: ClassVar[dict[int, "User"]] = {}

    def __post_init__(self) -> None:
        User._registry[self.id] = self

@dataclass(frozen=True)  # Immutable
class Point:
    x: float
    y: float

    def distance(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# With slots (Python 3.10+)
@dataclass(slots=True)
class HighPerformanceData:
    value: int
    label: str
```

## Framework-Specific Typing

### Django

```python
# Install: pip install django-stubs

# pyproject.toml
# [tool.mypy]
# plugins = ["mypy_django_plugin.main"]
# [tool.mypy.plugins.django-stubs]
# django_settings_module = "myproject.settings"

from django.db import models
from django.http import HttpRequest, HttpResponse, JsonResponse

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def discounted_price(self, discount: float) -> float:
        return float(self.price) * (1 - discount)

# View with typed request
def list_products(request: HttpRequest) -> JsonResponse:
    products = Product.objects.all()
    return JsonResponse({"products": list(products.values())})

# QuerySet typing
def get_active_products() -> models.QuerySet[Product]:
    return Product.objects.filter(is_active=True)
```

### FastAPI / Pydantic

```python
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    age: int = Field(ge=18, le=120)

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate) -> UserResponse:
    # Pydantic validates input automatically
    db_user = create_user_in_db(user)
    return UserResponse.model_validate(db_user)

@app.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(ge=1)],
    include_posts: Annotated[bool, Query()] = False,
) -> UserResponse:
    return get_user_from_db(user_id)
```

## LLM Usage Tips

### When Generating Code

1. **Specify Python version** - Features differ significantly between 3.9, 3.10, 3.11, 3.12
2. **Request specific type checker** - mypy and Pyright have different behaviors
3. **Mention frameworks** - Django, FastAPI, etc. have specific typing patterns
4. **Ask for strict mode** - Gets more comprehensive type coverage

### Prompt Patterns

```
"Generate a Python 3.12+ function with full type hints..."
"Add mypy-compatible type hints to this Django model..."
"Convert this function to use ParamSpec for preserving signatures..."
"Add TypedDict definitions for this API response..."
```

### Common Requests

| Need | Ask For |
|------|---------|
| Generic class | "Use Python 3.12 generic syntax `class Foo[T]:`" |
| Decorator typing | "Use ParamSpec to preserve function signature" |
| Dict structure | "Define TypedDict with Required/NotRequired" |
| Duck typing | "Use Protocol for structural subtyping" |
| Callback | "Type with Callable and proper return type" |

## Configuration Files

### mypy (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
check_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true
```

### Pyright (pyproject.toml)

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = true
reportUnusedVariable = true
```

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## External Resources

### Official Documentation
- [Python typing module](https://docs.python.org/3/library/typing.html)
- [typing specification](https://typing.python.org/en/latest/)
- [What's New in Python 3.12](https://docs.python.org/3/whatsnew/3.12.html)

### Type Checkers
- [mypy documentation](https://mypy.readthedocs.io/)
- [Pyright documentation](https://github.com/microsoft/pyright)
- [ty (Astral)](https://astral.sh/blog/ty)

### PEPs
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 544 - Protocols](https://peps.python.org/pep-0544/)
- [PEP 604 - Union Syntax](https://peps.python.org/pep-0604/)
- [PEP 612 - ParamSpec](https://peps.python.org/pep-0612/)
- [PEP 655 - Required/NotRequired](https://peps.python.org/pep-0655/)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [PEP 728 - TypedDict Extra Items](https://peps.python.org/pep-0728/)

### Tutorials and Guides
- [Real Python: Python Protocols](https://realpython.com/python-protocol/)
- [Real Python: Python 3.12 Typing](https://realpython.com/python312-typing/)
- [ParamSpec Guide](https://sobolevn.me/2021/12/paramspec-guide)
- [Better Stack: Type Hints Guide](https://betterstack.com/community/guides/scaling-python/python-type-hints/)

### Framework Stubs
- [django-stubs](https://github.com/typeddjango/django-stubs)
- [djangorestframework-stubs](https://github.com/typeddjango/djangorestframework-stubs)
- [SQLAlchemy stubs](https://docs.sqlalchemy.org/en/20/orm/extensions/mypy.html)

---

## Related Methodologies

- [python-code-quality/](../python-code-quality/) - Code quality and linting
- [django-coding-standards/](../django-coding-standards/) - Django patterns
- [python-fastapi/](../python-fastapi/) - FastAPI development

---

*Last updated: 2026-01*
