# Caching Strategy

## Summary

Multi-level caching (CDN → app in-memory → Redis/Valkey → DB) with explicit pattern selection (cache-aside, write-through, write-behind, SWR) and mandatory per-key TTL, invalidation trigger, and hit-rate monitoring. Every cache layer requires a documented invalidation path and stampede protection for endpoints serving > 100 RPS.

## Why

Unbounded read traffic can saturate databases even when queries are well-tuned. Caching reduces latency and DB load, but only when hit rates are measured and staleness tolerance is explicitly decided. Without stampede protection (singleflight / SWR) a cache miss under load sends all concurrent requests to the DB simultaneously, reproducing the original problem.

## When To Use

- Read-heavy endpoints with bounded staleness tolerance (product catalog, user profile, settings).
- Expensive computations whose inputs repeat (LLM responses, image transforms, search aggregations).
- Static or near-static API responses behind a CDN or edge cache.
- Session storage, OAuth token cache, rate-limit counters — natural Redis fit.
- Aggregation/dashboard responses where 30-60 s freshness is acceptable.

## When NOT To Use

- Highly volatile data (live counts, current bid prices) where any staleness is unacceptable.
- Per-user data with no reuse pattern (expected hit ratio < 50% — wasted memory).
- Strong-consistency requirements (financial ledger, inventory hold).
- Small datasets that fit in app memory already (use a plain dict).
- Without a measurement plan — caching without hit-rate monitoring is dead weight.
- When cache invalidation logic is more complex than the underlying query.

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Cache-aside, write-through, write-behind patterns with rules and code examples. |
| `content/02-invalidation.xml` | TTL-based, event-based, version-based invalidation; HTTP ETag/Cache-Control directives. |
| `content/03-antipatterns.xml` | Stampede, stale data, memory pressure, hot key, pickle/RCE, async/sync client mix-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cache-aside.py` | Cache-aside decorator with Redis, TTL, key builder, and invalidation helper. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/cache-singleflight.py` | Async cache-aside with thundering-herd protection via Redis NX mutex. |
