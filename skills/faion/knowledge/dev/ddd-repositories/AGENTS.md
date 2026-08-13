# DDD Repository Pattern: Domain-Owned Persistence Interfaces

## Summary

**One-sentence:** DDD Repository pattern — domain owns the interface (no ORM types); infra implements; returns reconstituted aggregates; queries by identity only.

**One-paragraph:** A Repository provides a collection-like interface for accessing Aggregates. The Domain layer defines the interface (`find_by_id`, `save`, `delete`); the Infrastructure layer implements it against the ORM. The domain MUST never import SQLAlchemy / EF / JPA types; the repository returns fully reconstituted aggregate objects, never raw ORM models. Collection queries by arbitrary criteria belong in Read Models / Query Services, not in the repository. This methodology pins five rules: domain owns the interface, return aggregates not ORM models, identity-only queries, infra translates persistence ↔ domain, ports + adapters. Output: a repository interface + implementation + mapper conforming to `02-output-contract.xml`.

**Ефективно для:**

- Persisting aggregate roots cleanly without ORM coupling in domain code.
- Replacing the ORM in the future (SQLAlchemy → Django ORM → EF) without domain rewrites.
- Testing domain logic without spinning up a DB (mock the repository).
- Multi-store systems where one aggregate lives in DB + Redis + S3.
- Cross-language DDD reference architecture.

## Applies If (ALL must hold)

- Domain logic exists separately from persistence code.
- The team commits to keeping ORM imports out of the domain.
- Aggregates per `[[ddd-aggregates]]` are the persistence unit.
- The application needs `find_by_id` + `save` more often than arbitrary queries.

## Skip If (ANY kills it)

- CRUD-only project — Active Record on the model is enough.
- Reporting service with mostly arbitrary queries — use Query Services / projections.
- Single-file script — overhead exceeds benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Aggregate root + value objects | source | repo |
| ORM model (existing) | source | repo |
| DB connection / session | config | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-aggregates]] | Repository persists aggregates as a unit. |
| [[ddd-value-objects]] | Value objects need (de)serialization across the persistence boundary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: domain-owns-interface, return-aggregates, identity-only-queries, infra-translates, ports-and-adapters | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for repository spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: orm-types-in-domain, arbitrary-query-method, lazy-load-leak, fat-repository | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on aggregate write-pattern → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-interface` | sonnet | Vocabulary + boundary judgment. |
| `write-implementation` | sonnet | ORM mapping scaffolding. |
| `write-domain-mock` | haiku | Mechanical in-memory stub for tests. |

## Templates

| File | Purpose |
|------|---------|
| `templates/RepositoryInterface.py` | Domain-layer interface skeleton |
| `templates/SqlAlchemyRepository.py` | Infra implementation + mapper |
| `templates/InMemoryRepository.py` | Test double for domain tests |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ddd-repositories.py` | Validate repository spec against schema | Pre-commit on spec artefact |

## Related

- [[ddd-aggregates]]
- [[ddd-value-objects]]
- [[ddd-anti-corruption-layer]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (query shape, aggregate count, ORM dependency cost) to a rule from `01-core-rules.xml`. Use it whenever adding a new repository or refactoring a method that currently returns `IQueryable`/`QuerySet`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/RepositoryInterface.py`

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

# import only domain types; the line below is a domain import, not an ORM one
from .order import Order


class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]: ...

    @abstractmethod
    def find_by_external_key(self, key: str) -> Optional[Order]: ...

    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def delete(self, order: Order) -> None: ...
```

### `templates/SqlAlchemyRepository.py`

```python
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
```

### `templates/InMemoryRepository.py`

```python
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
```
