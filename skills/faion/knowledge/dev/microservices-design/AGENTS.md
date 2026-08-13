# Microservices Design

## Summary

**One-sentence:** Produces a microservices spec naming bounded contexts, per-service data ownership, transport contracts (HTTP/gRPC/async), circuit-breaker policies, and rules forbidding cross-service code imports and shared tables.

**One-paragraph:** Microservices structure an application as independently deployable services where each service owns its data, exposes a well-defined API, and communicates via HTTP/gRPC or async messaging. Each service has exactly one database (no shared tables); services never import each other's code directly; failures in one service must not cascade to others.

**Ефективно для:**

- Large application з кількома teams що працюють паралельно.
- Independent scaling (checkout 10x під час flash sales, user service ні).
- Continuous deployment де lockstep releases — bottleneck.
- Technology diversity з justified причиною (ML Python, billing Java).

## Applies If (ALL must hold)

- Large application with multiple teams working on different features simultaneously.
- Independent scaling required.
- Continuous deployment without lockstep release.
- Technology diversity justified.
- High availability where one service failure must not take down the product.

## Skip If (ANY kills it)

- Single team / early-stage startup.
- Domain not yet stable — premature service boundaries are costly.
- Team lacks distributed-systems experience.
- ACID across multiple business entities — sagas add significant complexity.
- Tight latency budget — each hop adds round-trip time.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bounded-context map | Markdown | domain expert |
| Per-service data ownership table | spreadsheet | team |
| Transport policy (HTTP/gRPC/async) | ADR | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[domain-driven-design]] | Bounded contexts from DDD are the service boundaries |
| [[cap-pacelc-walkthrough]] | Each service's data store is chosen with CAP/PACELC explicit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure | ~800 |
| `content/05-examples.xml` | medium | One fully-worked example matching the output schema | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-services` | sonnet | Map bounded contexts to services + owners. |
| `design-transports` | sonnet | Pick HTTP vs gRPC vs async per interaction. |
| `author-failure-modes` | opus | Cross-service synthesis on circuit breakers + sagas. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-main.py` | FastAPI service skeleton with circuit-breaker import + DB ownership. |
| `templates/circuit-breaker.py` | Circuit breaker (CLOSED → OPEN → HALF_OPEN → CLOSED) for inter-service calls. |
| `templates/message-bus.py` | Async message bus for inter-service events (publish + subscribe). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-microservices-design.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[domain-driven-design]]
- [[event-sourcing-implementation]]
- [[cap-pacelc-walkthrough]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates microservices on team count, scaling asymmetry, and ops maturity; otherwise modular monolith is the better default.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/service-main.py`

```python
"""
from fastapi import FastAPI
from .infra.circuit_breaker import CircuitBreaker
from .infra.db import owned_db_session

app = FastAPI(title="orders-service")

_payment_breaker = CircuitBreaker(failure_threshold=5, reset_after_sec=30)


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    async with owned_db_session() as db:
        # only this service writes to this DB
        return await db.fetch_one("SELECT id, status FROM orders WHERE id = $1", order_id)


@app.post("/orders/{order_id}/charge")
async def charge(order_id: str):
    return await _payment_breaker.call(_charge_payment, order_id)


async def _charge_payment(order_id: str):
    # HTTP call to payments service; never import payments code directly
    ...
```

### `templates/circuit-breaker.py`

```python
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


class State(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_after_sec: int = 30) -> None:
        self.state = State.CLOSED
        self.failures = 0
        self.opened_at: datetime | None = None
        self.failure_threshold = failure_threshold
        self.reset_after = timedelta(seconds=reset_after_sec)

    async def call(self, fn: Callable[..., Awaitable[T]], *args, **kw) -> T:
        if self.state == State.OPEN:
            if self.opened_at and datetime.utcnow() - self.opened_at >= self.reset_after:
                self.state = State.HALF_OPEN
            else:
                raise RuntimeError("circuit open")
        try:
            result = await fn(*args, **kw)
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.state = State.OPEN
                self.opened_at = datetime.utcnow()
            raise
        else:
            self.failures = 0
            self.state = State.CLOSED
            return result
```

### `templates/message-bus.py`

```python
"""
from typing import Awaitable, Callable, Dict, List


Handler = Callable[[dict], Awaitable[None]]


class MessageBus:
    def __init__(self) -> None:
        self._subs: Dict[str, List[Handler]] = {}

    def subscribe(self, topic: str, handler: Handler) -> None:
        self._subs.setdefault(topic, []).append(handler)

    async def publish(self, topic: str, payload: dict) -> None:
        for h in self._subs.get(topic, []):
            await h(payload)
```
