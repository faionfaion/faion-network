# purpose: event-sourced aggregate with apply-only mutation + collect_pending_events
# consumes: command inputs
# produces: domain aggregate type
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~350 tokens when loaded as reference

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List
from uuid import UUID, uuid4


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class OrderPlaced:
    order_id: UUID
    customer_id: UUID
    occurred_at: datetime = field(default_factory=_now)
    event_id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class ItemAdded:
    order_id: UUID
    sku: str
    price: float
    quantity: int
    occurred_at: datetime = field(default_factory=_now)
    event_id: UUID = field(default_factory=uuid4)


class Order:
    def __init__(self, order_id: UUID) -> None:
        self._id = order_id
        self._customer_id: UUID | None = None
        self._items: list[ItemAdded] = []
        self._status = "draft"
        self._pending: List[object] = []

    # ----- reconstruction --------------------------------------------------
    @classmethod
    def from_events(cls, order_id: UUID, events: list[object]) -> "Order":
        agg = cls(order_id)
        for ev in events:
            agg._apply(ev)
        return agg

    def _apply(self, ev: object) -> None:
        handler = getattr(self, f"_apply_{type(ev).__name__}", None)
        if handler is None:
            raise RuntimeError(f"missing apply handler for {type(ev).__name__}")
        handler(ev)

    # ----- apply handlers (state mutation lives ONLY here) -----------------
    def _apply_OrderPlaced(self, ev: OrderPlaced) -> None:
        self._customer_id = ev.customer_id
        self._status = "placed"

    def _apply_ItemAdded(self, ev: ItemAdded) -> None:
        self._items.append(ev)

    # ----- commands (validate + emit + return) -----------------------------
    def place(self, customer_id: UUID) -> None:
        if self._status != "draft":
            raise ValueError(f"cannot place order in status {self._status}")
        ev = OrderPlaced(order_id=self._id, customer_id=customer_id)
        self._pending.append(ev)
        self._apply(ev)

    def add_item(self, sku: str, price: float, quantity: int) -> None:
        if self._status != "placed":
            raise ValueError(f"cannot add item in status {self._status}")
        ev = ItemAdded(order_id=self._id, sku=sku, price=price, quantity=quantity)
        self._pending.append(ev)
        self._apply(ev)

    # ----- boundary --------------------------------------------------------
    def collect_pending_events(self) -> list[object]:
        events, self._pending = self._pending, []
        return events
