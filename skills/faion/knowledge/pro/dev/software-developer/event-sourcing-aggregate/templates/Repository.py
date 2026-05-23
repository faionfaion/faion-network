# purpose: ES repository with expected_version semantics
# consumes: event-store client + aggregate.collect_pending_events
# produces: persistence boundary enforcing optimistic concurrency
# depends-on: content/01-core-rules.xml, templates/Aggregate.py
# token-budget-impact: ~200 tokens when loaded as reference

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
