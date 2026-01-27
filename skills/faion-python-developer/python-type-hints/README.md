# Python Type Hints

## Overview

Type hints enable static type checking, better IDE support, and self-documenting code. Modern Python (3.12+) introduces significant typing improvements including new type parameter syntax (PEP 695), `TypeIs` for bidirectional narrowing (PEP 742), and default values for TypeVar (Python 3.13).

**Target:** Python 3.12+ (with typing_extensions for older versions)

## Why Type Hints Matter

| Benefit | Description |
|---------|-------------|
| **Static Analysis** | Catch type errors before runtime with mypy/pyright |
| **IDE Support** | Better autocompletion, refactoring, navigation |
| **Documentation** | Self-documenting function signatures |
| **LLM Enhancement** | Type hints dramatically improve AI code generation accuracy |
| **Maintainability** | Easier refactoring and onboarding |

## Python Version Features

| Version | Key Typing Features |
|---------|---------------------|
| 3.9 | `list[int]`, `dict[str, int]` (no imports needed) |
| 3.10 | `X \| Y` union syntax, `ParamSpec`, `TypeAlias` |
| 3.11 | `Self`, `LiteralString`, `TypeVarTuple`, `Required`/`NotRequired` |
| 3.12 | PEP 695 type parameter syntax (`class Box[T]:`, `def first[T]():`) |
| 3.13 | `TypeIs` (PEP 742), TypeVar defaults, `@deprecated` |
| 3.14 | PEP 649 lazy annotations, tighter dataclass integration |

## Core Concepts

### 1. Basic Types

```python
# Primitives
name: str = "John"
age: int = 30
active: bool = True
score: float = 95.5

# Collections (Python 3.9+)
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95}
unique: set[int] = {1, 2, 3}
point: tuple[float, float] = (10.5, 20.3)
```

### 2. Union and Optional

```python
# Python 3.10+ - use | for union
def get_user(id: int) -> User | None:
    return User.objects.filter(id=id).first()

def process(value: int | str) -> str:
    return str(value)
```

### 3. Generic Types (Python 3.12+)

```python
# New syntax - no TypeVar import needed
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)
```

### 4. TypeIs vs TypeGuard

```python
from typing import TypeIs, TypeGuard

# TypeIs (Python 3.13) - bidirectional narrowing
def is_str(x: object) -> TypeIs[str]:
    return isinstance(x, str)

def process(x: int | str) -> None:
    if is_str(x):
        print(x.upper())  # x is str
    else:
        print(x + 1)  # x is int (narrowed!)

# TypeGuard - only narrows in if branch
def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)
```

### 5. Protocol (Structural Subtyping)

```python
from typing import Protocol

class Sendable(Protocol):
    def send(self, message: str) -> bool: ...

# No inheritance needed - structural matching
class EmailClient:
    def send(self, message: str) -> bool:
        return True

def notify(client: Sendable, msg: str) -> bool:
    return client.send(msg)

notify(EmailClient(), "Hello")  # Works!
```

## Type Checker Comparison

| Feature | mypy | pyright |
|---------|------|---------|
| **Speed** | Slower | 3-5x faster |
| **IDE Integration** | Good | Excellent (VSCode/Pylance) |
| **Plugin Support** | Yes | No |
| **Default Strictness** | Lenient | Stricter |
| **Unannotated Code** | Skips by default | Checks everything |
| **Django Support** | django-stubs | django-stubs |
| **Language** | Python | TypeScript |

**Recommendation:** Use Pylance (pyright) for development, mypy in CI for comprehensive checking.

## LLM Usage Tips

### For Better Code Generation

1. **Always provide type hints in prompts** - LLMs generate more accurate code when types are specified
2. **Include Protocol definitions** - Helps LLM understand expected interfaces
3. **Specify Python version** - "Using Python 3.12+ type hints" triggers modern syntax
4. **Show TypedDict structures** - For complex JSON/dict shapes

### When Asking LLM to Add Types

```
Add type hints to this code:
- Use Python 3.12+ syntax (list[int] not List[int])
- Use | for unions (str | None not Optional[str])
- Define TypedDict for dict structures
- Use Protocol for duck typing interfaces
- Add return types to all functions
```

### When Reviewing LLM Output

Check for:
- `Any` overuse (should be specific types)
- Missing `| None` on nullable returns
- Generic types properly constrained
- Protocols used instead of ABC when appropriate

## Quick Reference

| Need | Use |
|------|-----|
| Optional value | `T \| None` |
| Multiple types | `int \| str \| float` |
| Callback function | `Callable[[ArgTypes], ReturnType]` |
| Decorator params | `ParamSpec` |
| Generic class | `class Box[T]:` (3.12+) |
| Generic function | `def first[T](items: list[T]) -> T:` (3.12+) |
| Structural typing | `Protocol` |
| Dict with known keys | `TypedDict` |
| Narrowing if/else | `TypeIs[T]` |
| Narrowing if only | `TypeGuard[T]` |
| Exhaustive matching | `assert_never()` |
| Immutable value | `Final[T]` |
| Literal values | `Literal["a", "b"]` |
| Type + metadata | `Annotated[T, metadata]` |

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step type annotation checklist |
| [examples.md](examples.md) | Real-world typing examples |
| [templates.md](templates.md) | Copy-paste type patterns |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted typing |

## External Resources

### Official Documentation
- [Python typing Documentation](https://docs.python.org/3/library/typing.html)
- [typing.python.org](https://typing.python.org/) - Typing reference documentation
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pyright Documentation](https://github.com/microsoft/pyright)

### PEPs
- [PEP 484](https://peps.python.org/pep-0484/) - Type Hints (original)
- [PEP 544](https://peps.python.org/pep-0544/) - Protocols
- [PEP 604](https://peps.python.org/pep-0604/) - Union syntax `X | Y`
- [PEP 612](https://peps.python.org/pep-0612/) - ParamSpec
- [PEP 695](https://peps.python.org/pep-0695/) - Type Parameter Syntax (3.12)
- [PEP 742](https://peps.python.org/pep-0742/) - TypeIs (3.13)
- [PEP 649](https://peps.python.org/pep-0649/) - Lazy Annotations (3.14)

### Framework-Specific
- [django-stubs](https://github.com/typeddjango/django-stubs) - Django type stubs
- [FastAPI Types](https://fastapi.tiangolo.com/python-types/) - FastAPI typing guide
- [Pydantic Types](https://docs.pydantic.dev/latest/concepts/types/) - Pydantic typing

### Tools
- [typing_extensions](https://pypi.org/project/typing-extensions/) - Backports for older Python
- [pyupgrade](https://github.com/asottile/pyupgrade) - Auto-upgrade type hint syntax
- [ruff](https://github.com/astral-sh/ruff) - Fast linter with type checking rules
