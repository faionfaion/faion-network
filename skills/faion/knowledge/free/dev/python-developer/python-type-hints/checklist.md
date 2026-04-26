# Type Hints Checklist

Step-by-step guide for adding type hints to Python code.

## Pre-Flight Checklist

- [ ] **Determine Python version** - Check `python_requires` in pyproject.toml
- [ ] **Choose type checker** - mypy, pyright, or both
- [ ] **Install typing_extensions** if Python < 3.12
- [ ] **Configure type checker** in pyproject.toml

## Phase 1: Setup

### 1.1 Configure Type Checker

```toml
# pyproject.toml - mypy
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
check_untyped_defs = true
no_implicit_optional = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true
```

```toml
# pyproject.toml - pyright
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
reportMissingImports = true
reportMissingTypeStubs = false
```

### 1.2 Install Dependencies

```bash
# Type checking tools
pip install mypy pyright

# Framework stubs
pip install django-stubs  # Django
pip install types-requests  # requests
pip install types-redis  # redis

# Backports (if Python < 3.12)
pip install typing_extensions
```

### 1.3 Add to CI

```yaml
# .github/workflows/ci.yml
- name: Type check
  run: |
    pip install mypy
    mypy src/
```

## Phase 2: Function Signatures

### 2.1 Public Functions Checklist

For each public function:

- [ ] Add parameter types
- [ ] Add return type
- [ ] Handle `None` explicitly (`-> T | None`)
- [ ] Use `*` for keyword-only args
- [ ] Add `**kwargs` types if used

```python
# Before
def create_user(email, name, age=None, **kwargs):
    ...

# After
def create_user(
    email: str,
    name: str,
    *,
    age: int | None = None,
    **kwargs: Any,
) -> User:
    ...
```

### 2.2 Return Type Decisions

| Scenario | Return Type |
|----------|-------------|
| Always returns value | `-> T` |
| May return None | `-> T \| None` |
| Returns nothing | `-> None` |
| Never returns (raises) | `-> NoReturn` |
| Generator | `-> Iterator[T]` |
| Async generator | `-> AsyncIterator[T]` |
| Context manager | `-> ContextManager[T]` |

### 2.3 Common Function Patterns

- [ ] Factory functions return the created type
- [ ] `get_*` functions often return `T | None`
- [ ] `get_*_or_404` functions return `T` (raises on None)
- [ ] `list_*` functions return `list[T]`
- [ ] `find_*` functions return `T | None`
- [ ] Validators return `bool` or raise

## Phase 3: Class Attributes

### 3.1 Instance Attributes

- [ ] Declare all attributes in `__init__`
- [ ] Use class-level annotations for type hints
- [ ] Use `ClassVar` for class attributes

```python
class User:
    # Class attribute
    _registry: ClassVar[dict[int, "User"]] = {}

    # Instance attributes (annotated at class level)
    id: int
    email: str
    name: str | None
    created_at: datetime

    def __init__(self, id: int, email: str) -> None:
        self.id = id
        self.email = email
        self.name = None
        self.created_at = datetime.now()
```

### 3.2 Property Types

- [ ] Add return type to `@property`
- [ ] Add parameter type to setter

```python
@property
def full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"

@full_name.setter
def full_name(self, value: str) -> None:
    parts = value.split()
    self.first_name = parts[0]
    self.last_name = parts[-1]
```

## Phase 4: Collections and Generics

### 4.1 Collection Types Checklist

- [ ] Use `list[T]` not `List[T]`
- [ ] Use `dict[K, V]` not `Dict[K, V]`
- [ ] Use `set[T]` not `Set[T]`
- [ ] Use `tuple[T, ...]` for variable-length
- [ ] Use `tuple[T1, T2]` for fixed-length
- [ ] Use `Sequence[T]` for read-only list-like
- [ ] Use `Mapping[K, V]` for read-only dict-like
- [ ] Use `Iterable[T]` for any iterable

### 4.2 Generic Classes (Python 3.12+)

- [ ] Use new syntax `class Name[T]:` instead of `Generic[T]`
- [ ] Constrain with `class Name[T: BaseType]:`
- [ ] Use bounds for interface constraints

```python
# Python 3.12+ syntax
class Repository[T]:
    def get(self, id: int) -> T | None: ...
    def list(self) -> list[T]: ...
    def create(self, item: T) -> T: ...

# With constraint
class NumberProcessor[T: (int, float)]:
    def process(self, value: T) -> T: ...
```

## Phase 5: Complex Types

### 5.1 Callable Types

