# purpose: Python aggregate root with command methods + event collection
# consumes: domain constructor inputs
# produces: aggregate class for the domain layer
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~350 tokens when loaded as reference

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4


@dataclass(frozen=True)
class OrderPlaced:
    order_id: UUID
    customer_id: UUID
    occurred_at: datetime
    event_id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class OrderCancelled:
    order_id: UUID
    occurred_at: datetime
    event_id: UUID = field(default_factory=uuid4)


class Order:
    def __init__(self, order_id: UUID, customer_id: UUID) -> None:
        self._id = order_id
        self._customer_id = customer_id          # identity-only cross-aggregate ref
        self._status = "draft"
        self._items: List["OrderItem"] = []
        self._events: List[object] = []

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def items(self) -> tuple["OrderItem", ...]:
        return tuple(self._items)

    @property
    def status(self) -> str:
        return self._status

    def add_item(self, sku: str, price: float, quantity: int) -> None:
        if self._status != "draft":
            raise ValueError(f"cannot modify order in status {self._status}")
        self._items.append(OrderItem(sku, price, quantity))

    def place(self) -> None:
        if not self._items:
            raise ValueError("cannot place empty order")
        if self._status != "draft":
            raise ValueError(f"cannot place order in status {self._status}")
        self._status = "placed"
        self._events.append(OrderPlaced(self._id, self._customer_id, datetime.utcnow()))

    def cancel(self) -> None:
        if self._status == "shipped":
            raise ValueError("cannot cancel shipped order")
        self._status = "cancelled"
        self._events.append(OrderCancelled(self._id, datetime.utcnow()))

    def collect_events(self) -> list[object]:
        events, self._events = self._events, []
        return events


@dataclass(frozen=True)
class OrderItem:
    sku: str
    price: float
    quantity: int
