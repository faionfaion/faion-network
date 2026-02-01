---
id: django-imports
name: "Django Import Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Django Import Patterns

## Cross-app Imports - ALWAYS with alias

```python
# Standard library
from datetime import datetime, timedelta
from decimal import Decimal

# Third-party
from django.db import models
from rest_framework import serializers

# Cross-app imports - ALWAYS with alias
from apps.orders import models as order_models
from apps.users import models as user_models
from apps.catalog import models as catalog_models

# Services
from apps.users import services as user_services

# Constants
from apps.orders import constants as order_constants

# Own modules (relative imports)
from .models import User
from . import constants
```

## Avoid

```python
# Direct imports can cause naming conflicts
from apps.users.models import User       # Avoid
from apps.orders.models import Order     # Avoid
from apps.users.models import *          # NEVER!
```

## Import Order (PEP 8 + isort)

1. `__future__` imports
2. Standard library
3. Third-party packages (Django, DRF, etc.)
4. Local application imports

## Type Hints

### Python 3.9+ (using typing module)

```python
from typing import Optional, List, Dict, Union

def get_items(user: User) -> List[Item]:
    return Item.objects.filter(user=user)

def process_order(
    handler: OrderHandler,
    item_code: str,
    *,
    category: Optional[Category] = None,
) -> Optional[Order]:
    ...
```

### Python 3.10+ (modern syntax)

```python
# Union type with | operator
def get_item(uid: str) -> Item | None:
    ...

# Built-in generics (no import needed)
def get_items(user: User) -> list[Item]:
    ...
```

### Best Practice - Support multiple Python versions

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.users.models import User

def get_user_balance(user: User) -> Decimal:
    """Works in Python 3.9+ with __future__ annotations."""
    ...
```


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Sources

- [PEP 8 - Import Style](https://peps.python.org/pep-0008/#imports) - Python import conventions
- [isort Documentation](https://pycqa.github.io/isort/) - Automatic import sorting
- [PEP 563 - Postponed Annotations](https://peps.python.org/pep-0563/) - `__future__` annotations
- [Django Import Patterns](https://docs.djangoproject.com/en/stable/misc/design-philosophies/#don-t-repeat-yourself-dry) - DRY principle
- [Type Checking Best Practices](https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-avoid-circular-imports/) - Avoiding circular imports
