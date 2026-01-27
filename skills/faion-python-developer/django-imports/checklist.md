# Django Import Organization Checklist

Step-by-step guide for organizing imports in Django projects.

## Project Setup Checklist

### 1. Install and Configure Linting Tools

- [ ] Install Ruff: `pip install ruff` or `uv add ruff --dev`
- [ ] Create `pyproject.toml` with import sorting config
- [ ] Configure Django-specific import sections
- [ ] Add pre-commit hooks for auto-formatting
- [ ] Configure IDE to use Ruff for import sorting

### 2. Establish Import Order Convention

Standard order for all project files:

```
1. [ ] __future__ imports (always first)
2. [ ] Standard library (os, sys, datetime, etc.)
3. [ ] Third-party packages (django, rest_framework, celery)
4. [ ] Django components from other apps (with aliases)
5. [ ] Local imports (relative with single dot)
```

### 3. Configure Type Checking

- [ ] Add `from __future__ import annotations` to all files
- [ ] Create `TYPE_CHECKING` blocks for type-only imports
- [ ] Install `django-stubs` for Django type hints
- [ ] Configure mypy or pyright

## File-Level Checklist

### For Each Python File

#### Import Section Structure

- [ ] `__future__` imports at top
- [ ] Blank line after future imports
- [ ] Standard library imports grouped
- [ ] Blank line after standard library
- [ ] Third-party imports grouped
- [ ] Blank line after third-party
- [ ] Cross-app imports with aliases
- [ ] Blank line after cross-app
- [ ] Local relative imports

#### Import Style

- [ ] No star imports (`from x import *`)
- [ ] No multi-dot relative imports (`from ...models`)
- [ ] Cross-app imports use aliases
- [ ] Local imports use single-dot relative
- [ ] Imports sorted alphabetically within groups
- [ ] `import X` before `from X import Y` in each group

#### Type Hints

- [ ] Type-only imports in `TYPE_CHECKING` block
- [ ] Using `annotations` future import
- [ ] String annotations for forward references

## Cross-App Import Checklist

### When Importing from Another App

- [ ] Use alias pattern: `from apps.users import models as user_models`
- [ ] Access via alias: `user_models.User`, not just `User`
- [ ] Document why cross-app import is needed (if not obvious)

### When Importing Models

- [ ] For ForeignKey: prefer string reference `'users.User'`
- [ ] For runtime access: prefer `apps.get_model('users', 'User')`
- [ ] For type hints: use `TYPE_CHECKING` block

### Alias Conventions

| Module Type | Alias Pattern | Example |
|-------------|---------------|---------|
| models | `{app}_models` | `user_models` |
| services | `{app}_services` | `order_services` |
| serializers | `{app}_serializers` | `catalog_serializers` |
| constants | `{app}_constants` | `payment_constants` |
| utils | `{app}_utils` | `notification_utils` |

## Circular Import Prevention Checklist

### Before Adding Import

- [ ] Check if import creates circular dependency
- [ ] Consider if `TYPE_CHECKING` is sufficient
- [ ] Consider if `apps.get_model()` works better
- [ ] Consider if string reference works (for model fields)

### Signs of Circular Import Issues

- [ ] `ImportError: cannot import name 'X' from partially initialized module`
- [ ] `AttributeError: module has no attribute 'X'`
- [ ] Import works in some files but not others
- [ ] Order of imports affects behavior

### Resolution Strategies

1. **TYPE_CHECKING** - For type hints only
   - [ ] Move import inside `if TYPE_CHECKING:` block
   - [ ] Use string annotation if needed

2. **Local Import** - For function-scoped needs
   - [ ] Move import inside function
   - [ ] Add comment explaining why

3. **apps.get_model()** - For dynamic model access
   - [ ] Replace direct import with `apps.get_model()`
   - [ ] Handle potential `LookupError`

4. **String References** - For model fields
   - [ ] Use `'app.Model'` string format
   - [ ] Works for ForeignKey, ManyToMany, OneToOne

5. **Architecture Refactor** - For structural issues
   - [ ] Move shared code to separate module
   - [ ] Use signals for cross-app communication
   - [ ] Create interface/protocol module

