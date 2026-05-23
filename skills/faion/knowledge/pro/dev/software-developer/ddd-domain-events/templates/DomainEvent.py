# purpose: frozen domain-event record with required metadata
# consumes: aggregate state at the moment of the command
# produces: immutable event for collection + dispatch
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~150 tokens when loaded as reference

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
