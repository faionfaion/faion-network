# DDD Aggregates: Invariant-Enforcing Cluster Roots

## Summary

**One-sentence:** DDD Aggregate root pattern — cluster Entities + Value Objects under one root, enforce invariants via intention-revealing methods, no public setters, identity-only cross-aggregate refs.

**One-paragraph:** An Aggregate is a cluster of domain objects treated as a single unit for data changes. One Entity is the Aggregate Root: all external access goes through it; all invariants are enforced inside its command methods. No public setters; mutation happens through `order.place(...)`, `order.cancel()`. Aggregates reference other aggregates by identity (UUID), never by object reference. This methodology pins five rules: root-only mutation, raise events on state change, identity-only cross-aggregate refs, invariants-as-tests, small aggregate size. Output: an aggregate class + invariant tests conforming to `02-output-contract.xml`.

**Ефективно для:**

- Rich domain with non-trivial invariants (order placement, payment, scheduling).
- Cross-table consistency boundaries within one transaction.
- Codebases adopting CQRS — aggregates own the write side.
- Teams enforcing no-public-setter discipline in code review.
- AI-generated code where regression to anaemic domain is the default.

## Applies If (ALL must hold)

- Domain has invariants that span multiple entities/value objects.
- Strong consistency required within the aggregate's transactional boundary.
- The team has internalized DDD vocabulary.
- Writes go through a repository; queries can use read models / projections.

## Skip If (ANY kills it)

- CRUD-only entity with no real invariants — overhead exceeds benefit.
- Read-heavy reporting service — use projections / DTOs directly.
- Aggregate would span more than ~5 entities — split into smaller aggregates.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain glossary | Markdown | domain owner |
| Invariants list | Markdown bullet list | spec |
| Existing entity sketch | language source / ERD | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-value-objects]] | Aggregates compose value objects for self-validating attributes. |
| [[ddd-repositories]] | Repositories return aggregates; aggregate boundary defines persistence boundary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: root-only-mutation, raise-event-on-mutation, identity-only-refs, invariant-as-test, small-aggregate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for aggregate spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: bypass-root, god-aggregate, object-ref-across-aggregates, invariant-in-service | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: identify boundary → root + invariants → command methods → events → tests | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on consistency boundary + size → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-boundary` | sonnet | Judgment on consistency edges. |
| `write-aggregate-class` | sonnet | Domain scaffolding. |
| `derive-invariant-tests` | haiku | Mechanical mapping of invariant → failing test. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Aggregate.py` | Python aggregate root with collected events |
| `templates/Aggregate.cs` | C# aggregate root with private setters |
| `templates/invariant-tests.md.j2` | Markdown checklist of invariant→test mappings |
| `templates/invariant-tests.md` | Markdown checklist of invariant→test mappings Generated from `templates/invariant-tests.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ddd-aggregates.py` | Validate aggregate spec against schema | Pre-commit on spec artefact |

## Related

- [[ddd-value-objects]]
- [[ddd-repositories]]
- [[ddd-domain-events]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (consistency boundary, aggregate size, transaction scope) to a rule from `01-core-rules.xml`. Use it whenever proposing a new aggregate or refactoring a large one.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Aggregate.py`

```python
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
```

### `templates/Aggregate.cs`

```csharp
namespace Faion.Domain.Orders;

public sealed class Order
{
    private readonly List<OrderItem> _items = new();
    private readonly List<object> _events = new();

    public Guid Id { get; private set; }
    public Guid CustomerId { get; private set; }
    public OrderStatus Status { get; private set; } = OrderStatus.Draft;
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();
    public IReadOnlyList<object> Events => _events.AsReadOnly();

    private Order() { }

    public Order(Guid id, Guid customerId)
    {
        if (customerId == Guid.Empty) throw new ArgumentException("customer required", nameof(customerId));
        Id = id;
        CustomerId = customerId;
        Status = OrderStatus.Draft;
    }

    public void AddItem(string sku, decimal price, int quantity)
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOperationException($"cannot modify order in status {Status}");
        _items.Add(new OrderItem(sku, price, quantity));
    }

    public void Place()
    {
        if (_items.Count == 0)
            throw new InvalidOperationException("cannot place empty order");
        if (Status != OrderStatus.Draft)
            throw new InvalidOperationException($"cannot place order in status {Status}");
        Status = OrderStatus.Placed;
        _events.Add(new OrderPlaced(Id, CustomerId, DateTime.UtcNow));
    }

    public void Cancel()
    {
        if (Status == OrderStatus.Shipped)
            throw new InvalidOperationException("cannot cancel shipped order");
        Status = OrderStatus.Cancelled;
        _events.Add(new OrderCancelled(Id, DateTime.UtcNow));
    }

    public List<object> CollectEvents()
    {
        var snapshot = _events.ToList();
        _events.Clear();
        return snapshot;
    }
}

public sealed record OrderItem(string Sku, decimal Price, int Quantity);
public enum OrderStatus { Draft, Placed, Shipped, Cancelled }
public sealed record OrderPlaced(Guid OrderId, Guid CustomerId, DateTime OccurredAt);
public sealed record OrderCancelled(Guid OrderId, DateTime OccurredAt);
```
