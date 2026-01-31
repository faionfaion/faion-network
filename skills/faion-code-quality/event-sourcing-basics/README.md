---
id: event-sourcing-basics
name: "Event Sourcing - Basics"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Event Sourcing - Basics

## Overview

Event Sourcing persists the state of an entity as a sequence of state-changing events. Instead of storing current state, you store all events that led to it. The current state is derived by replaying events.

## When to Use

- Complete audit trail required
- Complex domain with temporal queries
- Event-driven architectures
- Systems requiring state reconstruction
- Financial or compliance-heavy applications

## Key Principles

1. **Events are immutable** - Once stored, events never change
2. **Events are the source of truth** - State is derived from events
3. **Event order matters** - Events must be applied in sequence
4. **Snapshots for performance** - Periodically save state snapshots
5. **Projections for queries** - Build read models from events

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Command Handler                          │
│  1. Load events from store                                    │
│  2. Reconstruct aggregate                                     │
│  3. Execute command (generate new events)                     │
│  4. Persist new events                                        │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                       Event Store                             │
│  ┌─────────┬─────────┬───────────┬──────────────────────┐    │
│  │ EventId │ StreamId│  Version  │     Event Data        │    │
│  ├─────────┼─────────┼───────────┼──────────────────────┤    │
│  │    1    │ order-1 │     1     │ OrderCreated {...}   │    │
│  │    2    │ order-1 │     2     │ ItemAdded {...}      │    │
│  │    3    │ order-1 │     3     │ ItemAdded {...}      │    │
│  │    4    │ order-1 │     4     │ OrderPlaced {...}    │    │
│  └─────────┴─────────┴───────────┴──────────────────────┘    │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                      Projections                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Order Details│  │ Customer     │  │ Analytics    │       │
│  │ Projection   │  │ Orders List  │  │ Projection   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────────────────────────────────────────────┘
```

## Event Definitions

```python
# domain/events/base.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Event:
    """Base class for all domain events."""
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict = field(default_factory=dict)


# domain/events/order_events.py
from dataclasses import dataclass
from decimal import Decimal
from typing import List
from uuid import UUID


@dataclass(frozen=True)
class OrderCreated(Event):
    """Event when order is created."""
    order_id: UUID
    customer_id: UUID


@dataclass(frozen=True)
class OrderItemAdded(Event):
    """Event when item is added to order."""
    order_id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class OrderItemRemoved(Event):
    """Event when item is removed from order."""
    order_id: UUID
    product_id: UUID


@dataclass(frozen=True)
class OrderPlaced(Event):
    """Event when order is placed."""
    order_id: UUID
    shipping_address: dict
    total_amount: Decimal


@dataclass(frozen=True)
class OrderShipped(Event):
    """Event when order is shipped."""
    order_id: UUID
    tracking_number: str
    carrier: str


@dataclass(frozen=True)
class OrderDelivered(Event):
    """Event when order is delivered."""
    order_id: UUID
    delivered_at: datetime
    signature: Optional[str] = None


@dataclass(frozen=True)
class OrderCancelled(Event):
    """Event when order is cancelled."""
    order_id: UUID
    reason: str
    cancelled_by: UUID
```

## Event-Sourced Aggregate

```python
# domain/aggregates/order.py
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from domain.events.order_events import *