- [ ] Define callback signatures
- [ ] Use `ParamSpec` for decorators
- [ ] Use `Concatenate` for parameter modification

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

# Simple callback
Handler = Callable[[Request], Response]

# Decorator preserving signature
def logged[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### 5.2 TypedDict

- [ ] Use for JSON-like structures
- [ ] Mark optional fields with `NotRequired`
- [ ] Use `Required` in `total=False` dicts

```python
from typing import TypedDict, NotRequired, Required

class UserData(TypedDict):
    id: int
    email: str
    name: NotRequired[str]

class CreateUserData(TypedDict, total=False):
    email: Required[str]  # Required in optional dict
    name: str
    age: int
```

### 5.3 Protocol

- [ ] Use Protocol for duck typing
- [ ] Add `@runtime_checkable` if isinstance() needed
- [ ] Define only required methods

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

def cleanup(resource: Closeable) -> None:
    resource.close()
```

## Phase 6: Type Narrowing

### 6.1 Narrowing Techniques

- [ ] Use `isinstance()` for runtime checks
- [ ] Use `TypeIs` for custom narrowing (both branches)
- [ ] Use `TypeGuard` for one-way narrowing
- [ ] Use `assert_never()` for exhaustiveness

```python
from typing import TypeIs, assert_never

def is_str(x: object) -> TypeIs[str]:
    return isinstance(x, str)

def process(val: int | str | float) -> str:
    if isinstance(val, int):
        return f"int: {val}"
    elif isinstance(val, str):
        return f"str: {val}"
    elif isinstance(val, float):
        return f"float: {val}"
    else:
        assert_never(val)  # Ensures exhaustive matching
```

### 6.2 None Handling

- [ ] Use early returns for None checks
- [ ] Use `assert` for type checker hints
- [ ] Create `assert_not_none` helper

```python
def assert_not_none[T](value: T | None, message: str = "") -> T:
    if value is None:
        raise ValueError(message or "Value cannot be None")
    return value

# Usage
user = get_user(id)
verified = assert_not_none(user, f"User {id} not found")
```

## Phase 7: Framework-Specific

### 7.1 Django Checklist

- [ ] Install `django-stubs`
- [ ] Configure mypy plugin
- [ ] Type model fields
- [ ] Type QuerySet returns
- [ ] Type view parameters

```toml
# pyproject.toml
[tool.mypy]
plugins = ["mypy_django_plugin.main"]

[tool.django-stubs]
django_settings_module = "myproject.settings"
```

### 7.2 FastAPI/Pydantic Checklist

- [ ] Use Pydantic models for request/response
- [ ] Use `Annotated` for dependencies
- [ ] Type path/query parameters

```python
from typing import Annotated
from fastapi import Depends, Path

@app.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    ...
```

## Phase 8: Review and Cleanup

### 8.1 Final Review Checklist

- [ ] Run `mypy --strict` on codebase
- [ ] Fix all errors (don't use `# type: ignore` liberally)
- [ ] Review `Any` usage (minimize)
- [ ] Check for missing `| None` on nullable returns
- [ ] Verify generic constraints are appropriate
- [ ] Run `pyupgrade` to modernize syntax

### 8.2 Common Mistakes to Check

- [ ] No `Any` for "I don't know" types
- [ ] No `# type: ignore` without reason
- [ ] No missing return types
- [ ] No implicit `None` returns
- [ ] No `list` without element type
- [ ] No `dict` without key/value types

### 8.3 Maintenance

- [ ] Add type checking to CI
- [ ] Configure pre-commit hooks
- [ ] Document type conventions in README
- [ ] Update types when refactoring

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.8.0
  hooks:
    - id: mypy
      additional_dependencies:
        - django-stubs
```

## Quick Decision Tree

```
Need to type this:
├── Function parameter?
│   ├── Required → `param: Type`
│   ├── Optional with default → `param: Type = default`
│   └── May be None → `param: Type | None`
├── Return value?
│   ├── Always returns → `-> Type`
│   ├── May be None → `-> Type | None`
│   ├── No return → `-> None`
│   └── Never returns → `-> NoReturn`
├── Collection?
│   ├── List → `list[ElementType]`
│   ├── Dict → `dict[KeyType, ValueType]`
│   ├── Read-only list → `Sequence[ElementType]`
│   └── Any iterable → `Iterable[ElementType]`
├── Callback?
│   ├── Simple → `Callable[[Args], Return]`
│   └── Decorator → `ParamSpec + TypeVar`
├── Dict with known keys?
│   └── Use `TypedDict`
└── Duck typing interface?
    └── Use `Protocol`
```
