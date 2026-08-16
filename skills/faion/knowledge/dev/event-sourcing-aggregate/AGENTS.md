# Event Sourcing — Aggregate Root Pattern

## Summary

**One-sentence:** Event-sourced aggregate root pattern — replay events to rebuild state, mutate only in apply handlers, command methods emit, repository.save with expected_version.

**One-paragraph:** An event-sourced aggregate reconstructs state by replaying events through `apply()` handlers; it emits new events from command methods but NEVER mutates state directly there. The repository loads `(events, version)`, the command runs, and `save(stream_id, new_events, expected_version)` enforces optimistic concurrency. This methodology pins five rules: apply-only mutation, command methods emit + return, expected_version on save, `from_events` reconstruction, `collect_pending_events` boundary. Output: aggregate + event classes + repository scaffold conforming to `02-output-contract.xml`.

**Ефективно для:**

- New event-sourced aggregates (Order, Subscription, Wallet).
- Migrating CRUD entity to ES while preserving domain logic.
- Codifying invariants as event-emission patterns.
- Concurrency-safe writes via expected_version.
- Pair-trained AI agent runs per `[[event-sourcing-agentic]]`.

## Applies If (ALL must hold)

- Event sourcing is the persistence pattern (not just notifications).
- An event-store library (or hand-rolled equivalent) is in place.
- Aggregates per `[[ddd-aggregates]]` are the unit of consistency.
- The team understands optimistic concurrency + version semantics.

## Skip If (ANY kills it)

- CRUD app pretending to use ES — overhead exceeds benefit.
- Aggregate has no invariants — events without invariants are just an audit log; use `[[ddd-domain-events]]` instead.
- Sub-millisecond write latency requirement — replay overhead dominates.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event catalog | YAML/Markdown | repo |
| Aggregate boundary | spec | spec |
| Event-store API docs | URL | infra |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[event-sourcing-fundamentals]] | Core invariants the aggregate must protect. |
| [[ddd-aggregates]] | Aggregate-root rules (no public setters etc.). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: apply-only-mutation, command-emits-returns, expected-version-on-save, from-events-reconstruction, collect-pending-boundary | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for aggregate spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: mutate-in-command, save-without-version, lazy-apply, leaked-events | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on aggregate workload → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-event-list` | sonnet | Domain judgment. |
| `write-apply-handlers` | sonnet | Mechanical mapping per event. |
| `write-concurrency-test` | haiku | Generate expected_version clash test. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Aggregate.py` | Event-sourced aggregate skeleton |
| `templates/Repository.py` | Repository with expected_version semantics |
| `templates/ConcurrencyTest.py` | Optimistic-concurrency clash test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-aggregate.py` | Validate aggregate spec | Pre-commit on spec artefact |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[event-sourcing-fundamentals]]
- [[event-sourcing-projections]]
- [[event-sourcing-snapshots]]
- [[event-sourcing-versioning]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (write rate, concurrency, replay cost) to a rule from `01-core-rules.xml` and either approves ES-aggregate scaffolding or redirects to a CRUD aggregate / read-model-only design.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Aggregate.py`

```python
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
```

### `templates/Repository.py`

```python
from __future__ import annotations

from typing import Protocol
from uuid import UUID


class EventStore(Protocol):
    def read_stream(self, stream_id: UUID) -> tuple[list[object], int]: ...
    def append(self, stream_id: UUID, events: list[object], expected_version: int) -> int: ...


class ConcurrencyError(RuntimeError):
    """Raised when expected_version did not match the store's last version."""


class OrderRepository:
    def __init__(self, store: EventStore) -> None:
        self._store = store

    def load(self, stream_id: UUID):
        events, version = self._store.read_stream(stream_id)
        from .aggregate import Order
        return Order.from_events(stream_id, events), version

    def save(self, stream_id: UUID, aggregate, expected_version: int) -> int:
        pending = aggregate.collect_pending_events()
        if not pending:
            return expected_version
        try:
            return self._store.append(stream_id, pending, expected_version)
        except Exception as exc:
            # restore pending so caller can retry the command
            aggregate._pending = pending + aggregate._pending
            raise ConcurrencyError(str(exc)) from exc
```

### `templates/ConcurrencyTest.py`

```python
from __future__ import annotations

import pytest
from uuid import uuid4

from .repository import OrderRepository, ConcurrencyError


class InMemoryStore:
    def __init__(self) -> None:
        self._streams: dict = {}

    def read_stream(self, stream_id):
        events = self._streams.get(stream_id, [])
        return list(events), len(events)

    def append(self, stream_id, events, expected_version):
        existing = self._streams.get(stream_id, [])
        if len(existing) != expected_version:
            raise RuntimeError(f"version clash: expected {expected_version}, got {len(existing)}")
        self._streams[stream_id] = existing + list(events)
        return len(self._streams[stream_id])


def test_concurrent_commands_raise_concurrency_error():
    store = InMemoryStore()
    repo = OrderRepository(store)
    stream_id = uuid4()

    a, version_a = repo.load(stream_id)
    b, version_b = repo.load(stream_id)
    assert version_a == version_b == 0

    a.place(customer_id=uuid4())
    b.place(customer_id=uuid4())

    repo.save(stream_id, a, expected_version=version_a)

    with pytest.raises(ConcurrencyError):
        repo.save(stream_id, b, expected_version=version_b)
```
