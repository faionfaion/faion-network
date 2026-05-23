# purpose: Stdlib sliding-window limiter keyed on auth identity
# consumes: Limiter key + tier config
# produces: allow / 429 + Retry-After
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~350 tokens when loaded
"""
sliding_window.py — Redis sliding-window rate limiter for FastAPI.

Usage: add RateLimitMiddleware to your FastAPI app.
Requires: redis>=5, fastapi
"""
import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis


class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int, redis_client: redis.Redis):
        self.limit = limit
        self.window = window_seconds
        self.redis = redis_client

    async def is_allowed(self, key: str) -> tuple[bool, int]:
        """Returns (allowed, current_count)."""
        now = time.time()
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, now - self.window)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, self.window)
        _, _, count, _ = await pipe.execute()
        return count <= self.limit, int(count)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: SlidingWindowRateLimiter):
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next):
        # Key by user_id if authenticated, else by IP
        user_id = getattr(request.state, "user_id", None)
        forwarded_for = request.headers.get("X-Forwarded-For")
        ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host
        key = f"ratelimit:{user_id or ip}"

        allowed, count = await self.limiter.is_allowed(key)
        reset_time = int(time.time()) + self.limiter.window
        headers = {
            "RateLimit-Limit": str(self.limiter.limit),
            "RateLimit-Remaining": str(max(0, self.limiter.limit - count)),
            "RateLimit-Reset": str(reset_time),
        }

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": {"code": "RATE_LIMIT_EXCEEDED",
                                   "message": "Too many requests",
                                   "retryAfter": self.limiter.window}},
                headers={"Retry-After": str(self.limiter.window), **headers},
            )

        response = await call_next(request)
        for k, v in headers.items():
            response.headers[k] = v
        return response
