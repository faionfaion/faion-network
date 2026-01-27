# Type Hints Templates

Copy-paste patterns for common Python typing scenarios.

## Table of Contents

1. [Imports](#imports)
2. [Function Templates](#function-templates)
3. [Class Templates](#class-templates)
4. [Generic Templates](#generic-templates)
5. [Protocol Templates](#protocol-templates)
6. [TypedDict Templates](#typeddict-templates)
7. [Decorator Templates](#decorator-templates)
8. [Type Narrowing Templates](#type-narrowing-templates)
9. [Configuration Templates](#configuration-templates)
10. [Django Templates](#django-templates)
11. [FastAPI Templates](#fastapi-templates)
12. [Async Templates](#async-templates)

---

## Imports

### Standard Library Imports

```python
# Python 3.12+ - minimal imports needed
from typing import (
    # Type constructs
    Any,
    Final,
    Literal,
    TypeAlias,
    TypedDict,
    NotRequired,
    Required,
    # Type narrowing
    TypeGuard,
    TypeIs,  # Python 3.13+
    assert_never,
    # Generics (for <3.12 compatibility)
    TypeVar,
    ParamSpec,
    Generic,
    # Protocols
    Protocol,
    runtime_checkable,
    # Special types
    Annotated,
    Self,
    NoReturn,
    Never,
    # Overloads
    overload,
    # Concatenate for decorators
    Concatenate,
)

# Collections (use these for abstract types)
from collections.abc import (
    Callable,
    Awaitable,
    Coroutine,
    Iterator,
    AsyncIterator,
    Generator,
    AsyncGenerator,
    Iterable,
    Sequence,
    Mapping,
    MutableMapping,
    Set,
    MutableSet,
)

# Context managers
from contextlib import AbstractContextManager, AbstractAsyncContextManager
```

### typing_extensions (for older Python)

```python
# For Python < 3.12, use typing_extensions for newer features
from typing_extensions import (
    TypeIs,  # Python 3.13
    TypeVar,  # with default support
    ParamSpec,
    Self,
    Unpack,
    TypeVarTuple,
)
```

---

## Function Templates

### Basic Function

```python
def function_name(
    required_param: str,
    optional_param: int = 0,
    *,  # keyword-only after this
    keyword_only: bool = False,
) -> ReturnType:
    """Function docstring."""
    ...
```

### Function with Optional Return

```python
def find_item(item_id: int) -> Item | None:
    """Return item or None if not found."""
    ...
```

### Function with Multiple Return Types

```python
def process(value: int | str) -> int | str:
    """Process and return same type."""
    if isinstance(value, int):
        return value * 2
    return value.upper()
```

### Function with *args and **kwargs

```python
def variadic_function(
    *args: str,
    **kwargs: int,
) -> None:
    """Function with variadic arguments."""
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f"{key}={value}")
```

### Generator Function

```python
def generate_items(count: int) -> Iterator[Item]:
    """Generate items."""
    for i in range(count):
        yield Item(id=i)
```

### Async Function

```python
async def fetch_data(url: str) -> dict[str, Any]:
    """Fetch data from URL."""
    ...
```

### Function Never Returns

```python
def raise_error(message: str) -> NoReturn:
    """Always raises an exception."""
    raise RuntimeError(message)
```

---

## Class Templates

### Basic Class

```python
class ClassName:
    """Class docstring."""

    # Class variable
    class_var: ClassVar[int] = 0

    # Instance variables (annotated at class level)
    instance_var: str
    optional_var: int | None

    def __init__(self, instance_var: str) -> None:
        self.instance_var = instance_var
        self.optional_var = None

    def method(self, param: str) -> str:
        """Instance method."""
        return f"{self.instance_var}: {param}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create from dictionary."""
        return cls(**data)

    @staticmethod
    def utility(value: int) -> int:
        """Static utility method."""
        return value * 2

    @property
    def computed(self) -> str:
        """Computed property."""
        return self.instance_var.upper()
```

### Dataclass

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class DataClassName:
    """Dataclass with typed fields."""

    required_field: str
    optional_field: int = 0
    list_field: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def method(self) -> str:
        return self.required_field
```

### Frozen Dataclass

```python
@dataclass(frozen=True)
class ImmutableData:
    """Immutable dataclass."""

    id: int
    name: str
```

### Slots Class

```python
@dataclass(slots=True)
class SlottedData:
    """Memory-efficient dataclass with slots."""

    id: int
    name: str
```

---

## Generic Templates

### Generic Function (Python 3.12+)

```python
def first[T](items: list[T]) -> T | None:
    """Return first item or None."""
    return items[0] if items else None
```

### Generic Function with Multiple Type Parameters

```python
def zip_strict[T, U](
    first: list[T],
    second: list[U],
) -> list[tuple[T, U]]:
    """Zip two lists of equal length."""
    if len(first) != len(second):
        raise ValueError("Lists must be same length")
    return list(zip(first, second))
```

### Generic Class (Python 3.12+)

```python
class Container[T]:
    """Generic container."""

    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value
```

### Generic Class with Constraint

```python
class Processor[T: (int, float)]:
    """Process only numeric types."""

    def process(self, value: T) -> T:
        return value * 2
```

### Generic Class with Bound

```python
from abc import ABC, abstractmethod

class Entity(ABC):
    @abstractmethod
    def get_id(self) -> int: ...

class Repository[T: Entity]:
    """Repository for Entity subclasses."""

    def __init__(self) -> None:
        self._items: dict[int, T] = {}

    def get(self, id: int) -> T | None:
        return self._items.get(id)

    def save(self, item: T) -> None:
        self._items[item.get_id()] = item
```

### Legacy Generic (Python < 3.12)

```python
from typing import TypeVar, Generic

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value
```

---

## Protocol Templates

### Basic Protocol

```python
from typing import Protocol

class Readable(Protocol):
    """Protocol for readable objects."""

    def read(self, n: int = -1) -> bytes:
        """Read up to n bytes."""
        ...
```

### Protocol with Property

```python
class Sized(Protocol):
    """Protocol with property."""

    @property
    def size(self) -> int:
        """Return size."""
        ...
```

### Protocol with Generic

```python
class Comparable[T](Protocol):
    """Protocol for comparable objects."""

    def __lt__(self, other: T) -> bool: ...
    def __le__(self, other: T) -> bool: ...
    def __gt__(self, other: T) -> bool: ...
    def __ge__(self, other: T) -> bool: ...
```

### Runtime Checkable Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    """Runtime checkable protocol."""

    def close(self) -> None:
        """Close the resource."""
        ...

# Can use isinstance()
def close_if_possible(obj: object) -> None:
    if isinstance(obj, Closeable):
        obj.close()
```

### Callback Protocol

```python
class Handler(Protocol):
    """Protocol for handler callables."""

    def __call__(self, event: Event) -> bool:
        """Handle event, return True if handled."""
        ...
```

---

## TypedDict Templates

### Basic TypedDict

```python
from typing import TypedDict

class UserData(TypedDict):
    """User data structure."""

    id: int
    email: str
    name: str
```

### TypedDict with Optional Fields

```python
from typing import TypedDict, NotRequired

class UserDataOptional(TypedDict):
    """User data with optional fields."""

    id: int
    email: str
    name: NotRequired[str]
    age: NotRequired[int]
```

### TypedDict total=False

```python
from typing import TypedDict, Required

class UpdateData(TypedDict, total=False):
    """All fields optional except Required ones."""

    email: Required[str]  # This is required
    name: str  # Optional
    age: int  # Optional
```

### Nested TypedDict

```python
class Address(TypedDict):
    street: str
    city: str
    zip_code: str

class Person(TypedDict):
    name: str
    address: Address
```

### TypedDict with Inheritance

```python
class BaseRecord(TypedDict):
    id: int
    created_at: str

class UserRecord(BaseRecord):
    email: str
    name: str
```

---

## Decorator Templates

### Simple Decorator

```python
from functools import wraps
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def simple_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that preserves signature."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper
```

### Decorator with Arguments

```python
def repeat(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator factory with arguments."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for _ in range(times - 1):
                func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator

@repeat(3)
def greet(name: str) -> str:
    return f"Hello, {name}"
```

### Async Decorator

```python
from collections.abc import Awaitable, Callable

def async_decorator[**P, R](
    func: Callable[P, Awaitable[R]]
) -> Callable[P, Awaitable[R]]:
    """Decorator for async functions."""

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling async {func.__name__}")
        return await func(*args, **kwargs)

    return wrapper
```

### Method Decorator

```python
from typing import Concatenate

def method_decorator[T, **P, R](
    func: Callable[Concatenate[T, P], R]
) -> Callable[Concatenate[T, P], R]:
    """Decorator for methods (preserves self)."""

    @wraps(func)
    def wrapper(self: T, *args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Method {func.__name__} on {type(self).__name__}")
        return func(self, *args, **kwargs)

    return wrapper
```

---

## Type Narrowing Templates

### TypeIs Function

```python
from typing import TypeIs

def is_string(value: object) -> TypeIs[str]:
    """Type narrowing that works in both branches."""
    return isinstance(value, str)

def process(value: int | str) -> None:
    if is_string(value):
        print(value.upper())  # str
    else:
        print(value + 1)  # int
```

### TypeGuard Function

```python
from typing import TypeGuard

def is_str_list(value: list[object]) -> TypeGuard[list[str]]:
    """Check if all list items are strings."""
    return all(isinstance(x, str) for x in value)
```

### assert_not_none Helper

```python
def assert_not_none[T](value: T | None, message: str = "") -> T:
    """Assert value is not None."""
    if value is None:
        raise ValueError(message or "Unexpected None")
    return value
```

### Exhaustiveness Check

```python
from typing import assert_never, Literal

Status = Literal["pending", "active", "closed"]

def handle_status(status: Status) -> str:
    match status:
        case "pending":
            return "Waiting"
        case "active":
            return "In progress"
        case "closed":
            return "Done"
        case _:
            assert_never(status)
```

---

## Configuration Templates

### mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
extra_checks = true

# Per-module overrides
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
strict = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true

[[tool.mypy.overrides]]
module = "untyped_library.*"
ignore_missing_imports = true
```

### pyright Configuration

```toml
# pyproject.toml
[tool.pyright]
pythonVersion = "3.12"
pythonPlatform = "Linux"
typeCheckingMode = "strict"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = true
reportUnusedVariable = true
reportDuplicateImport = true
reportPrivateUsage = true
reportConstantRedefinition = true
venvPath = "."
venv = ".venv"
```

### Django mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["mypy_django_plugin.main"]

[tool.django-stubs]
django_settings_module = "myproject.settings"

[[tool.mypy.overrides]]
module = "*.migrations.*"
ignore_errors = true
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - django-stubs
          - types-requests
        args: [--strict]
```

---

## Django Templates

### Model with Type Hints

```python
from django.db import models
from django.db.models import QuerySet, Manager
from typing import ClassVar

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    # Typed manager
    objects: ClassVar[Manager["User"]]

    class Meta:
        verbose_name = "User"

    def __str__(self) -> str:
        return self.email
```

### Service with Typed QuerySet

```python
from django.db.models import QuerySet

class UserService:
    def get_active_users(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)

    def get_by_email(self, email: str) -> User | None:
        return User.objects.filter(email=email).first()

    def get_or_404(self, user_id: int) -> User:
        from django.shortcuts import get_object_or_404
        return get_object_or_404(User, pk=user_id)

    def create(
        self,
        email: str,
        name: str,
        *,
        is_active: bool = True,
    ) -> User:
        return User.objects.create(
            email=email,
            name=name,
            is_active=is_active,
        )
```

### View with Type Hints

```python
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def user_list(request: HttpRequest) -> HttpResponse:
    users = User.objects.all()
    return render(request, "users/list.html", {"users": users})

@require_http_methods(["GET", "POST"])
def user_detail(request: HttpRequest, user_id: int) -> HttpResponse:
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        # Handle form
        pass
    return render(request, "users/detail.html", {"user": user})
```

---

## FastAPI Templates

### Basic Endpoint

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    model_config = {"from_attributes": True}

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate) -> UserResponse:
    new_user = await db.create_user(**user.model_dump())
    return UserResponse.model_validate(new_user)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
```

### Annotated Dependencies

```python
from typing import Annotated
from fastapi import Depends, Query, Header

async def get_db() -> AsyncGenerator[Session, None]:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: Annotated[str, Header()],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    user = await db.get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401)
    return user

DbDep = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/me")
async def get_me(user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(user)
```

### Paginated Response

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int

    @property
    def has_next(self) -> bool:
        return self.page * self.page_size < self.total

@app.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    db: DbDep = None,
) -> PaginatedResponse[UserResponse]:
    total = await db.count_users()
    users = await db.get_users(
        skip=(page - 1) * page_size,
        limit=page_size,
    )
    return PaginatedResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
    )
```

---

## Async Templates

### Async Function

```python
async def fetch_data(url: str) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### Async Generator

```python
async def stream_items(count: int) -> AsyncIterator[Item]:
    for i in range(count):
        await asyncio.sleep(0.1)
        yield Item(id=i)
```

### Async Context Manager

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

@asynccontextmanager
async def get_connection() -> AsyncIterator[Connection]:
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()
```

### Concurrent Execution

```python
async def fetch_all[T](
    urls: list[str],
    parser: Callable[[dict[str, Any]], T],
) -> list[T]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return [parser(r) for r in results]
```

### Async Queue Processing

```python
async def process_queue[T](
    queue: asyncio.Queue[T],
    handler: Callable[[T], Awaitable[None]],
) -> None:
    while True:
        item = await queue.get()
        try:
            await handler(item)
        finally:
            queue.task_done()
```
