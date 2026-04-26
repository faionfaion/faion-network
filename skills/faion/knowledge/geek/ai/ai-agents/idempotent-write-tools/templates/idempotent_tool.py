"""Reference idempotent write tool.

Contract:
- `idempotency_key` is REQUIRED and supplied by the agent (not generated here).
- Result is persisted in `key_store` for ttl_seconds; replays return stored result.
- Read tools never take the key — keep their schema clean.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Protocol


class KeyStore(Protocol):
    def get(self, key: str) -> Any | None: ...
    def set(self, key: str, value: Any, ttl_seconds: int) -> None: ...


@dataclass
class WriteResult:
    ok: bool
    data: dict
    replayed: bool = False


def idempotent_write(
    *,
    idempotency_key: str,
    payload: dict,
    perform: callable,        # pure side-effect callable
    store: KeyStore,
    ttl_seconds: int = 86400,
) -> WriteResult:
    if not idempotency_key:
        raise ValueError("idempotency_key is required for write tools")

    if hit := store.get(idempotency_key):
        return WriteResult(ok=True, data=hit, replayed=True)

    data = perform(payload)
    store.set(idempotency_key, data, ttl_seconds=ttl_seconds)
    return WriteResult(ok=True, data=data, replayed=False)
