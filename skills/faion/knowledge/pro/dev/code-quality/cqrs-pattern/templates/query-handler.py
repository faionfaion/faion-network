"""CQRS query-side skeleton: Query base, QueryHandler base, OrderDto read model."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from uuid import UUID

T = TypeVar("T")
R = TypeVar("R")


@dataclass
class Query(ABC):
    """Base for all queries. Queries never modify state."""


class QueryHandler(ABC, Generic[T, R]):
    """Base for query handlers. Returns a read model."""

    @abstractmethod
    async def handle(self, query: T) -> R:
        pass


# --- Example read model and handler ---

@dataclass
class OrderDto:
    id: UUID
    customer_id: UUID
    status: str
    items: list
    total: float
    placed_at: Optional[str]


@dataclass
class GetOrderQuery(Query):
    order_id: UUID


class GetOrderHandler(QueryHandler[GetOrderQuery, OrderDto]):
    def __init__(self, read_store):
        self._read_store = read_store

    async def handle(self, query: GetOrderQuery) -> OrderDto:
        data = await self._read_store.get(f"order:{query.order_id}")
        if not data:
            raise KeyError(f"Order not found: {query.order_id}")
        return OrderDto(**data)
