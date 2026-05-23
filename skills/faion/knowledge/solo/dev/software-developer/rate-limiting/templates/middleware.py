"""purpose: Reference middleware sketch: token-bucket via Redis INCR + TTL.
consumes: see content/02-output-contract.xml inputs for rate-limiting
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml + content/04-procedure.xml
token-budget-impact: ~200-700 tokens when loaded as context"""

from typing import Awaitable, Callable

async def rate_limit(request, call_next: Callable[..., Awaitable], *, redis, policy):
    path = request.url.path
    if path in policy.bypass_paths:
        return await call_next(request)
    cls = classify(path, policy)
    key = f"ratelimit:{cls.name}:{actor_key(request, policy.key_strategy)}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, policy.storage.ttl_seconds)
    if count > cls.rps + cls.burst:
        return respond_429(cls)
    return await call_next(request)

def respond_429(cls):
    return {
        'status': 429,
        'headers': {'Retry-After': str(cls.window_seconds()), 'RateLimit-Limit': str(cls.rps), 'RateLimit-Remaining': '0'},
        'body': {'type': 'about:blank', 'title': 'Too Many Requests', 'status': 429, 'retry_after_seconds': cls.window_seconds()},
    }
