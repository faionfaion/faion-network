"""sliding-window.py — Redis-backed sliding window rate limiter.

Stores request timestamps in a sorted set (ZSET) per key. On each check:
  1. Remove timestamps older than the window.
  2. Add current timestamp.
  3. Count total entries — if > limit, reject.

Uses a Lua script for atomic check-and-add to prevent race conditions.

Usage:
    limiter = SlidingWindowLimiter(redis_client, limit=100, window_seconds=60)
    allowed = await limiter.is_allowed("user:123")
"""
import time
from dataclasses import dataclass

import redis.asyncio as aioredis

_LUA_SCRIPT = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
redis.call('ZADD', key, now, now)
redis.call('EXPIRE', key, window)
local count = redis.call('ZCARD', key)
return count
"""


@dataclass
class RateLimitResult:
    allowed: bool
    count: int
    limit: int
    remaining: int


class SlidingWindowLimiter:
    def __init__(self, redis: aioredis.Redis, limit: int, window_seconds: int):
        self.r = redis
        self.limit = limit
        self.window = window_seconds
        self._script = self.r.register_script(_LUA_SCRIPT)

    async def check(self, key: str) -> RateLimitResult:
        now = time.time()
        count = int(await self._script(keys=[key], args=[now, self.window, self.limit]))
        allowed = count <= self.limit
        return RateLimitResult(
            allowed=allowed,
            count=count,
            limit=self.limit,
            remaining=max(0, self.limit - count),
        )

    async def is_allowed(self, key: str) -> bool:
        result = await self.check(key)
        return result.allowed
