# purpose: projection skeleton with idempotent UPSERTs + checkpoint
# consumes: event subscription + read store
# produces: projection class
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~250 tokens when loaded as reference

from __future__ import annotations

from typing import Protocol


class ReadStore(Protocol):
    def upsert(self, table: str, key: dict, payload: dict) -> None: ...
    def delete(self, table: str, key: dict) -> None: ...
    def get_checkpoint(self, name: str) -> int: ...
    def set_checkpoint(self, name: str, position: int) -> None: ...


class OrdersListProjection:
    NAME = "orders_list"
    TABLE = "orders_list"

    def __init__(self, store: ReadStore) -> None:
        self._store = store

    def handle(self, event, position: int) -> None:
        method = getattr(self, f"_on_{type(event).__name__}", None)
        if method is not None:
            method(event)
        self._store.set_checkpoint(self.NAME, position)

    def _on_OrderPlaced(self, ev) -> None:
        self._store.upsert(
            self.TABLE,
            key={"order_id": ev.order_id},
            payload={
                "order_id": ev.order_id,
                "customer_id": ev.customer_id,
                "status": "placed",
                "total": 0,
            },
        )

    def _on_ItemAdded(self, ev) -> None:
        self._store.upsert(
            self.TABLE,
            key={"order_id": ev.order_id},
            payload={"increment_total": ev.price * ev.quantity},
        )

    def _on_OrderCancelled(self, ev) -> None:
        self._store.delete(self.TABLE, key={"order_id": ev.order_id})
