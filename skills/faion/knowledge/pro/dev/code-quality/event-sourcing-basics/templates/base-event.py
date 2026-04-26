"""Base Event dataclass and example domain event skeleton for event sourcing."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Event:
    """Base class for all domain events. frozen=True enforces immutability."""
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict = field(default_factory=dict)


# --- Example domain events ---

@dataclass(frozen=True)
class OrderCreated(Event):
    """Event raised when a new order is created."""
    order_id: UUID = field(default=None)
    customer_id: UUID = field(default=None)


@dataclass(frozen=True)
class OrderPlaced(Event):
    """Event raised when a draft order is placed."""
    order_id: UUID = field(default=None)
    shipping_address: dict = field(default_factory=dict)
    total_amount: float = 0.0


@dataclass(frozen=True)
class OrderCancelled(Event):
    """Event raised when an order is cancelled."""
    order_id: UUID = field(default=None)
    reason: str = ""
    cancelled_by: Optional[UUID] = None
