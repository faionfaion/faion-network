# purpose: Template helper for API Rate Limiting (rate_limiter.py).
# consumes: see content/02-output-contract.xml inputs for api-rate-limiting
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# SlidingWindowRateLimiter and TokenBucketRateLimiter with Redis backend.
import time
from typing import Any


class SlidingWindowRateLimiter:
    """Sliding window via Redis sorted set — no boundary burst problem."""

    def __init__(self, limit: int, window_seconds: int, redis_client: Any):
        self.limit = limit
        self.window = window_seconds
        self.redis = redis_client

    async def is_allowed(self, key: str) -> bool:
        now = time.time()
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, now - self.window)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, self.window)
        _, _, count, _ = await pipe.execute()
        return count <= self.limit

    async def get_remaining(self, key: str) -> int:
        now = time.time()
        count = await self.redis.zcount(key, now - self.window, now)
        return max(0, self.limit - count)


class TokenBucketRateLimiter:
    """Token bucket — allows controlled burst capacity."""

    def __init__(self, bucket_size: int, refill_rate: float):
        self.bucket_size = bucket_size
        self.refill_rate = refill_rate  # tokens per second
        self.buckets: dict[str, dict] = {}

    def is_allowed(self, key: str, tokens: int = 1) -> bool:
        now = time.time()
        bucket = self.buckets.get(key, {"tokens": self.bucket_size, "last_refill": now})
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(
            self.bucket_size,
            bucket["tokens"] + elapsed * self.refill_rate,
        )
        bucket["last_refill"] = now
        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            self.buckets[key] = bucket
            return True
        return False
