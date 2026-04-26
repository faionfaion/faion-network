# API Rate Limiting

## Summary

Throttle API consumers using sliding window (fairness), fixed window (simplicity), or token bucket (burst control) algorithms. Every 429 response includes `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After` headers. Limits are tiered by plan; endpoints with expensive operations use tighter per-route limits. Redis backs distributed deployments.

## Why

Without rate limiting, a single misbehaving client can saturate server resources and degrade service for all users. Sliding window avoids the boundary spike problem of fixed window. Token bucket allows controlled bursting — ideal for bursty-but-fair use cases like search or export. Standard headers allow clients to back off gracefully without polling.

## When To Use

- Public or partner-facing APIs exposed to untrusted clients
- APIs with computationally expensive endpoints (search, export, AI inference)
- When adding tiered billing plans that correspond to different request quotas
- Distributed deployments where per-instance counters would give inconsistent limits

## When NOT To Use

- Internal service-to-service APIs within a trusted network — use circuit breakers instead
- CLI tools or scripts that run under a single authenticated identity with known call patterns
- Development/staging environments where rate limiting interferes with testing

## Content

| File | What's inside |
|------|---------------|
| `content/01-algorithms.xml` | Fixed window, sliding window (Redis sorted set), token bucket — code + trade-off notes |
| `content/02-implementation.xml` | FastAPI middleware pattern, tiered limits table, per-endpoint config, headers, 429 response shape |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate_limiter.py` | SlidingWindowRateLimiter + TokenBucketRateLimiter classes with Redis backend |
| `templates/middleware.py` | FastAPI rate-limit middleware with header injection and 429 response |
