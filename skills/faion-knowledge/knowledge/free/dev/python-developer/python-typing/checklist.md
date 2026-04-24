# Python Typing Checklist

Step-by-step guide for adding type hints to Python code.

---

## Pre-Flight Checklist

- [ ] **Determine Python version** - Features vary significantly (3.9 vs 3.10 vs 3.12)
- [ ] **Choose type checker** - mypy (strict) or Pyright (fast) or both
- [ ] **Install stubs** - `django-stubs`, `types-requests`, etc.
- [ ] **Configure type checker** - Set up `pyproject.toml`
- [ ] **Decide strictness level** - Gradual vs strict from start

---

## New Project Setup

### 1. Configure Type Checker

- [ ] Add mypy/pyright configuration to `pyproject.toml`
- [ ] Set Python version
- [ ] Enable strict mode (recommended for new projects)
- [ ] Configure module overrides for tests/migrations

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### 2. Install Required Packages

- [ ] `pip install mypy` or `pip install pyright`
- [ ] Framework stubs: `pip install django-stubs` (if Django)
- [ ] Utility stubs: `pip install types-requests types-redis`

### 3. Set Up CI/CD

- [ ] Add type checking to pre-commit hooks
- [ ] Add type checking to CI pipeline
- [ ] Consider running both mypy and Pyright

---

## Function Typing Checklist

### Basic Function

- [ ] Add parameter types
- [ ] Add return type
- [ ] Handle `None` returns explicitly
- [ ] Type `*args` and `**kwargs` if used

```python
# Before
def process(data, flag=False):
    if flag:
        return data.upper()
    return None

# After
def process(data: str, flag: bool = False) -> str | None:
    if flag:
        return data.upper()
    return None
```

### Complex Function

- [ ] Use `TypeVar` for generic behavior
- [ ] Use `ParamSpec` for decorators
- [ ] Use `overload` for multiple signatures
- [ ] Document type constraints

---

## Class Typing Checklist

### Basic Class

- [ ] Type all instance attributes in `__init__`
- [ ] Type class variables with `ClassVar`
- [ ] Type all method parameters and returns
- [ ] Consider using `@dataclass` for data containers

```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool = True

    _cache: ClassVar[dict[int, "User"]] = {}
```

### Generic Class

- [ ] Use Python 3.12+ syntax: `class Container[T]:`
- [ ] Add bounds if needed: `class NumericContainer[T: (int, float)]:`
- [ ] Consider variance (covariant/contravariant)

---

## Dict/Data Structure Typing

### When to Use What

| Use Case | Type |
|----------|------|
| Known fixed keys | `TypedDict` |
| Unknown keys, same value type | `dict[str, ValueType]` |
| Data validation needed | Pydantic `BaseModel` |
| Immutable data | `@dataclass(frozen=True)` |
| Performance critical | `NamedTuple` |

### TypedDict Checklist

- [ ] Define all required keys
- [ ] Mark optional keys with `NotRequired`
- [ ] Use `total=False` if most keys are optional
- [ ] Consider inheritance for key reuse
- [ ] Use `ReadOnly` for immutable fields (Python 3.13+)

```python
from typing import TypedDict, NotRequired, Required

class APIResponse(TypedDict):
    status: int
    data: dict[str, Any]
    error: NotRequired[str]
    meta: NotRequired[dict[str, Any]]
```

---

## Protocol Typing Checklist

### When to Use Protocol

- [ ] Need duck typing with type safety
- [ ] Working with third-party code you can't modify
- [ ] Want structural subtyping (vs inheritance)
- [ ] Defining callback/handler interfaces

### Protocol Definition

- [ ] Define only the methods/attributes you need
- [ ] Keep protocols small and focused
- [ ] Use `@runtime_checkable` only if needed for `isinstance()`
- [ ] Use properties for read-only attributes

```python
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict[str, Any]: ...

class JSONSerializable(Protocol):
    def to_json(self) -> str: ...
```

---

## Callable/Decorator Typing

### Basic Callable

- [ ] Define input types: `Callable[[int, str], bool]`
- [ ] Handle async: `Callable[[Request], Awaitable[Response]]`
- [ ] Use Protocol for complex signatures

### Decorator Typing

- [ ] Use `ParamSpec` to preserve signatures
- [ ] Use `Concatenate` when adding/removing args
- [ ] Use `@wraps` from functools
- [ ] Test with type checker

```python
from typing import ParamSpec, TypeVar
from functools import wraps

P = ParamSpec('P')
T = TypeVar('T')

def logged(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

---

## Framework-Specific Checklists

### Django

- [ ] Install `django-stubs`
- [ ] Configure mypy plugin in `pyproject.toml`
- [ ] Type views with `HttpRequest` -> `HttpResponse`
- [ ] Use `QuerySet[Model]` for query results
- [ ] Type model methods
- [ ] Consider `AuthenticatedHttpRequest` for authenticated views

### FastAPI

- [ ] Use Pydantic models for request/response
- [ ] Use `Annotated` for parameter metadata
- [ ] Type path/query parameters
- [ ] Define response models explicitly
- [ ] Use `Field()` for validation rules

### pytest

- [ ] Type fixtures with return types
- [ ] Use `pytest.fixture` decorator properly
- [ ] Consider less strict typing for test files

---

## Migration Checklist (Legacy Code)

### Phase 1: Setup

- [ ] Add type checker configuration
- [ ] Run type checker to see current errors
- [ ] Create baseline (ignore existing errors initially)

### Phase 2: Gradual Adoption

- [ ] Type new code (enforce in CI)
- [ ] Type public APIs first
- [ ] Type core business logic next
- [ ] Fix errors when touching existing code
- [ ] Use `# type: ignore` sparingly (with comment)

### Phase 3: Strictness

- [ ] Gradually enable stricter settings
- [ ] Remove `# type: ignore` comments
- [ ] Add missing stubs or contribute to typeshed

---

## Code Review Typing Checklist

### Completeness

- [ ] All public functions have type hints
- [ ] All class methods have type hints
- [ ] Return types are explicit (not inferred)
- [ ] `None` returns are handled

### Correctness

- [ ] Types match actual runtime behavior
- [ ] No overly broad types (`Any`, `object`) without reason
- [ ] Generic types are properly constrained
- [ ] Optional fields are marked correctly

### Best Practices

- [ ] Using modern syntax for Python version
- [ ] No unnecessary imports from `typing` (use built-ins)
- [ ] Protocols used instead of ABCs where appropriate
- [ ] TypedDict used for dict structures

---

## Quick Reference: Modern Syntax

| Old (Pre-3.9/3.10) | New (3.9+/3.10+) |
|-------------------|------------------|
| `List[int]` | `list[int]` |
| `Dict[str, int]` | `dict[str, int]` |
| `Tuple[int, str]` | `tuple[int, str]` |
| `Optional[str]` | `str \| None` |
| `Union[int, str]` | `int \| str` |
| `Type[User]` | `type[User]` |

| Old (Pre-3.12) | New (3.12+) |
|----------------|-------------|
| `T = TypeVar('T')` | `def func[T](x: T):` |
| `class Foo(Generic[T])` | `class Foo[T]:` |
| `TypeAlias = list[int]` | `type Alias = list[int]` |

---

## Verification Checklist

- [ ] Type checker passes (`mypy .` or `pyright`)
- [ ] No `# type: ignore` without explanatory comment
- [ ] IDE shows correct types on hover
- [ ] Autocomplete works correctly
- [ ] Refactoring tools work properly

---

*Use this checklist when adding types to new or existing Python code.*
