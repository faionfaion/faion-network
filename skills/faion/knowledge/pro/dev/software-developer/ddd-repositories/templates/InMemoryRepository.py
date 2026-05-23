# purpose: in-memory test double satisfying the same port as the SQLAlchemy adapter
# consumes: only domain types
# produces: pure-Python repository for unit tests
# depends-on: content/01-core-rules.xml, templates/RepositoryInterface.py
# token-budget-impact: ~150 tokens when loaded as reference

from __future__ import annotations

from typing import Optional
from uuid import UUID

from ..domain.order import Order
from ..domain.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._by_id: dict[UUID, Order] = {}
        self._by_key: dict[str, UUID] = {}

    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        return self._by_id.get(order_id)

    def find_by_external_key(self, key: str) -> Optional[Order]:
        oid = self._by_key.get(key)
        return None if oid is None else self._by_id.get(oid)

    def save(self, order: Order) -> None:
        self._by_id[order.id] = order

    def delete(self, order: Order) -> None:
        self._by_id.pop(order.id, None)
