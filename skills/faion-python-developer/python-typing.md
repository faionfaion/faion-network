# Python Type Hints and mypy

**Type safety, static analysis, better IDE support**

---

## Problem

Python code needs type safety for better IDE support, documentation, and catching bugs early.

## Framework

### Basic Type Hints

```python
from typing import Any

# Variables
name: str = "John"
age: int = 30
is_active: bool = True
scores: list[int] = [1, 2, 3]
data: dict[str, Any] = {"key": "value"}

# Functions
def greet(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[str]) -> None:
    for item in items:
        print(item)
```

### Optional and Union Types

```python
from typing import Optional

# Optional (value or None)
def get_user(user_id: int) -> Optional[User]:
    """Return user or None if not found."""
    return User.objects.filter(id=user_id).first()

# Modern syntax (Python 3.10+)
def get_user(user_id: int) -> User | None:
    """Return user or None if not found."""
    return User.objects.filter(id=user_id).first()

# Union of types
def process(value: int | str) -> str:
    return str(value)
```

### Generic Types

```python
from typing import TypeVar, Generic
from collections.abc import Sequence, Mapping

T = TypeVar('T')

class Repository(Generic[T]):
    """Generic repository pattern."""

    def get(self, id: int) -> T | None:
        raise NotImplementedError

    def list(self) -> list[T]:
        raise NotImplementedError

    def create(self, item: T) -> T:
        raise NotImplementedError


# Using the generic
class UserRepository(Repository[User]):
    def get(self, id: int) -> User | None:
        return User.objects.filter(id=id).first()


# Type aliases
UserId = int
UserDict = dict[str, Any]
Callback = Callable[[int, str], bool]
```

### Callable Types

```python
from collections.abc import Callable

# Function that takes a callback
def apply_operation(
    values: list[int],
    operation: Callable[[int], int],
) -> list[int]:
    return [operation(v) for v in values]

# Async callable
from collections.abc import Awaitable

AsyncHandler = Callable[[Request], Awaitable[Response]]
```

### TypedDict for Structured Dicts

```python
from typing import TypedDict, NotRequired

class UserData(TypedDict):
    id: int
    email: str
    name: str
    is_active: NotRequired[bool]  # Optional field

def process_user(data: UserData) -> None:
    print(data["email"])  # Type-safe access
```

### Protocol for Duck Typing

```python
from typing import Protocol

class Sendable(Protocol):
    """Protocol for objects that can be sent."""
    def send(self, message: str) -> bool:
        ...

class EmailClient:
    def send(self, message: str) -> bool:
        # Send email
        return True

class SMSClient:
    def send(self, message: str) -> bool:
        # Send SMS
        return True

def notify(client: Sendable, message: str) -> bool:
    """Works with any Sendable."""
    return client.send(message)
```

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

# Per-module configuration
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true
```

### Running mypy

```bash
# Check all code
mypy src/

# Check specific file
mypy src/services/users.py

# Check with specific options
mypy --strict src/

# Generate HTML report
mypy --html-report mypy-report src/
```

## Templates

**Type-safe function signature:**
```python
def process_user(
    user_id: int,
    action: str,
    *,
    force: bool = False,
    metadata: dict[str, Any] | None = None,
) -> tuple[User, bool]:
    ...
```

## Sources

- [Python typing Documentation](https://docs.python.org/3/library/typing.html) - Official typing module reference
- [mypy Documentation](https://mypy.readthedocs.io/) - Static type checker for Python
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/) - Type hints specification
- [PEP 604 - Union Syntax](https://peps.python.org/pep-0604/) - `X | Y` union syntax
- [typing best practices](https://typing.readthedocs.io/en/latest/source/guides/libraries.html) - Library typing guide

## Agent

Executed by: faion-code-agent
