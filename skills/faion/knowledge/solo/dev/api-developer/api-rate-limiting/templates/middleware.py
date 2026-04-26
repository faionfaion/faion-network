# FastAPI rate-limit middleware with standard headers and 429 response.
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Inject a rate limiter instance (SlidingWindowRateLimiter or TokenBucketRateLimiter)
# rate_limiter = SlidingWindowRateLimiter(limit=100, window_seconds=3600, redis_client=redis)

RATE_LIMITS: dict[str, dict] = {
    "/api/search": {"limit": 10, "window": 60},
    "/api/export": {"limit": 5, "window": 3600},
}
DEFAULT_LIMIT = 100
DEFAULT_WINDOW = 3600


def get_user_id(request: Request) -> str:
    # Extract from JWT or API key; fall back to IP
    return request.headers.get("X-User-Id", request.client.host if request.client else "anon")


def add_rate_limit_headers(response: JSONResponse, limit: int, remaining: int, window: int) -> None:
    reset_at = int(time.time()) + window
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset_at)


def build_rate_limit_middleware(app: FastAPI, rate_limiter) -> None:
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        user_id = get_user_id(request)
        endpoint_cfg = RATE_LIMITS.get(request.url.path, {"limit": DEFAULT_LIMIT, "window": DEFAULT_WINDOW})
        limit = endpoint_cfg["limit"]
        window = endpoint_cfg["window"]
        key = f"rl:{user_id}:{request.url.path}"

        allowed = await rate_limiter.is_allowed(key)
        remaining = await rate_limiter.get_remaining(key)

        if not allowed:
            response = JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests",
                        "retryAfter": window,
                        "limit": limit,
                        "window": f"{window}s",
                    }
                },
                headers={"Retry-After": str(window)},
            )
            add_rate_limit_headers(response, limit, 0, window)
            return response

        response = await call_next(request)
        add_rate_limit_headers(response, limit, remaining, window)
        return response
