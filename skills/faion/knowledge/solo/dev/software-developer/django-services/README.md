---
id: django-services
name: "Django Services Architecture"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Django Services Architecture

## Decision Tree

```
What does the function do?
│
├─► Changes DB (CREATE/UPDATE/DELETE)?
│   └─► services/
├─► Makes external API calls (POST/PUT/DELETE)?
│   └─► services/ (or integrations/)
├─► Pure function (validation, calculations)?
│   └─► utils/
└─► Data transformation?
    └─► utils/
```

## Services = Functions (preferred)

```python
# services/item_activation.py
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.inventory.models import Item
    from apps.users.models import User, Admin

def activate_user_item(
    user: User,
    item_code: str,
    *,
    activated_by: Admin,
) -> Item:
    """
    Activate item for user.

    Business logic:
    - Validates item availability
    - Associates item with user
    - Creates audit log entry
    """
    from apps.inventory.models import Item

    item = Item.objects.get(code=item_code)
    item.user = user
    item.is_active = True
    item.save(update_fields=['user', 'is_active', 'updated_at'])
    return item
```

## Service Classes (for complex operations)

Only when you need dependency injection or complex state:

```python
class OrderProcessingService:
    def __init__(self, payment_gateway: PaymentGateway):
        self.payment_gateway = payment_gateway

    def process(self, order: Order) -> ProcessingResult:
        ...
```

## Function Parameters Formatting

Multi-line for 3+ parameters:

```python
# CORRECT - each parameter on separate line
def create_order(
    user: User,
    amount: Decimal,
    order_type: str,
    *,
    item: Item | None = None,
    notify: bool = True,
) -> Order:
    ...

# Use keyword-only args (*) for optional parameters
def send_notification(
    user: User,
    message: str,
    *,  # Everything after is keyword-only
    priority: str = 'normal',
    channel: str = 'email',
) -> bool:
    ...
```

## Docstrings (Google Style)

```python
def create_order(user: User, amount: Decimal) -> Order:
    """
    Create order for user.

    Business logic:
    - Validates user limits
    - Creates Transaction and Order records
    - Sends confirmation notification

    Args:
        user: User placing the order.
        amount: Order amount in base currency.

    Returns:
        Created Order instance.

    Raises:
        LimitExceededError: If daily limit exceeded.
    """
    ...
```


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Sources

- [Django Service Layer Pattern](https://www.dabapps.com/insights/django-models-and-encapsulation/) - Service layer architecture
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) - Django best practices book
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) - Docstring conventions
- [PEP 3102 - Keyword-Only Arguments](https://peps.python.org/pep-3102/) - Function parameter patterns
- [Type Checking Django](https://adamj.eu/tech/2021/05/09/how-to-type-check-django/) - Django type hints
