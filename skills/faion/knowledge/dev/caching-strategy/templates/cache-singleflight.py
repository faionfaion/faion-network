#!/usr/bin/env python3
# purpose: Single-flight primitive used inside cache-aside miss path
# consumes: key
# produces: single in-flight result shared across callers
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded
"""cache-singleflight.py — Async cache-aside with thundering-herd protection.

On cache miss, only one coroutine fetches from the origin; others poll until
the result is available. Uses Redis SET NX as a distributed mutex.

Usage:
    sf = CacheSingleflight(redis_client, ttl=600)
    user = await sf.get_or_set("user:123", lambda: db.fetch_user(123))

The lock carries an OWNER TOKEN and is released by a compare-and-delete
script. The first version released with a bare `DELETE lock_key` in `finally`,
and that is exactly wrong when the origin is slow: with a 1 s lock TTL and a
2 s load, the lock expires mid-load, a second caller wins a fresh lock, and
the first caller's `finally` then deletes the lock the SECOND caller holds. Two
loaders ran concurrently under a primitive whose only job is to prevent that.
Verified against a real Redis before this rewrite.
"""
import asyncio
import json
import uuid

import redis.asyncio as aioredis

# DEL only if the value is still our token. GET-then-DEL is two round trips
# and a race; one Lua call is atomic on the server.
_RELEASE_LUA = (
    "if redis.call('get', KEYS[1]) == ARGV[1] then "
    "return redis.call('del', KEYS[1]) end return 0"
)


class CacheSingleflight:
    def __init__(self, redis: aioredis.Redis, ttl: int = 600, lock_ttl: int = 30):
        # lock_ttl must exceed the slowest plausible loader; it is a crash
        # guard, not a timeout. A lock that expires under a live loader is the
        # failure this class exists to prevent.
        self.r = redis
        self.ttl = ttl
        self.lock_ttl = lock_ttl
        self._release = redis.register_script(_RELEASE_LUA)

    async def get_or_set(self, key: str, loader):
        """Return cached value or load it; coalesce concurrent misses."""
        cached = await self.r.get(key)
        if cached is not None:
            return json.loads(cached)

        lock_key = f"lock:{key}"
        token = uuid.uuid4().hex
        won = await self.r.set(lock_key, token, nx=True, ex=self.lock_ttl)
        if won:
            try:
                value = await loader()
                await self.r.set(key, json.dumps(value), ex=self.ttl)
                return value
            finally:
                await self._release(keys=[lock_key], args=[token])

        # Losers poll with bounded retries (50 x 50 ms = 2.5 s max)
        for _ in range(50):
            await asyncio.sleep(0.05)
            cached = await self.r.get(key)
            if cached is not None:
                return json.loads(cached)
        # Winner crashed or is slower than the poll budget: load independently.
        # Documented double-load path; raise lock_ttl and the poll budget
        # together if it fires in production.
        return await loader()
