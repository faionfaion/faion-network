# purpose: Outbox table + relay scaffolding for broker-bound events
# consumes: collected aggregate events + DB session
# produces: outbox rows + broker publication
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~300 tokens when loaded as reference

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
