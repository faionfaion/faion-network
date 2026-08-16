# CQRS Pattern

## Summary

**One-sentence:** Produces a CQRS skeleton: Command + CommandHandler returning None/ID; Query + QueryHandler returning a read model; a Mediator that dispatches by type with no handler doing both shapes.

**One-paragraph:** CQRS separates write and read sides into distinct models: commands change state and return None or an ID; queries return data and never modify state. A handler is either CommandHandler or QueryHandler — never both. This lets the write side enforce invariants on a domain model while the read side uses flat projections optimised per query (Redis, Elasticsearch, denormalised SQL views).

**Ефективно для:**

- High read/write ratio з різними optimization patterns.
- Складний domain + кілька read models per use case.
- Audit trail через events що драйвлять projections.
- Eventual consistency через design, не випадково.

## Applies If (ALL must hold)

- High read/write ratio where each side has different optimization needs.
- Complex domain with separate read models per use case.
- System needs event-driven projections rebuilding read models.
- Application paired with event sourcing.

## Skip If (ANY kills it)

- Simple CRUD where reads and writes are symmetric.
- Team unfamiliar with eventual consistency.
- System needs immediate read-after-write consistency.
- Small domain where a single repository covers all queries.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model with identified commands + queries | list | domain expert |
| Read-side persistence target (Redis / SQL view / Elasticsearch) | infra | team |
| Mediator or DI container | tool | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[clean-architecture]] | CQRS handlers sit in the application layer; clean-architecture defines that layer |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-handlers` | sonnet | Generate CommandHandler + QueryHandler stubs. |
| `author-mediator` | sonnet | Write the dispatcher with type-based routing. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/command-handler.py` | Command + CommandHandler skeleton; returns None or ID only. |
| `templates/query-handler.py` | Query + QueryHandler skeleton; returns a read model only. |
| `templates/mediator.py` | Type-based Mediator dispatching to the right handler. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[clean-architecture]]
- [[event-sourcing-basics]]
- [[event-sourcing-implementation]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates CQRS on read/write asymmetry + team readiness for eventual consistency; otherwise plain repository pattern is enough.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/command-handler.py`

```python
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID, uuid4

T = TypeVar("T")


@dataclass
class Command:
    pass


class CommandHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, cmd: Command) -> T | None: ...


@dataclass
class PlaceOrderCommand(Command):
    user_id: UUID
    items: list[str]


class PlaceOrderHandler(CommandHandler[UUID]):
    async def handle(self, cmd: PlaceOrderCommand) -> UUID:
        # validate, write to event store, return new id
        return uuid4()
```

### `templates/query-handler.py`

```python
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
```

### `templates/mediator.py`

```python
"""
from typing import Any


class Mediator:
    def __init__(self) -> None:
        self._handlers: dict[type, Any] = {}

    def register(self, message_type: type, handler: Any) -> None:
        self._handlers[message_type] = handler

    async def send(self, message: Any) -> Any:
        handler = self._handlers.get(type(message))
        if handler is None:
            raise KeyError(f"no handler for {type(message).__name__}")
        return await handler.handle(message)
```
