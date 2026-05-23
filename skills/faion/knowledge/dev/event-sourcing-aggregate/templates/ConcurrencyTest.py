# purpose: optimistic-concurrency clash test for the ES aggregate
# consumes: OrderRepository + in-memory event store
# produces: pytest test asserting ConcurrencyError
# depends-on: content/01-core-rules.xml, templates/Repository.py
# token-budget-impact: ~250 tokens when loaded as reference

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
