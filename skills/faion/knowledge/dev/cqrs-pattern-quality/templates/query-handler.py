"""
purpose: Query + QueryHandler skeleton; returns a read model only.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (cqrs-pattern)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


@dataclass
class Query:
    pass


class QueryHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, q: Query) -> T: ...


@dataclass
class GetOrderQuery(Query):
    order_id: UUID


@dataclass
class OrderView:
    order_id: UUID
    status: str
    total_cents: int


class GetOrderHandler(QueryHandler[OrderView]):
    async def handle(self, q: GetOrderQuery) -> OrderView:
        # read from projection / view
        return OrderView(q.order_id, "placed", 0)
