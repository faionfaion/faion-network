# DDD Domain Events: Raising, Collecting, and Dispatching

## Summary

**One-sentence:** DDD Domain Events pattern — raise frozen event records inside aggregate command methods; collect after commit; pair with Outbox for cross-broker delivery.

**One-paragraph:** Domain Events make state changes observable across the system without coupling the producer to consumers. Events are raised inside aggregate command methods (`order.place()` appends `OrderPlaced` to `self._events`); the application service collects events after the DB commit and dispatches them. For systems with message brokers (Kafka, RabbitMQ, SNS) raw dispatch suffers from dual-write bugs — the Outbox pattern fixes this by writing the event to an outbox table in the same DB transaction. This methodology pins five rules: frozen events, raised on the aggregate, collected after commit, identifier + timestamp metadata, Outbox for brokered delivery. Output: event records + outbox row spec conforming to `02-output-contract.xml`.

**Ефективно для:**

- Cross-bounded-context notifications without RPC coupling.
- Event-sourcing read-model rebuilds.
- Async workflows triggered by domain state changes.
- Audit trails / activity streams derived from events.
- Outbox pattern implementation against any DB + broker pair.

## Applies If (ALL must hold)

- Aggregate state changes have downstream consequences (other contexts, async workflows).
- The team can guarantee event collection runs after DB commit, not before.
- A message broker or in-process dispatcher is wired in (or planned).
- Domain logic lives on aggregates per `[[ddd-aggregates]]`.

## Skip If (ANY kills it)

- Monolithic CRUD app with no async workflow — events add complexity without payoff.
- Synchronous workflows where direct method calls are clearer than event indirection.
- Bus-without-outbox systems unwilling to handle dual-write — defer until outbox can be built.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Aggregate root | source | repo |
| Broker / dispatcher contract | docs | infra |
| Outbox table schema | DDL or migration | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-aggregates]] | Events live on aggregates. |
| [[event-sourcing-fundamentals]] | Sibling pattern — events as the source of truth (not just notifications). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: frozen-events, raise-on-aggregate, collect-after-commit, event-metadata, outbox-on-broker | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for event + outbox row spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: mutable-event, dispatch-before-commit, dual-write, missing-event-id | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on delivery target → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-event-record` | sonnet | Naming + payload judgment. |
| `wire-outbox` | sonnet | DB + broker plumbing. |
| `verify-collect-after-commit` | haiku | Mechanical assertion on app-service order. |

## Templates

| File | Purpose |
|------|---------|
| `templates/DomainEvent.py` | Frozen event record skeleton |
| `templates/Outbox.py` | Outbox publisher + DB row spec |
| `templates/dispatch.md` | Application-service dispatch sequence |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ddd-domain-events.py` | Validate event + outbox spec | Pre-commit on spec artefact |

## Related

- [[ddd-aggregates]]
- [[event-sourcing-fundamentals]]
- [[event-sourcing-versioning]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps delivery target (in-process vs broker) to a rule from `01-core-rules.xml`. Use it whenever raising a new event or wiring an event to a downstream consumer.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/DomainEvent.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class OrderPlaced:
    order_id: UUID
    customer_id: UUID
    total: float
    occurred_at: datetime = field(default_factory=_now)
    event_id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class OrderCancelled:
    order_id: UUID
    reason: str
    occurred_at: datetime = field(default_factory=_now)
    event_id: UUID = field(default_factory=uuid4)
```

### `templates/Outbox.py`

```python
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable, Protocol
from uuid import UUID

log = logging.getLogger(__name__)


@dataclass
class OutboxRow:
    event_id: UUID
    event_name: str
    aggregate_identity: str
    payload_json: str
    occurred_at: datetime
    processed_at: datetime | None = None


class OutboxStore(Protocol):
    def append(self, row: OutboxRow) -> None: ...
    def claim_unprocessed(self, batch_size: int) -> list[OutboxRow]: ...
    def mark_processed(self, event_id: UUID) -> None: ...


class Broker(Protocol):
    def publish(self, topic: str, payload: dict, idempotency_key: str) -> None: ...


def append_events_to_outbox(store: OutboxStore, events: Iterable[object]) -> None:
    """Call INSIDE the same DB transaction as the aggregate state change."""
    for ev in events:
        row = OutboxRow(
            event_id=getattr(ev, "event_id"),
            event_name=type(ev).__name__,
            aggregate_identity=_extract_identity(ev),
            payload_json=json.dumps(asdict(ev), default=str),
            occurred_at=getattr(ev, "occurred_at", datetime.now(timezone.utc)),
        )
        store.append(row)


def relay_once(store: OutboxStore, broker: Broker, topic: str, batch: int = 100) -> int:
    rows = store.claim_unprocessed(batch)
    for row in rows:
        try:
            broker.publish(topic, json.loads(row.payload_json), idempotency_key=str(row.event_id))
            store.mark_processed(row.event_id)
        except Exception as exc:  # broker publish failed; leave row unprocessed for retry
            log.warning("outbox publish failed for %s: %s", row.event_id, exc)
            break
    return len(rows)


def _extract_identity(ev: object) -> str:
    for attr in ("order_id", "customer_id", "aggregate_id"):
        if hasattr(ev, attr):
            return str(getattr(ev, attr))
    return "unknown"
```
