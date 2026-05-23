# purpose: infrastructure-layer SQLAlchemy adapter for OrderRepository
# consumes: SQLAlchemy Session + ORM model
# produces: reconstituted Order aggregates
# depends-on: content/01-core-rules.xml, templates/RepositoryInterface.py
# token-budget-impact: ~350 tokens when loaded as reference

from __future__ import annotations

from typing import Optional
from uuid import UUID

# Vendor imports live HERE — never in the domain layer.
from sqlalchemy.orm import Session

from ..domain.order import Order, OrderItem
from ..domain.order_repository import OrderRepository
from .models import OrderModel, OrderItemModel  # ORM models


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        row = self._session.get(OrderModel, order_id)
        return None if row is None else self._to_aggregate(row)

    def find_by_external_key(self, key: str) -> Optional[Order]:
        row = self._session.query(OrderModel).filter_by(external_key=key).one_or_none()
        return None if row is None else self._to_aggregate(row)

    def save(self, order: Order) -> None:
        existing = self._session.get(OrderModel, order.id)
        if existing is None:
            self._session.add(self._to_model(order))
        else:
            self._merge_state(order, existing)

    def delete(self, order: Order) -> None:
        row = self._session.get(OrderModel, order.id)
        if row is not None:
            self._session.delete(row)

    @staticmethod
    def _to_aggregate(row: OrderModel) -> Order:
        order = Order(row.id, row.customer_id)
        for item_row in row.items:
            order._items.append(OrderItem(item_row.sku, item_row.price, item_row.quantity))
        return order

    @staticmethod
    def _to_model(order: Order) -> OrderModel:
        return OrderModel(
            id=order.id,
            customer_id=order._customer_id,
            items=[OrderItemModel(sku=i.sku, price=i.price, quantity=i.quantity) for i in order.items],
        )

    def _merge_state(self, order: Order, existing: OrderModel) -> None:
        existing.items.clear()
        for it in order.items:
            existing.items.append(OrderItemModel(sku=it.sku, price=it.price, quantity=it.quantity))
