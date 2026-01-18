# M-PY-006: Type Hints

## Metadata
- **Category:** Development/Python
- **Difficulty:** Beginner
- **Tags:** #dev, #python, #typing, #methodology
- **Agent:** faion-code-agent

---

## Problem

Dynamic typing makes Python flexible but error-prone. Bugs hide until runtime. IDEs cannot help without type information. Code intent is unclear without reading implementation.

## Promise

After this methodology, you will write Python code that catches errors at development time, has better IDE support, and is self-documenting.

## Overview

Type hints add optional static typing to Python. They do not affect runtime but enable static analysis with tools like mypy.

---

## Framework

### Step 1: Basic Types

```python
# Built-in types
name: str = "Alice"
age: int = 30
price: float = 19.99
is_active: bool = True

# Function annotations
def greet(name: str) -> str:
    return f"Hello, {name}"

# None type
def find_user(id: int) -> str | None:
    # Returns string or None
    pass

# Multiple types (Union)
def process(value: int | str) -> None:
    pass
```

### Step 2: Collections

```python
# List
def get_names() -> list[str]:
    return ["Alice", "Bob"]

# Dict
def get_config() -> dict[str, int]:
    return {"timeout": 30, "retries": 3}

# Tuple (fixed length)
def get_coordinates() -> tuple[float, float]:
    return (52.5, 13.4)

# Tuple (variable length)
def get_values() -> tuple[int, ...]:
    return (1, 2, 3, 4, 5)

# Set
def get_unique_ids() -> set[int]:
    return {1, 2, 3}
```

### Step 3: Optional and Default Values

```python
# Optional = X | None
from typing import Optional

def find_user(id: int) -> Optional[User]:
    # Same as User | None
    pass

# Default values
def connect(host: str, port: int = 8080) -> Connection:
    pass

# None as default
def fetch(url: str, timeout: float | None = None) -> Response:
    pass
```

### Step 4: Type Aliases

```python
from typing import TypeAlias

# Simple alias
UserId: TypeAlias = int
UserDict: TypeAlias = dict[str, str | int | bool]

# Complex alias
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]

def parse_json(data: str) -> JsonValue:
    pass

# NewType for distinct types (stricter)
from typing import NewType

UserId = NewType("UserId", int)
ProductId = NewType("ProductId", int)

def get_user(user_id: UserId) -> User:
    pass

# user_id: int = 123
# get_user(user_id)  # mypy error: expected UserId
# get_user(UserId(123))  # OK
```

### Step 5: Callable and Functions

```python
from typing import Callable

# Function that takes no args, returns int
Counter: TypeAlias = Callable[[], int]

# Function that takes str and int, returns bool
Validator: TypeAlias = Callable[[str, int], bool]

# Any callable
AnyFunc: TypeAlias = Callable[..., Any]

# Using in function signature
def apply_function(
    func: Callable[[int], int],
    value: int
) -> int:
    return func(value)

# Callback example
def process_data(
    data: list[str],
    on_complete: Callable[[list[str]], None]
) -> None:
    result = [item.upper() for item in data]
    on_complete(result)
```

### Step 6: Generics

```python
from typing import TypeVar, Generic

# Type variable
T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Usage
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
value: int = int_stack.pop()

# Bounded type variable
from typing import TypeVar
Comparable = TypeVar("Comparable", bound="SupportsLessThan")

def min_value(a: Comparable, b: Comparable) -> Comparable:
    return a if a < b else b
```

### Step 7: Protocols

```python
from typing import Protocol

# Structural typing (duck typing)
class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

# Any class with draw() method works
def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())  # OK
render(Square())  # OK

# Protocol with properties
class Sized(Protocol):
    @property
    def size(self) -> int: ...

# Protocol with class methods
class Factory(Protocol[T]):
    def create(self) -> T: ...
```

### Step 8: TypedDict

```python
from typing import TypedDict, Required, NotRequired

# Required fields
class UserDict(TypedDict):
    id: int
    name: str
    email: str

# Mixed required/optional
class Config(TypedDict, total=False):
    host: Required[str]
    port: int  # Optional
    debug: bool  # Optional

# Nested TypedDict
class Address(TypedDict):
    street: str
    city: str

class Person(TypedDict):
    name: str
    address: Address

# Usage
user: UserDict = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}
```

---

## Templates

### mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true

[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = ["external_lib.*"]
ignore_missing_imports = true
```

### Type Stubs

```python
# stubs/external_lib.pyi
from typing import Any

def external_function(arg: str) -> dict[str, Any]: ...

class ExternalClass:
    def method(self, value: int) -> str: ...
```

### Common Patterns

```python
from typing import (
    Any,
    ClassVar,
    Final,
    Literal,
    Self,
    TypeVar,
    overload,
)

# Class variable
class Config:
    DEFAULT_TIMEOUT: ClassVar[int] = 30

# Final (constant)
MAX_RETRIES: Final = 3

# Literal types
def set_mode(mode: Literal["read", "write", "append"]) -> None:
    pass

# Self (Python 3.11+)
class Builder:
    def with_name(self, name: str) -> Self:
        self.name = name
        return self

# Overloads
@overload
def parse(data: str) -> dict: ...
@overload
def parse(data: bytes) -> dict: ...

def parse(data: str | bytes) -> dict:
    if isinstance(data, bytes):
        data = data.decode()
    return json.loads(data)
```

---

## Examples

### Dataclass with Types

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    name: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)
```

### Pydantic Models

```python
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: int | None = Field(None, ge=0, le=150)
    tags: list[str] = []

# Automatic validation + serialization
user = User(id=1, email="user@example.com", name="Alice")
```

### Async Types

```python
from typing import AsyncIterator, Coroutine, Awaitable

async def fetch_data() -> str:
    return "data"

# Coroutine type
coro: Coroutine[Any, Any, str] = fetch_data()

# Awaitable
async def process(awaitable: Awaitable[str]) -> str:
    return await awaitable

# Async iterator
async def generate() -> AsyncIterator[int]:
    for i in range(10):
        yield i
```

---

## Common Mistakes

1. **Mixing mutable defaults** - Use `field(default_factory=list)` for mutable defaults
2. **Ignoring None** - Always handle `X | None` explicitly
3. **Using Any everywhere** - Defeats purpose of type hints
4. **Forgetting return type** - Always annotate return types
5. **Circular imports** - Use `from __future__ import annotations`

---

## Checklist

- [ ] mypy configured in pyproject.toml
- [ ] All functions annotated
- [ ] No untyped definitions
- [ ] Optional values handled
- [ ] Generic types used appropriately
- [ ] Protocols for duck typing
- [ ] Type stubs for external libs
- [ ] CI runs mypy checks

---

## Next Steps

- M-PY-004: Pytest Testing
- M-PY-008: Code Quality

---

*Methodology M-PY-006 v1.0*