class OrderStatus(Enum):
    DRAFT = "draft"
    PLACED = "placed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Order:
    """Event-sourced Order aggregate."""

    id: UUID
    customer_id: UUID = None
    status: OrderStatus = OrderStatus.DRAFT
    items: List[OrderItem] = field(default_factory=list)
    shipping_address: dict = None
    tracking_number: str = None
    version: int = 0
    _pending_events: List[Event] = field(default_factory=list, repr=False)

    @classmethod
    def create(cls, order_id: UUID, customer_id: UUID) -> "Order":
        """Factory method - creates new order with initial event."""
        order = cls(id=order_id)
        order._apply(OrderCreated(order_id=order_id, customer_id=customer_id))
        return order

    @classmethod
    def from_events(cls, order_id: UUID, events: List[Event]) -> "Order":
        """Reconstruct order from event history."""
        order = cls(id=order_id)
        for event in events:
            order._apply(event, is_new=False)
        return order

    def add_item(
        self,
        product_id: UUID,
        product_name: str,
        quantity: int,
        unit_price: Decimal,
    ) -> None:
        """Add item to order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Cannot modify placed order")

        if quantity <= 0:
            raise DomainError("Quantity must be positive")

        # Check if already in order
        if any(item.product_id == product_id for item in self.items):
            raise DomainError("Product already in order")

        self._apply(OrderItemAdded(
            order_id=self.id,
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price,
        ))

    def remove_item(self, product_id: UUID) -> None:
        """Remove item from order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Cannot modify placed order")

        if not any(item.product_id == product_id for item in self.items):
            raise DomainError("Product not in order")

        self._apply(OrderItemRemoved(order_id=self.id, product_id=product_id))

    def place(self, shipping_address: dict) -> None:
        """Place the order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Order already placed")

        if not self.items:
            raise DomainError("Cannot place empty order")

        self._apply(OrderPlaced(
            order_id=self.id,
            shipping_address=shipping_address,
            total_amount=self.total,
        ))

    def ship(self, tracking_number: str, carrier: str) -> None:
        """Ship the order."""
        if self.status != OrderStatus.PLACED:
            raise DomainError("Order must be placed before shipping")

        self._apply(OrderShipped(
            order_id=self.id,
            tracking_number=tracking_number,
            carrier=carrier,
        ))

    def cancel(self, reason: str, cancelled_by: UUID) -> None:
        """Cancel the order."""
        if self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise DomainError("Cannot cancel shipped order")

        self._apply(OrderCancelled(
            order_id=self.id,
            reason=reason,
            cancelled_by=cancelled_by,
        ))

    @property
    def total(self) -> Decimal:
        return sum(item.total for item in self.items)

    def _apply(self, event: Event, is_new: bool = True) -> None:
        """Apply event to aggregate state."""
        # Route to appropriate handler
        handler_name = f"_on_{self._to_snake_case(type(event).__name__)}"
        handler = getattr(self, handler_name, None)

        if handler:
            handler(event)

        self.version += 1

        if is_new:
            self._pending_events.append(event)

    def _on_order_created(self, event: OrderCreated) -> None:
        self.customer_id = event.customer_id
        self.status = OrderStatus.DRAFT

    def _on_order_item_added(self, event: OrderItemAdded) -> None:
        self.items.append(OrderItem(
            product_id=event.product_id,
            product_name=event.product_name,
            quantity=event.quantity,
            unit_price=event.unit_price,
        ))

    def _on_order_item_removed(self, event: OrderItemRemoved) -> None:
        self.items = [i for i in self.items if i.product_id != event.product_id]

    def _on_order_placed(self, event: OrderPlaced) -> None:
        self.shipping_address = event.shipping_address
        self.status = OrderStatus.PLACED

    def _on_order_shipped(self, event: OrderShipped) -> None:
        self.tracking_number = event.tracking_number
        self.status = OrderStatus.SHIPPED

    def _on_order_cancelled(self, event: OrderCancelled) -> None:
        self.status = OrderStatus.CANCELLED

    def collect_pending_events(self) -> List[Event]:
        """Get and clear pending events."""
        events = self._pending_events.copy()
        self._pending_events.clear()
        return events

    @staticmethod
    def _to_snake_case(name: str) -> str:
        import re
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
```

## Anti-patterns

### Avoid: Mutable Events

```python
# BAD - modifying event data
event = OrderCreated(order_id=order_id)
event.customer_id = new_customer_id  # Never do this!

# GOOD - events are immutable
@dataclass(frozen=True)
class OrderCreated(Event):
    order_id: UUID
    customer_id: UUID
```

### Avoid: Large Events

```python
# BAD - entire state in one event
@dataclass
class OrderUpdated(Event):
    entire_order_data: dict  # Contains everything

# GOOD - specific events for each change
@dataclass
class OrderItemAdded(Event):
    product_id: UUID
    quantity: int

@dataclass
class ShippingAddressChanged(Event):
    new_address: Address
```

## References

- [Event Sourcing by Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Greg Young - Event Sourcing](https://www.youtube.com/watch?v=8JKjvY4etTY)
- [EventStoreDB](https://www.eventstore.com/)
- [Marten Events](https://martendb.io/events/)

## See Also

- [event-sourcing-implementation.md](event-sourcing-implementation.md) - Event store, snapshots, projections
