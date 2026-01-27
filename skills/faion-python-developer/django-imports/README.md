# Django Import Patterns

Comprehensive guide to organizing imports in Django projects for maintainable, conflict-free codebases.

## Overview

| Aspect | Best Practice |
|--------|---------------|
| Sorting | Ruff or isort with Django profile |
| Cross-app | Always use aliases |
| Local | Single-dot relative imports |
| Type hints | `TYPE_CHECKING` guard |
| Circular deps | `apps.get_model()` or strings |

## Why Import Organization Matters

1. **Readability** - Consistent ordering makes imports scannable
2. **Conflict prevention** - Aliases prevent naming collisions between apps
3. **Circular import avoidance** - Proper patterns prevent runtime errors
4. **Type checking** - Clean separation of runtime vs type-only imports
5. **Maintainability** - Automated sorting reduces merge conflicts

## Import Order (PEP 8 + Django Style)

```
1. __future__ imports
2. Standard library
3. Third-party packages (Django, DRF, Celery)
4. Other Django components (cross-app)
5. Local application imports (relative)
```

### Django-Specific Rules

| Rule | Example |
|------|---------|
| Absolute for Django core | `from django.db import models` |
| Absolute for cross-app | `from apps.users import models as user_models` |
| Single-dot relative for local | `from .models import User` |
| Avoid multi-dot relative | Never `from ...users.models import User` |

## Key Patterns

### Cross-App Imports with Aliases

```python
# Cross-app imports - ALWAYS with alias
from apps.orders import models as order_models
from apps.users import models as user_models
from apps.catalog import services as catalog_services
```

**Why aliases?**
- Prevents `User` vs `User` conflicts
- Makes origin explicit: `user_models.User`
- Enables IDE auto-import without conflicts

### TYPE_CHECKING for Type Hints

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.users.models import User
    from apps.orders.models import Order

def process_order(user: User, order: Order) -> bool:
    # Type hints work, no runtime import
    ...
```

### Lazy Imports with `apps.get_model()`

```python
from django.apps import apps

def get_user_orders(user_id: int):
    Order = apps.get_model('orders', 'Order')
    return Order.objects.filter(user_id=user_id)
```

### String References in Models

```python
class Order(models.Model):
    # String reference - no import needed
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    # String for ManyToMany
    products = models.ManyToManyField('catalog.Product')
```

## Circular Import Prevention

| Strategy | When to Use |
|----------|-------------|
| `TYPE_CHECKING` | Type hints only |
| `apps.get_model()` | Runtime model access |
| String references | ForeignKey, ManyToMany |
| Local imports | Function-scoped needs |
| Signals | Cross-app side effects |

## Python 3.10+ Type Hints

```python
from __future__ import annotations

# No typing imports needed for generics
def get_items(user_id: int) -> list[Item]:
    ...

def find_item(code: str) -> Item | None:
    ...
```

## Files in This Folder

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step imports organization |
| [examples.md](examples.md) | Real patterns and anti-patterns |
| [templates.md](templates.md) | Copy-paste configurations |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted organization |

## LLM Usage Tips

### When to Apply This Methodology

- Setting up new Django project
- Refactoring existing imports
- Resolving circular import errors
- Adding type hints to legacy code
- Configuring Ruff/isort

### Key Instructions for LLMs

1. **Always use aliases for cross-app imports** - prevents naming conflicts
2. **Use `TYPE_CHECKING` for type-only imports** - zero runtime cost
3. **Prefer `apps.get_model()` over direct imports** - prevents circular deps
4. **Use string references in model fields** - Django resolves at runtime
5. **Configure Ruff with Django section** - proper import ordering

### Common LLM Mistakes

| Mistake | Correct Approach |
|---------|------------------|
| Direct cross-app imports | Use aliases: `import models as user_models` |
| Importing unused types | Wrap in `TYPE_CHECKING` |
| Multi-dot relative imports | Use absolute or single-dot |
| `from app.models import *` | Never use star imports |

## Python 3.14+ Lazy Imports (PEP 810)

Python 3.14+ introduces explicit lazy imports for improved startup performance:

```python
# Future syntax (Python 3.14+)
lazy from heavy_analytics import ReportGenerator

def generate_report():
    # ReportGenerator module loaded only when first accessed
    return ReportGenerator().run()
```

**Performance benefits:**
- 2-3x faster startup time in CLI tools
- Reduced memory usage at initialization
- No more need for `if TYPE_CHECKING:` patterns for performance

**Current alternative (Python 3.9-3.13):**
```python
def generate_report():
    from heavy_analytics import ReportGenerator  # Lazy at function level
    return ReportGenerator().run()
```

## External References

### Official Documentation
- [PEP 8 - Import Style](https://peps.python.org/pep-0008/#imports)
- [PEP 328 - Absolute/Relative Imports](https://peps.python.org/pep-0328/)
- [Django Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- [PEP 563 - Postponed Annotations](https://peps.python.org/pep-0563/)
- [PEP 690 - Lazy Imports](https://peps.python.org/pep-0690/) - Proposal
- [PEP 810 - Explicit Lazy Imports](https://peps.python.org/pep-0810/) - Accepted for Python 3.14+

### Tools
- [Ruff Settings](https://docs.astral.sh/ruff/settings/)
- [Ruff Configuration](https://docs.astral.sh/ruff/configuration/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [isort Configuration Options](https://pycqa.github.io/isort/docs/configuration/options.html)
- [django-stubs](https://github.com/typeddjango/django-stubs) - Type stubs for Django
- [lazy-imports PyPI](https://pypi.org/project/lazy-imports/) - Lazy import utilities

### Tutorials & Articles
- [Django Best Practices: Imports](https://learndjango.com/tutorials/django-best-practices-imports)
- [Absolute vs Relative Imports](https://realpython.com/absolute-vs-relative-python-imports/)
- [Circular Import Trap in Python](https://medium.com/@denis.volokh/the-circular-import-trap-in-python-and-how-to-escape-it-9fb22925dab6)
- [Avoiding Circular Imports in Django](https://forum.djangoproject.com/t/best-practices-for-avoiding-circular-imports-and-maintaining-app-independence-in-django/37946)
- [Fixing Circular Imports](https://www.pythonmorsels.com/fixing-circular-imports/) - Python Morsels
- [Lazy Imports Performance](https://hugovk.dev/blog/2025/lazy-imports/) - 3x faster startup
- [Lazy Imports in Python](https://www.geeksforgeeks.org/python/lazy-import-in-python/)
- [Sorting Imports with Ruff](https://pydevtools.com/handbook/how-to/how-to-sort-python-imports-with-ruff/)
- [Pre-commit with Django](https://learndjango.com/tutorials/pre-commit-django)
- [Organize Django Imports with isort](https://medium.com/django-unleashed/organize-your-django-imports-like-a-pro-with-isort-95b3a3b4b513)

---

**Related:** [django-coding-standards](../django-coding-standards/) | [python-type-hints](../python-type-hints/) | [python-code-quality](../python-code-quality/)
