"""
Domain Events Template

Events published by a module for other modules to consume.
Events are immutable facts; include event_id and version for evolution.
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1


@dataclass(frozen=True)
class OrderCreatedEvent(DomainEvent):
    """Published when a new order is created."""
    order_id: str = ""
    user_id: str = ""
    total_amount: float = 0.0


@dataclass(frozen=True)
class OrderCompletedEvent(DomainEvent):
    """Published when an order is marked as completed."""
    order_id: str = ""
    user_id: str = ""


@dataclass(frozen=True)
class OrderCancelledEvent(DomainEvent):
    """Published when an order is cancelled."""
    order_id: str = ""
    user_id: str = ""
    reason: str = ""
