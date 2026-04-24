# Type Hints Examples

Real-world typing examples for various Python scenarios.

## Table of Contents

1. [Basic Types](#basic-types)
2. [Generic Functions (Python 3.12+)](#generic-functions-python-312)
3. [Generic Classes](#generic-classes)
4. [TypeVar Constraints and Bounds](#typevar-constraints-and-bounds)
5. [Protocol and Structural Subtyping](#protocol-and-structural-subtyping)
6. [TypedDict](#typeddict)
7. [Callable and ParamSpec](#callable-and-paramspec)
8. [Type Narrowing](#type-narrowing)
9. [Literal and Final](#literal-and-final)
10. [Annotated](#annotated)
11. [Django Examples](#django-examples)
12. [FastAPI Examples](#fastapi-examples)
13. [Async Patterns](#async-patterns)
14. [Dataclasses](#dataclasses)

---

## Basic Types

### Variables and Collections

```python
from datetime import datetime
from decimal import Decimal

# Primitives
name: str = "Alice"
age: int = 30
balance: Decimal = Decimal("100.50")
created: datetime = datetime.now()

# Collections (Python 3.9+)
tags: list[str] = ["python", "typing"]
scores: dict[str, int] = {"alice": 95, "bob": 87}
unique_ids: set[int] = {1, 2, 3}
point: tuple[float, float] = (10.5, 20.3)
point_3d: tuple[float, float, float] = (1.0, 2.0, 3.0)

# Variable-length tuple
numbers: tuple[int, ...] = (1, 2, 3, 4, 5)

# Nested collections
matrix: list[list[int]] = [[1, 2], [3, 4]]
user_scores: dict[str, list[int]] = {"alice": [95, 87, 92]}
```

### Function Signatures

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def add_numbers(a: int, b: int) -> int:
    return a + b

def process_items(items: list[str]) -> None:
    for item in items:
        print(item)

# Optional parameters
def create_user(
    email: str,
    name: str,
    *,  # Keyword-only after this
    age: int | None = None,
    active: bool = True,
) -> "User":
    return User(email=email, name=name, age=age, active=active)

# *args and **kwargs
def log_message(message: str, *args: str, **kwargs: int) -> None:
    print(message, args, kwargs)
```

---

## Generic Functions (Python 3.12+)

### New Type Parameter Syntax

```python
# Python 3.12+ - no imports needed for generics
def first[T](items: list[T]) -> T | None:
    """Return first item or None if empty."""
    return items[0] if items else None

def last[T](items: list[T]) -> T | None:
    """Return last item or None if empty."""
    return items[-1] if items else None

def identity[T](value: T) -> T:
    """Return the same value."""
    return value

# Multiple type parameters
def swap[T, U](pair: tuple[T, U]) -> tuple[U, T]:
    """Swap elements in a tuple."""
    return (pair[1], pair[0])

def merge_dicts[K, V](d1: dict[K, V], d2: dict[K, V]) -> dict[K, V]:
    """Merge two dictionaries."""
    return {**d1, **d2}

# With default value (Python 3.13+)
def get_or_default[T = str](
    mapping: dict[str, T],
    key: str,
    default: T,
) -> T:
    return mapping.get(key, default)
```

### Legacy TypeVar Syntax (Python < 3.12)

```python
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

---

## Generic Classes

### Python 3.12+ Syntax

```python
class Stack[T]:
    """Generic stack implementation."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        return len(self._items) == 0


class Repository[T]:
    """Generic repository pattern."""

    def __init__(self, model_class: type[T]) -> None:
        self.model_class = model_class
        self._storage: dict[int, T] = {}
        self._next_id = 1

    def get(self, id: int) -> T | None:
        return self._storage.get(id)

    def get_or_raise(self, id: int) -> T:
        item = self._storage.get(id)
        if item is None:
            raise KeyError(f"{self.model_class.__name__} with id {id} not found")
        return item

    def list(self) -> list[T]:
        return list(self._storage.values())

    def create(self, item: T) -> T:
        self._storage[self._next_id] = item
        self._next_id += 1
        return item

    def delete(self, id: int) -> bool:
        return self._storage.pop(id, None) is not None


# Multiple type parameters
class Pair[T, U]:
    """Generic pair container."""

    def __init__(self, first: T, second: U) -> None:
        self.first = first
        self.second = second

    def swap(self) -> "Pair[U, T]":
        return Pair(self.second, self.first)


# Usage
stack: Stack[int] = Stack()
stack.push(1)
stack.push(2)
value: int = stack.pop()

pair = Pair("hello", 42)
swapped = pair.swap()  # Pair[int, str]
```

---

## TypeVar Constraints and Bounds

### Constrained TypeVar

```python
from typing import TypeVar

# Constrained to specific types
Number = TypeVar("Number", int, float, complex)

def add_numbers(a: Number, b: Number) -> Number:
    return a + b

# Python 3.12+ syntax
def add[T: (int, float, complex)](a: T, b: T) -> T:
    return a + b

# Works
add_numbers(1, 2)       # int
add_numbers(1.5, 2.5)   # float

# Error: str not in constraint
# add_numbers("a", "b")
```

### Bounded TypeVar

```python
from typing import TypeVar

class Animal:
    def speak(self) -> str:
        return "..."

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

# Bound to Animal or subclasses
T_Animal = TypeVar("T_Animal", bound=Animal)

def make_speak(animal: T_Animal) -> str:
    return animal.speak()

# Python 3.12+ syntax with bound
def make_speak_new[T: Animal](animal: T) -> str:
    return animal.speak()

# Works with Animal and subclasses
make_speak(Dog())  # "Woof!"
make_speak(Cat())  # "Meow!"
```

### Covariant and Contravariant

```python
from typing import TypeVar, Generic

# Covariant - can use subtype
T_co = TypeVar("T_co", covariant=True)

class ImmutableList(Generic[T_co]):
    """Read-only list - covariant."""

    def __init__(self, items: list[T_co]) -> None:
        self._items = items

    def __getitem__(self, index: int) -> T_co:
        return self._items[index]

# Contravariant - can use supertype
T_contra = TypeVar("T_contra", contravariant=True)

class Consumer(Generic[T_contra]):
    """Consumer - contravariant."""

    def consume(self, item: T_contra) -> None:
        print(item)

# Python 3.12+ with infer_variance
class Box[T](Generic[T]):  # Invariant by default
    def __init__(self, value: T) -> None:
        self.value = value
```

---

## Protocol and Structural Subtyping

### Basic Protocol

```python
from typing import Protocol, runtime_checkable

class Drawable(Protocol):
    """Protocol for drawable objects."""

    def draw(self) -> None:
        """Draw the object."""
        ...

class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> None:
        print(f"Drawing circle with radius {self.radius}")

class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    def draw(self) -> None:
        print(f"Drawing square with side {self.side}")

def render(shape: Drawable) -> None:
    """Render any drawable shape."""
    shape.draw()

# Both work - structural subtyping
render(Circle(5.0))
render(Square(10.0))
```

### Protocol with Properties

```python
from typing import Protocol

class Sizeable(Protocol):
    @property
    def size(self) -> int:
        ...

class Array:
    def __init__(self, data: list[int]) -> None:
        self._data = data

    @property
    def size(self) -> int:
        return len(self._data)

def print_size(obj: Sizeable) -> None:
    print(f"Size: {obj.size}")

print_size(Array([1, 2, 3]))  # Works!
```

### Generic Protocol

```python
from typing import Protocol

class Comparable[T](Protocol):
    def __lt__(self, other: T) -> bool:
        ...

    def __gt__(self, other: T) -> bool:
        ...

def max_value[T: Comparable[T]](a: T, b: T) -> T:
    return a if a > b else b

# Works with any comparable type
max_value(1, 2)  # int
max_value("a", "b")  # str
```

### Callback Protocol

```python
from typing import Protocol

class RequestHandler(Protocol):
    """Protocol for request handlers."""

    def __call__(self, request: "Request") -> "Response":
        ...

class AsyncRequestHandler(Protocol):
    """Protocol for async request handlers."""

    async def __call__(self, request: "Request") -> "Response":
        ...

def process_request(handler: RequestHandler, request: "Request") -> "Response":
    return handler(request)
```

### Runtime Checkable

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None:
        ...

class FileWrapper:
    def close(self) -> None:
        print("Closing file")

class DatabaseConnection:
    def close(self) -> None:
        print("Closing connection")

def is_closeable(obj: object) -> bool:
    return isinstance(obj, Closeable)

# Runtime checks work
print(is_closeable(FileWrapper()))  # True
print(is_closeable("string"))  # False
```

---

## TypedDict

### Basic TypedDict

```python
from typing import TypedDict, NotRequired, Required

class UserData(TypedDict):
    """User data structure."""
    id: int
    email: str
    name: str

class UserDataOptional(TypedDict):
    """User data with optional fields."""
    id: int
    email: str
    name: NotRequired[str]  # Optional field
    age: NotRequired[int]

def create_user(data: UserData) -> "User":
    return User(**data)

# Valid
user: UserData = {"id": 1, "email": "test@example.com", "name": "Test"}

# Invalid - missing required field
# user: UserData = {"id": 1, "email": "test@example.com"}
```

### TypedDict with total=False

```python
from typing import TypedDict, Required

class UpdateUserData(TypedDict, total=False):
    """All fields optional by default."""
    email: Required[str]  # But this is required
    name: str
    age: int
    bio: str

def update_user(user_id: int, data: UpdateUserData) -> None:
    print(f"Updating user {user_id} with {data}")

# Only email is required
update_user(1, {"email": "new@example.com"})
update_user(1, {"email": "new@example.com", "name": "New Name"})
```

### Nested TypedDict

```python
from typing import TypedDict

class Address(TypedDict):
    street: str
    city: str
    country: str
    zip_code: str

class Person(TypedDict):
    name: str
    age: int
    address: Address

person: Person = {
    "name": "Alice",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Springfield",
        "country": "USA",
        "zip_code": "12345",
    },
}
```

### TypedDict Inheritance

```python
from typing import TypedDict, NotRequired

class BaseUser(TypedDict):
    id: int
    email: str

class AdminUser(BaseUser):
    """Extends BaseUser with admin fields."""
    role: str
    permissions: list[str]

class GuestUser(BaseUser):
    """Extends BaseUser with guest fields."""
    expires_at: NotRequired[str]
```

---

## Callable and ParamSpec

### Basic Callable

```python
from collections.abc import Callable, Awaitable

# Simple callback
Handler = Callable[[str], None]

def process(message: str, handler: Handler) -> None:
    handler(message)

# With multiple parameters
Calculator = Callable[[int, int], int]

def apply(a: int, b: int, operation: Calculator) -> int:
    return operation(a, b)

# Async callable
AsyncHandler = Callable[[str], Awaitable[None]]

async def process_async(message: str, handler: AsyncHandler) -> None:
    await handler(message)
```

### ParamSpec for Decorators

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
import time

P = ParamSpec("P")
R = TypeVar("R")

def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that times function execution."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result

    return wrapper

@timer
def slow_function(x: int, y: str) -> str:
    time.sleep(0.1)
    return f"{x}: {y}"

# Type signature preserved
result: str = slow_function(42, "hello")
```

### Python 3.12+ ParamSpec Syntax

```python
from collections.abc import Callable
from functools import wraps

def logged[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """Log function calls."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper

@logged
def greet(name: str, excited: bool = False) -> str:
    suffix = "!" if excited else "."
    return f"Hello, {name}{suffix}"
```

### Concatenate for Parameter Modification

```python
from typing import ParamSpec, TypeVar, Concatenate
from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")

class Context:
    user: str = "anonymous"

def with_context(
    func: Callable[Concatenate[Context, P], R]
) -> Callable[P, R]:
    """Add context as first parameter."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        ctx = Context()
        return func(ctx, *args, **kwargs)

    return wrapper

@with_context
def get_user_data(ctx: Context, user_id: int) -> dict[str, str]:
    return {"user_id": str(user_id), "requested_by": ctx.user}

# Call without context - it's injected
data = get_user_data(123)
```

---

## Type Narrowing

### isinstance Narrowing

```python
def process(value: int | str | list[int]) -> str:
    if isinstance(value, int):
        # value is int here
        return f"Integer: {value * 2}"
    elif isinstance(value, str):
        # value is str here
        return f"String: {value.upper()}"
    else:
        # value is list[int] here
        return f"List sum: {sum(value)}"
```

### TypeIs (Python 3.13+)

```python
from typing import TypeIs

def is_str_list(value: list[object]) -> TypeIs[list[str]]:
    """Check if all items are strings."""
    return all(isinstance(x, str) for x in value)

def process_items(items: list[object]) -> None:
    if is_str_list(items):
        # items is list[str] here
        for item in items:
            print(item.upper())
    else:
        # items is still list[object] here
        # (TypeIs narrows in both branches)
        print("Not all strings")

def is_positive(x: int) -> TypeIs[int]:
    """TypeIs for same type - useful for constraints."""
    return x > 0
```

### TypeGuard (One-way Narrowing)

```python
from typing import TypeGuard

def is_str_list(value: list[object]) -> TypeGuard[list[str]]:
    """Check if all items are strings."""
    return all(isinstance(x, str) for x in value)

def process(items: list[object]) -> None:
    if is_str_list(items):
        # items is list[str] here
        for item in items:
            print(item.upper())
    else:
        # items is still list[object] here
        # (TypeGuard doesn't narrow else branch)
        pass
```

### assert_never for Exhaustiveness

```python
from typing import assert_never, Literal

Status = Literal["pending", "approved", "rejected"]

def handle_status(status: Status) -> str:
    if status == "pending":
        return "Waiting for review"
    elif status == "approved":
        return "Request approved"
    elif status == "rejected":
        return "Request rejected"
    else:
        # Type checker error if Status is extended
        assert_never(status)

# If you add a new status like "cancelled" to Status,
# assert_never will cause a type error until you handle it
```

### None Narrowing

```python
def assert_not_none[T](value: T | None, message: str = "") -> T:
    """Assert value is not None and narrow type."""
    if value is None:
        raise ValueError(message or "Unexpected None")
    return value

def get_user(user_id: int) -> "User | None":
    ...

# Usage
user = get_user(123)
# user is User | None

verified_user = assert_not_none(user, "User not found")
# verified_user is User
```

---

## Literal and Final

### Literal Types

```python
from typing import Literal

# Literal string values
Direction = Literal["north", "south", "east", "west"]

def move(direction: Direction, steps: int) -> None:
    print(f"Moving {direction} by {steps} steps")

move("north", 5)  # OK
# move("up", 5)  # Error: "up" not in Literal

# Literal with multiple types
Result = Literal[True, False, "error"]

def validate(data: dict[str, str]) -> Result:
    if not data:
        return "error"
    return True

# Literal numbers
HttpStatus = Literal[200, 201, 400, 404, 500]

def handle_response(status: HttpStatus) -> str:
    if status == 200:
        return "OK"
    elif status == 404:
        return "Not Found"
    ...
```

### Final Values

```python
from typing import Final

# Constant values
MAX_RETRIES: Final = 3
API_VERSION: Final[str] = "v1"
DEBUG: Final[bool] = False

class Config:
    # Class-level constant
    MAX_CONNECTIONS: Final = 100

    def __init__(self) -> None:
        # Instance constant
        self.name: Final = "MyApp"

# Reassignment error
# MAX_RETRIES = 5  # Type error

# Final methods (cannot be overridden)
from typing import final

class Base:
    @final
    def critical_method(self) -> None:
        """This method cannot be overridden."""
        pass

# Final class (cannot be subclassed)
@final
class Singleton:
    pass
```

---

## Annotated

### Basic Annotated

```python
from typing import Annotated

# Type with metadata
UserId = Annotated[int, "User identifier"]
Email = Annotated[str, "Valid email address"]

def get_user(user_id: UserId) -> "User":
    ...

def send_email(to: Email, subject: str) -> None:
    ...
```

### Annotated with Validators

```python
from typing import Annotated
from pydantic import Field, BaseModel

class User(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    age: Annotated[int, Field(ge=0, le=150)]
    email: Annotated[str, Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")]

# FastAPI with Annotated
from fastapi import Query, Path

async def search(
    q: Annotated[str, Query(min_length=1, max_length=50)],
    page: Annotated[int, Query(ge=1)] = 1,
) -> list["Item"]:
    ...

async def get_item(
    item_id: Annotated[int, Path(ge=1, description="Item ID")],
) -> "Item":
    ...
```

### Custom Annotated Validators

```python
from typing import Annotated, get_type_hints, get_origin, get_args

class Positive:
    """Marker for positive numbers."""
    pass

class NonEmpty:
    """Marker for non-empty strings."""
    pass

PositiveInt = Annotated[int, Positive()]
NonEmptyStr = Annotated[str, NonEmpty()]

def validate_annotated(value: object, expected_type: type) -> bool:
    """Basic validator using Annotated metadata."""
    origin = get_origin(expected_type)
    if origin is Annotated:
        args = get_args(expected_type)
        base_type = args[0]
        metadata = args[1:]

        if not isinstance(value, base_type):
            return False

        for meta in metadata:
            if isinstance(meta, Positive) and value <= 0:
                return False
            if isinstance(meta, NonEmpty) and value == "":
                return False

    return True
```

---

## Django Examples

### Model Types

```python
from django.db import models
from django.db.models import QuerySet, Manager

class User(models.Model):
    email: models.EmailField[str, str] = models.EmailField(unique=True)
    name: models.CharField[str, str] = models.CharField(max_length=100)
    is_active: models.BooleanField[bool, bool] = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    # Typed related manager (using string annotation)
    orders: "Manager[Order]"

    class Meta:
        verbose_name = "User"

class Order(models.Model):
    user: models.ForeignKey[User, User] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    total: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
```

### QuerySet Returns

```python
from django.db.models import QuerySet

def get_active_users() -> QuerySet[User]:
    """Return queryset of active users."""
    return User.objects.filter(is_active=True)

def get_user_by_email(email: str) -> User | None:
    """Return user by email or None."""
    return User.objects.filter(email=email).first()

def get_user_or_404(user_id: int) -> User:
    """Return user or raise 404."""
    from django.shortcuts import get_object_or_404
    return get_object_or_404(User, pk=user_id)

def list_users(
    *,
    active_only: bool = False,
    limit: int | None = None,
) -> list[User]:
    """Return list of users with optional filters."""
    qs = User.objects.all()
    if active_only:
        qs = qs.filter(is_active=True)
    if limit:
        qs = qs[:limit]
    return list(qs)
```

### View Types

```python
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View

def user_detail(request: HttpRequest, user_id: int) -> HttpResponse:
    """Function-based view with typed parameters."""
    user = get_object_or_404(User, pk=user_id)
    return render(request, "user_detail.html", {"user": user})

class UserListView(View):
    """Class-based view with typed methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        users = User.objects.all()
        return render(request, "user_list.html", {"users": users})

    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body)
        user = User.objects.create(**data)
        return JsonResponse({"id": user.id}, status=201)
```

### Form Types

```python
from django import forms
from typing import Any

class UserForm(forms.ModelForm[User]):
    class Meta:
        model = User
        fields = ["email", "name"]

    def clean_email(self) -> str:
        email: str = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit: bool = True) -> User:
        return super().save(commit=commit)
```

---

## FastAPI Examples

### Basic Endpoints

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int | None = None

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    model_config = {"from_attributes": True}

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserResponse:
    # user is validated UserCreate
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
from fastapi import Depends, Query, Path, Header

async def get_db() -> "AsyncSession":
    async with async_session() as session:
        yield session

async def get_current_user(
    token: Annotated[str, Header()],
    db: Annotated["AsyncSession", Depends(get_db)],
) -> "User":
    user = await db.get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401)
    return user

@app.get("/items")
async def list_items(
    db: Annotated["AsyncSession", Depends(get_db)],
    user: Annotated["User", Depends(get_current_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> list["Item"]:
    return await db.list_items(user_id=user.id, skip=skip, limit=limit)
```

### Generic Response Models

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool

class UserListResponse(PaginatedResponse[UserResponse]):
    pass

@app.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PaginatedResponse[UserResponse]:
    ...
```

---

## Async Patterns

### Async Functions

```python
from collections.abc import Awaitable, AsyncIterator
import asyncio

async def fetch_user(user_id: int) -> User | None:
    """Async function returning optional User."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/users/{user_id}") as response:
            if response.status == 404:
                return None
            data = await response.json()
            return User(**data)

async def fetch_all_users(user_ids: list[int]) -> list[User]:
    """Fetch multiple users concurrently."""
    tasks: list[Awaitable[User | None]] = [
        fetch_user(uid) for uid in user_ids
    ]
    results = await asyncio.gather(*tasks)
    return [u for u in results if u is not None]
```

### Async Generators

```python
async def stream_users(
    batch_size: int = 100,
) -> AsyncIterator[User]:
    """Stream users in batches."""
    offset = 0
    while True:
        users = await db.get_users(limit=batch_size, offset=offset)
        if not users:
            break
        for user in users:
            yield user
        offset += batch_size

async def process_stream() -> None:
    async for user in stream_users():
        await process_user(user)
```

### Async Context Managers

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

@asynccontextmanager
async def get_connection() -> AsyncIterator["Connection"]:
    """Async context manager for database connection."""
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()

async def main() -> None:
    async with get_connection() as conn:
        await conn.execute("SELECT 1")
```

---

## Dataclasses

### Basic Dataclass

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class Point:
    """Immutable point."""
    x: float
    y: float

    def distance(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
```

### Generic Dataclass (Python 3.12+)

```python
from dataclasses import dataclass

@dataclass
class Result[T]:
    """Generic result container."""
    value: T | None
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.error is None

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def failure(cls, error: str) -> "Result[T]":
        return cls(value=None, error=error)

# Usage
result: Result[User] = Result.success(user)
if result.is_success:
    print(result.value)
```

### Dataclass with Validation

```python
from dataclasses import dataclass

@dataclass
class User:
    email: str
    age: int

    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError("Invalid email")
        if self.age < 0:
            raise ValueError("Age must be non-negative")
```
