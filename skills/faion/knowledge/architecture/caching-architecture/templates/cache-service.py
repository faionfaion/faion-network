# purpose: Reference cache service implementation (Python).
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a caching-architecture artefact validating against scripts/validate-caching-architecture.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
"""
CacheService — generic async cache wrapper with get/set, get-or-set-with-lock,
XFetch probabilistic early expiration (stampede prevention), and pattern invalidation.

Dependencies: redis.asyncio (redis-py >= 4.2), Python >= 3.11
"""

from __future__ import annotations

import asyncio
import json
import math
import random
import time
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

import redis.asyncio as aioredis

T = TypeVar("T")

# Sentinel used to distinguish "key not found" from None values
_MISS = object()


class CacheService:
    def __init__(
        self,
        client: aioredis.Redis,
        key_prefix: str = "",
        default_ttl: int = 300,
    ) -> None:
        self._client = client
        self._prefix = key_prefix
        self._default_ttl = default_ttl
        # Single-flight: collapse concurrent misses for the same key
        self._inflight: dict[str, asyncio.Future[Any]] = {}
        self._inflight_lock = asyncio.Lock()

    # ---- low-level --------------------------------------------------------

    def _full_key(self, key: str) -> str:
        return f"{self._prefix}{key}" if self._prefix else key

    async def get(self, key: str) -> Any | None:
        raw = await self._client.get(self._full_key(key))
        if raw is None:
            return None
        return json.loads(raw)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        ttl = ttl if ttl is not None else self._default_ttl
        # Add ±10% jitter to prevent synchronized expiry storms
        jittered = int(ttl * (1 + random.uniform(-0.1, 0.1)))
        await self._client.set(
            self._full_key(key),
            json.dumps(value),
            ex=jittered,
        )

    async def delete(self, key: str) -> None:
        await self._client.delete(self._full_key(key))

    async def invalidate_pattern(self, pattern: str) -> int:
        """Delete all keys matching a glob pattern. Use sparingly — SCAN is O(N)."""
        full_pattern = self._full_key(pattern)
        deleted = 0
        async for batch in self._client.scan_iter(full_pattern, count=100):
            if batch:
                deleted += await self._client.delete(*batch)
        return deleted

    # ---- single-flight get-or-set -----------------------------------------

    async def get_or_set(
        self,
        key: str,
        loader: Callable[[], Awaitable[T]],
        ttl: int | None = None,
    ) -> T:
        """
        Return cached value or call loader once (single-flight).
        Concurrent callers for the same key wait on the same Future.
        """
        cached = await self.get(key)
        if cached is not None:
            return cached  # type: ignore[return-value]

        async with self._inflight_lock:
            # Check again inside lock — another coroutine may have populated it
            cached = await self.get(key)
            if cached is not None:
                return cached  # type: ignore[return-value]

            existing = self._inflight.get(key)
            if existing is not None:
                owner = False
                fut = existing
            else:
                loop = asyncio.get_event_loop()
                fut = loop.create_future()
                self._inflight[key] = fut
                owner = True

        if owner:
            try:
                value = await loader()
                await self.set(key, value, ttl)
                fut.set_result(value)
            except Exception as exc:
                fut.set_exception(exc)
                raise
            finally:
                async with self._inflight_lock:
                    self._inflight.pop(key, None)
        else:
            value = await fut

        return value  # type: ignore[return-value]

    # ---- XFetch probabilistic early expiration ----------------------------

    async def get_xfetch(
        self,
        key: str,
        loader: Callable[[], Awaitable[T]],
        ttl: int | None = None,
        beta: float = 1.0,
    ) -> T:
        """
        XFetch: probabilistic early recomputation to prevent stampedes.
        Workers independently decide whether to recompute based on remaining TTL
        and the time cost of the last recomputation. beta=1.0 is the standard value;
        increase to recompute more eagerly.

        Reference: Vattani et al. "Optimal Probabilistic Cache Stampede Prevention"
        """
        ttl = ttl if ttl is not None else self._default_ttl
        full_key = self._full_key(key)
        meta_key = f"{full_key}:_xfetch_delta"

        raw = await self._client.get(full_key)
        delta_raw = await self._client.get(meta_key)
        delta = float(delta_raw) if delta_raw else 0.0

        now = time.monotonic()
        remaining_ttl = await self._client.ttl(full_key)

        should_recompute = (
            raw is None
            or remaining_ttl < 0
            or (now - delta * beta * math.log(random.random())) >= (now + remaining_ttl - ttl)
        )

        if not should_recompute and raw is not None:
            return json.loads(raw)  # type: ignore[return-value]

        start = time.monotonic()
        value = await loader()
        elapsed = time.monotonic() - start

        await self._client.set(full_key, json.dumps(value), ex=ttl)
        await self._client.set(meta_key, str(elapsed), ex=ttl)
        return value  # type: ignore[return-value]
