# Caching Strategy

## Summary

**One-sentence:** Picks one of four canonical cache patterns (cache-aside, write-through, write-behind, read-through), sizes the TTL + key strategy, and emits an invalidation contract with measurable hit-rate target.

**One-paragraph:** Caches solve latency but introduce three new problems: staleness, stampedes, and key collisions. This methodology picks one of four patterns based on read/write ratio and consistency tolerance, sizes per-key TTL with jitter, declares an explicit invalidation contract (publish event / write-through / TTL-only), adds single-flight protection against stampedes, and sets a measurable hit-rate target with an alert below the floor.

**Ефективно для:**

- Solo dev adding Redis in front of a hot endpoint that does 12k QPS.
- Replacing a write-through that turned every write into a P0 outage when Redis blipped.
- Adding single-flight to stop thundering-herd on cache-miss for a popular key.
- Setting an invalidation contract so other services know how to flush on data change.

## Applies If (ALL must hold)

- Hot path has a clear read/write ratio (&gt;5:1 reads).
- Cache store available (Redis / Valkey / Memcached / in-memory).
- Stale-tolerance budget is known (e.g. 30s acceptable, 5min not).
- Author has authority to ship cache + invalidation on the same change.

## Skip If (ANY kills it)

- Pure write workload (cache cost outweighs).
- Hard real-time consistency requirements (e.g. payment authorisation).
- Endpoint with &lt;10 RPS where DB round-trips are fine.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Endpoint + read/write ratio | QPS sample | APM |
| Source-of-truth data store | Postgres / etc. | platform |
| Cache store | Redis / Valkey | platform |
| Stale-tolerance SLA | seconds | PM / architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-rate-limiting]] | Cache fronts the same endpoints; both share metrics. |
| [[observability-architecture]] | Hit-rate + p95 alerts cross-reference. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `caching_strategy_draft` | sonnet | Bounded synthesis. |
| `caching_strategy_validate` | haiku | Mechanical schema check. |
| `caching_strategy_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cache-aside.py` | Stdlib cache-aside helper with jittered TTL + single-flight |
| `templates/cache-singleflight.py` | Async single-flight skeleton with Redis NX-SET mutex against thundering herd |
| `templates/output-schema.json` | JSON Schema (draft-07) for the caching-strategy artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in caching-strategy artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-strategy.py` | Validate caching-strategy artefact against schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-rate-limiting]]
- [[observability-architecture]]
- [[database-design]]
- [[api-rest-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cache-aside.py`

```python
"""cache-aside.py — Cache-aside decorator backed by Redis with TTL, key builder, and invalidation.

Usage:
    @cache_aside("user", ttl=1800, key_builder=lambda user_id: user_id)
    def get_user(user_id: str) -> dict:
        return db.users.find_one({"_id": user_id})

    # Explicit invalidation after write:
    get_user.invalidate(user_id)
"""
import hashlib
import json
from functools import wraps

import redis

_redis: redis.Redis = redis.Redis(host="localhost", port=6379, decode_responses=True)


def cache_aside(key_prefix: str, ttl: int = 3600, key_builder=None):
    """Decorator: check Redis first; on miss load from function, cache result."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key_builder:
                cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
            else:
                key_data = f"{args}:{sorted(kwargs.items())}"
                key_hash = hashlib.md5(key_data.encode()).hexdigest()[:12]
                cache_key = f"{key_prefix}:{key_hash}"

            cached = _redis.get(cache_key)
            if cached is not None:
                return json.loads(cached)

            result = func(*args, **kwargs)
            if result is not None:
                _redis.setex(cache_key, ttl, json.dumps(result))
            else:
                # Negative cache with shorter TTL to prevent DB hammering
                _redis.setex(cache_key, min(ttl, 60), json.dumps(None))
            return result

        def invalidate(*args, **kwargs):
            if key_builder:
                cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
                _redis.delete(cache_key)
            else:
                # Cannot compute key without args — caller must supply them
                raise ValueError("Provide key_builder to use .invalidate()")

        wrapper.invalidate = invalidate
        return wrapper
    return decorator
```

### `templates/cache-singleflight.py`

```python
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
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/caching-strategy.json",
  "type": "object",
  "required": [
    "strategy_id",
    "pattern",
    "ttl_seconds_base",
    "ttl_jitter_pct",
    "invalidation",
    "single_flight",
    "hit_rate_target"
  ],
  "properties": {
    "strategy_id": {
      "type": "string",
      "pattern": "^CACHE-[A-Z0-9-]{2,40}$"
    },
    "pattern": {
      "type": "string",
      "enum": [
        "cache-aside",
        "read-through",
        "write-through",
        "write-behind"
      ]
    },
    "ttl_seconds_base": {
      "type": "integer",
      "minimum": 1,
      "maximum": 86400
    },
    "ttl_jitter_pct": {
      "type": "integer",
      "minimum": 5,
      "maximum": 50
    },
    "invalidation": {
      "type": "object",
      "required": [
        "mode"
      ],
      "properties": {
        "mode": {
          "type": "string",
          "enum": [
            "ttl-only",
            "write-through",
            "pubsub-event"
          ]
        }
      }
    },
    "single_flight": {
      "type": "boolean"
    },
    "hit_rate_target": {
      "type": "number",
      "minimum": 0.5,
      "maximum": 1.0
    },
    "store": {
      "type": "string",
      "enum": [
        "redis",
        "valkey",
        "memcached",
        "in-memory",
        "cdn"
      ]
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "strategy_id": "CACHE-PRICING-GET",
  "pattern": "cache-aside",
  "ttl_seconds_base": 300,
  "ttl_jitter_pct": 20,
  "invalidation": {
    "mode": "pubsub-event",
    "channel": "pricing-changes"
  },
  "single_flight": true,
  "hit_rate_target": 0.85,
  "store": "redis"
}
```