## Ruff Configuration Checklist

### Basic Setup

- [ ] Enable `I` rules (isort)
- [ ] Set `target-version` to match project
- [ ] Configure `src` paths for first-party detection
- [ ] Set `known-first-party` packages

### Django-Specific

- [ ] Create `django` section in isort config
- [ ] Add `django`, `rest_framework` to django section
- [ ] Order: future, stdlib, third-party, django, first-party, local

### Pre-commit

- [ ] Add ruff to `.pre-commit-config.yaml`
- [ ] Enable both `ruff check` and `ruff format`
- [ ] Configure fix mode for imports

## Code Review Checklist

### Import Review Points

- [ ] No star imports
- [ ] Cross-app imports use aliases
- [ ] No direct model imports across apps (without alias)
- [ ] Type-only imports in TYPE_CHECKING
- [ ] Import order follows convention
- [ ] No multi-dot relative imports
- [ ] No unused imports

### Anti-Patterns to Flag

| Anti-Pattern | Issue | Fix |
|--------------|-------|-----|
| `from apps.users.models import User` | Naming conflict risk | Use alias |
| `from ...models import X` | Hard to track | Use absolute |
| `from app import *` | Namespace pollution | Explicit imports |
| Imports inside class body | Performance | Move to top |
| Circular import hack | Technical debt | Refactor |

## Migration Checklist

### Migrating Existing Project

1. **Audit Phase**
   - [ ] Run Ruff to identify import issues
   - [ ] List all circular import workarounds
   - [ ] Document current import patterns

2. **Configuration Phase**
   - [ ] Set up `pyproject.toml` with Ruff config
   - [ ] Configure pre-commit hooks
   - [ ] Set up CI check for imports

3. **Migration Phase**
   - [ ] Run `ruff check --fix` to auto-fix sorting
   - [ ] Convert direct cross-app imports to aliases
   - [ ] Add TYPE_CHECKING blocks for type hints
   - [ ] Review and merge incrementally

4. **Validation Phase**
   - [ ] Run full test suite
   - [ ] Check for import errors at startup
   - [ ] Verify type checking still works
   - [ ] Update documentation

## Validation Commands

### Ruff Commands

```bash
# Check all import issues
ruff check --select I .

# Auto-fix import sorting
ruff check --select I --fix .

# Check Django-specific rules
ruff check --select DJ .

# Full check with auto-fix
ruff check --fix .

# Format code
ruff format .

# Check specific file
ruff check --select I apps/orders/views.py
```

### isort Commands (if not using Ruff)

```bash
# Check imports
isort --check-only .

# Fix imports
isort .

# Show diff
isort --diff .

# Check specific file
isort --check-only apps/orders/views.py
```

### Verification Steps

```bash
# 1. Check imports
ruff check --select I .

# 2. Run tests to catch import errors
pytest --collect-only  # Fast check for import issues

# 3. Check type hints
mypy apps/ --ignore-missing-imports

# 4. Start Django to verify no import errors
python manage.py check
```

## Quick Reference

### Import Statement Patterns

```python
# Good
from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import models
from apps.users import models as user_models
from .models import Order

# Bad
from apps.users.models import User  # No alias
from ...users.models import User    # Multi-dot
from apps.users.models import *     # Star import
```

### Type Hint Patterns

```python
# Good - TYPE_CHECKING guard
if TYPE_CHECKING:
    from apps.users.models import User

def process(user: User) -> None: ...

# Good - String annotation
def process(user: "User") -> None: ...

# Bad - Runtime import for types only
from apps.users.models import User  # If only used in hints
```

### Model Reference Patterns

```python
# Good - String reference
user = models.ForeignKey('users.User', on_delete=models.CASCADE)

# Good - apps.get_model
User = apps.get_model('users', 'User')

# Bad - Direct import (circular risk)
from apps.users.models import User
user = models.ForeignKey(User, on_delete=models.CASCADE)
```

---

**Next:** [examples.md](examples.md) - Real import patterns and anti-patterns
