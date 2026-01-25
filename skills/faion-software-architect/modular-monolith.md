# Modular Monolith

Best of both worlds: monolith simplicity with microservices boundaries.

## What is a Modular Monolith?

Single deployable unit with **strict module boundaries**.

```
┌─────────────────────────────────────────┐
│              MODULAR MONOLITH           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │ Users   │  │ Orders  │  │Payments │  │
│  │ Module  │  │ Module  │  │ Module  │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  │
│       │            │            │       │
│  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐  │
│  │ Schema  │  │ Schema  │  │ Schema  │  │
│  └─────────┘  └─────────┘  └─────────┘  │
│       └────────────┼────────────┘       │
│                    │                    │
│              ┌─────┴─────┐              │
│              │ Database  │              │
│              └───────────┘              │
└─────────────────────────────────────────┘
           Single deployment
```

## Key Characteristics

| Aspect | Modular Monolith |
|--------|------------------|
| Deployment | Single unit |
| Communication | In-process (method calls) |
| Data | Separate schemas, same DB |
| Boundaries | Strict, enforced |
| Extraction | Easy to split later |

## When to Choose

- Starting new project with growth expectations
- Microservices is overkill but need boundaries
- Want option to extract services later
- Limited DevOps maturity
- Team learning DDD

## Module Rules

### 1. Public API Only
Modules communicate through defined interfaces.

```python
# ❌ WRONG: Direct access
from orders.models import Order
order = Order.objects.get(id=123)

# ✅ RIGHT: Through public API
from orders.api import OrderService
order = OrderService.get_order(123)
```

### 2. No Shared Models
Each module owns its models.

```python
# ❌ WRONG: Shared model
class User:  # Used by multiple modules directly
    pass

# ✅ RIGHT: Module-specific representations
# users/models.py
class User: pass

# orders/models.py
class OrderCustomer:  # Orders' view of a user
    user_id: int
    name: str
```

### 3. Separate Schemas

```sql
-- Each module has its schema
CREATE SCHEMA users;
CREATE SCHEMA orders;
CREATE SCHEMA payments;

-- Tables in respective schemas
CREATE TABLE users.accounts (...);
CREATE TABLE orders.orders (...);
CREATE TABLE payments.transactions (...);
```

### 4. No Cross-Schema Joins

```sql
-- ❌ WRONG
SELECT * FROM users.accounts u
JOIN orders.orders o ON u.id = o.user_id;

-- ✅ RIGHT: Query through module API
-- or denormalize needed data
```

## Project Structure

```
src/
├── shared/                 # Truly shared utilities
│   ├── exceptions.py
│   └── utils.py
├── users/                  # User module
│   ├── __init__.py        # Public API exports
│   ├── api.py             # Public interface
│   ├── models.py          # Internal models
│   ├── services.py        # Business logic
│   └── repository.py      # Data access
├── orders/                 # Order module
│   ├── __init__.py
│   ├── api.py
│   ├── models.py
│   ├── services.py
│   └── events.py          # Domain events
├── payments/               # Payment module
│   └── ...
└── main.py                # Application entry
```

## Module Public API

```python
# orders/__init__.py
from .api import (
    create_order,
    get_order,
    cancel_order,
    OrderDTO,
)

__all__ = [
    'create_order',
    'get_order',
    'cancel_order',
    'OrderDTO',
]
```

## Communication Patterns

### Direct Call (Simple)
```python
# In payment module
from orders.api import get_order

order = get_order(order_id)
```

### Events (Decoupled)
```python
# orders/services.py
def complete_order(order_id):
    order = repository.complete(order_id)
    event_bus.publish(OrderCompletedEvent(order_id))

# payments/handlers.py
@event_handler(OrderCompletedEvent)
def handle_order_completed(event):
    process_payment(event.order_id)
```

## Enforcing Boundaries

### Linting Rules
```python
# .importlinter
[importlinter]
root_package = src

[importlinter:contract:modules]
name = Module boundaries
type = independence
modules =
    src.users
    src.orders
    src.payments
```

### Architecture Tests
```python
def test_orders_does_not_import_payments_internals():
    """Orders should only use payments public API"""
    orders_imports = get_imports('orders')
    assert 'payments.models' not in orders_imports
    assert 'payments.repository' not in orders_imports
```

## Migration to Microservices

When ready to extract:

```
1. Module already has:
   - Clear API boundary
   - Own schema
   - Event-based communication

2. Extract:
   - Copy module to new service
   - Replace in-process calls with HTTP/gRPC
   - Replace events with message queue
   - Separate database

3. One module at a time
```

## Related

- [monolith-architecture.md](monolith-architecture.md) - Simpler
- [microservices-architecture.md](microservices-architecture.md) - Next step
- [event-driven-architecture.md](event-driven-architecture.md) - Communication
