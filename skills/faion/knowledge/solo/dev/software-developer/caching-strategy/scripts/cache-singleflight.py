#!/usr/bin/env python3
"""cache-singleflight.py — Async cache-aside with thundering-herd protection.

On cache miss, only one coroutine fetches from the origin; others poll until
the result is available. Uses Redis NX SET as a distributed mutex.

Usage:
    sf = CacheSingleflight(redis_client, ttl=600)
    user = await sf.get_or_set("user:123", lambda: db.fetch_user(123))
"""
import asyncio
import json

import redis.asyncio as aioredis


class CacheSingleflight:
    def __init__(self, redis: aioredis.Redis, ttl: int = 600, lock_ttl: int = 30):
        self.r = redis
        self.ttl = ttl
        self.lock_ttl = lock_ttl

    async def get_or_set(self, key: str, loader):
        """Return cached value or load it; coalesce concurrent misses."""
        cached = await self.r.get(key)
        if cached is not None:
            return json.loads(cached)

        lock_key = f"lock:{key}"
        # NX SET: only one winner acquires the lock
        won = await self.r.set(lock_key, "1", nx=True, ex=self.lock_ttl)
        if won:
            try:
                value = await loader()
                await self.r.set(key, json.dumps(value), ex=self.ttl)
                return value
            finally:
                await self.r.delete(lock_key)
        else:
            # Losers poll with bounded retries (50 × 50 ms = 2.5 s max)
            for _ in range(50):
                await asyncio.sleep(0.05)
                cached = await self.r.get(key)
                if cached is not None:
                    return json.loads(cached)
            # Fallback: winner may have crashed; load independently
            return await loader()
