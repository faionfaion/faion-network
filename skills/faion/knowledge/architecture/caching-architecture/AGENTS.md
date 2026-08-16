# Caching Architecture

## Summary

**One-sentence:** Design multi-layer caching (browser → CDN → API gateway → application → database) using the correct pattern per data type: cache-aside, read-through, write-through, write-behind, or write-around.

**One-paragraph:** Caching architecture is a contract between layers about who reads, who writes, who invalidates, and what TTL applies. Output is a per-data-class caching policy document plus a Redis/CDN config that implements it. Wrong pattern choice creates either thundering herds (cache-aside without single-flight) or stale data (write-behind without idempotency).

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- At least one read-heavy endpoint with p95 latency above the SLO budget.
- Database costs dominated by read traffic, not writes.
- Data classes have distinguishable freshness requirements (real-time vs minutes vs hours).

## Skip If (ANY kills it)

- Write-heavy workload with cache hit rate < 30%.
- Strict consistency required end-to-end (cache adds risk without latency win).
- Prototype with no SLO commitments.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-endpoint RPS + latency profile | table | observability backend |
| Per-data-class freshness budget | table | PM/architect |
| Cache substrate (Redis/Memcached/CDN) | name + version | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/api-gateway-patterns` | Gateway is one cache layer. |
| `solo/dev/software-architect/database-selection` | DB choice influences cache pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip-this-methodology fallback | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for the caching policy + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: profile → classify → pick pattern → TTL → invalidation → load test | ~900 |
| `content/05-examples.xml` | medium | Worked example: product detail cache-aside + checkout no-cache | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-data` | sonnet | Per-endpoint data class assignment. |
| `pick-pattern` | sonnet | Per-data-class pattern selection. |
| `audit-cross-layer` | opus | Detect inconsistent TTLs across layers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/caching-policy.md.j2` | Per-data-class caching policy with pattern + TTL + invalidation rule. |
| `templates/caching-policy.md` | Per-data-class caching policy with pattern + TTL + invalidation rule. Generated from `templates/caching-policy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/redis-config.conf` | Production Redis standalone config: maxmemory + eviction policy + bind + auth. |
| `templates/cache-service.py` | Python cache-service skeleton: get-or-set + stampede protection + tag invalidation. |
| `templates/django-cache-settings.py` | Django `CACHES` settings block wired to Redis with per-view + low-level patterns. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-architecture.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[api-gateway-patterns]]
- [[database-selection]]
- [[data-modeling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/redis-config.conf`

```conf
# redis-config.conf — production Redis standalone (pure cache, no persistence)
# Tune: maxmemory, maxmemory-policy, bind, requirepass

# ---- Network ---------------------------------------------------------------
bind 127.0.0.1
port 6379
tcp-keepalive 60
timeout 0

# ---- Memory ----------------------------------------------------------------
# Set to 75-80% of available RAM, leaving headroom for OS and fork overhead.
maxmemory 2gb

# allkeys-lru:  evict any key using LRU approximation (general purpose)
# allkeys-lfu:  evict least-frequently-used (better for hot-key workloads)
# volatile-ttl: evict keys with TTL, prefer soonest-to-expire
# noeviction:   return OOM errors instead of evicting (NEVER use for a cache)
maxmemory-policy allkeys-lru

# Approximation sample size — 10 is balanced; raise to 20 for better accuracy
# at the cost of CPU on each eviction decision.
maxmemory-samples 10

# ---- Persistence (disabled for pure cache) ---------------------------------
save ""
appendonly no

# ---- Logging ---------------------------------------------------------------
loglevel notice
logfile ""

# ---- Performance -----------------------------------------------------------
# Max simultaneous clients
maxclients 10000

# Slow log threshold in microseconds (10ms default)
slowlog-log-slower-than 10000
slowlog-max-len 128

# ---- Security --------------------------------------------------------------
# Uncomment and set a strong password in production.
# requirepass your-strong-password-here

# Disable dangerous commands in production environments.
# rename-command FLUSHALL ""
# rename-command FLUSHDB ""
# rename-command DEBUG ""

# ---- TLS (optional) --------------------------------------------------------
# tls-port 6380
# tls-cert-file /etc/redis/tls/redis.crt
# tls-key-file /etc/redis/tls/redis.key
# tls-ca-cert-file /etc/redis/tls/ca.crt
# tls-auth-clients yes

# ---- Active Memory Defragmentation -----------------------------------------
activedefrag yes
active-defrag-ignore-bytes 100mb
active-defrag-threshold-lower 10
active-defrag-threshold-upper 100
```

### `templates/cache-service.py`

```python
"""
CacheService — generic async cache wrapper with get/set, get-or-set-with-lock,
XFetch probabilistic early expiration (stampede prevention), and pattern invalidation.

Dependencies: redis.asyncio (redis-py >= 4.2), Python >= 3.11
"""

from __future__ import annotations

import asyncio
import json
import math
import random
import time
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

import redis.asyncio as aioredis

T = TypeVar("T")

# Sentinel used to distinguish "key not found" from None values
_MISS = object()


class CacheService:
    def __init__(
        self,
        client: aioredis.Redis,
        key_prefix: str = "",
        default_ttl: int = 300,
    ) -> None:
        self._client = client
        self._prefix = key_prefix
        self._default_ttl = default_ttl
        # Single-flight: collapse concurrent misses for the same key
        self._inflight: dict[str, asyncio.Future[Any]] = {}
        self._inflight_lock = asyncio.Lock()

    # ---- low-level --------------------------------------------------------

    def _full_key(self, key: str) -> str:
        return f"{self._prefix}{key}" if self._prefix else key

    async def get(self, key: str) -> Any | None:
        raw = await self._client.get(self._full_key(key))
        if raw is None:
            return None
        return json.loads(raw)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        ttl = ttl if ttl is not None else self._default_ttl
        # Add ±10% jitter to prevent synchronized expiry storms
        jittered = int(ttl * (1 + random.uniform(-0.1, 0.1)))
        await self._client.set(
            self._full_key(key),
            json.dumps(value),
            ex=jittered,
        )

    async def delete(self, key: str) -> None:
        await self._client.delete(self._full_key(key))

    async def invalidate_pattern(self, pattern: str) -> int:
        """Delete all keys matching a glob pattern. Use sparingly — SCAN is O(N)."""
        full_pattern = self._full_key(pattern)
        deleted = 0
        async for batch in self._client.scan_iter(full_pattern, count=100):
            if batch:
                deleted += await self._client.delete(*batch)
        return deleted

    # ---- single-flight get-or-set -----------------------------------------

    async def get_or_set(
        self,
        key: str,
        loader: Callable[[], Awaitable[T]],
        ttl: int | None = None,
    ) -> T:
        """
        Return cached value or call loader once (single-flight).
        Concurrent callers for the same key wait on the same Future.
        """
        cached = await self.get(key)
        if cached is not None:
            return cached  # type: ignore[return-value]

        async with self._inflight_lock:
            # Check again inside lock — another coroutine may have populated it
            cached = await self.get(key)
            if cached is not None:
                return cached  # type: ignore[return-value]

            existing = self._inflight.get(key)
            if existing is not None:
                owner = False
                fut = existing
            else:
                loop = asyncio.get_event_loop()
                fut = loop.create_future()
                self._inflight[key] = fut
                owner = True

        if owner:
            try:
                value = await loader()
                await self.set(key, value, ttl)
                fut.set_result(value)
            except Exception as exc:
                fut.set_exception(exc)
                raise
            finally:
                async with self._inflight_lock:
                    self._inflight.pop(key, None)
        else:
            value = await fut

        return value  # type: ignore[return-value]

    # ---- XFetch probabilistic early expiration ----------------------------

    async def get_xfetch(
        self,
        key: str,
        loader: Callable[[], Awaitable[T]],
        ttl: int | None = None,
        beta: float = 1.0,
    ) -> T:
        """
        XFetch: probabilistic early recomputation to prevent stampedes.
        Workers independently decide whether to recompute based on remaining TTL
        and the time cost of the last recomputation. beta=1.0 is the standard value;
        increase to recompute more eagerly.

        Reference: Vattani et al. "Optimal Probabilistic Cache Stampede Prevention"
        """
        ttl = ttl if ttl is not None else self._default_ttl
        full_key = self._full_key(key)
        meta_key = f"{full_key}:_xfetch_delta"

        raw = await self._client.get(full_key)
        delta_raw = await self._client.get(meta_key)
        delta = float(delta_raw) if delta_raw else 0.0

        now = time.monotonic()
        remaining_ttl = await self._client.ttl(full_key)

        should_recompute = (
            raw is None
            or remaining_ttl < 0
            or (now - delta * beta * math.log(random.random())) >= (now + remaining_ttl - ttl)
        )

        if not should_recompute and raw is not None:
            return json.loads(raw)  # type: ignore[return-value]

        start = time.monotonic()
        value = await loader()
        elapsed = time.monotonic() - start

        await self._client.set(full_key, json.dumps(value), ex=ttl)
        await self._client.set(meta_key, str(elapsed), ex=ttl)
        return value  # type: ignore[return-value]
```

### `templates/django-cache-settings.py`

```python
"""
django-cache-settings.py — Django CACHES settings for default + session caches
using django-redis backend.

Requires: django-redis >= 5.0, Django >= 4.0
Install:  pip install django-redis

Place this in settings.py (or settings/production.py).
"""

import os

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
CACHE_KEY_PREFIX = os.environ.get("CACHE_KEY_PREFIX", "prod")

CACHES = {
    # ---- Default application cache -----------------------------------------
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 300,  # seconds; None = no expiry (use with caution)
        "KEY_PREFIX": CACHE_KEY_PREFIX,  # namespaces keys by env
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            # Connection pool: shared across threads in the same process
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "socket_connect_timeout": 1,   # seconds
                "socket_timeout": 1,            # seconds
            },
            # Ignore cache backend exceptions (return None on Redis error)
            # Set False in development to surface Redis issues early.
            "IGNORE_EXCEPTIONS": True,
            # Compress values > 1KB (requires python-lz4 or similar)
            # "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
        },
    },
    # ---- Session cache (separate DB index to allow selective flush) ---------
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_SESSION_URL", "redis://127.0.0.1:6379/1"),
        "TIMEOUT": 86400,  # 24h session TTL
        "KEY_PREFIX": f"{CACHE_KEY_PREFIX}:session",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": False,  # Session failures should surface
        },
    },
}

# Use Redis for Django sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


# ---------------------------------------------------------------------------
# Usage examples in views / services
# ---------------------------------------------------------------------------
#
# from django.core.cache import cache
#
# # Simple get/set
# user = cache.get(f"user:{user_id}")
# if user is None:
#     user = User.objects.get(pk=user_id)
#     cache.set(f"user:{user_id}", user, timeout=300)
#
# # get_or_set (atomic in Django >= 4.0)
# user = cache.get_or_set(f"user:{user_id}", lambda: User.objects.get(pk=user_id), 300)
#
# # Decorator: cache entire view for 5 minutes
# from django.views.decorators.cache import cache_page
#
# @cache_page(60 * 5)
# def product_list(request):
#     ...
#
# # Invalidate a key
# cache.delete(f"user:{user_id}")
#
# # Invalidate by pattern (django-redis specific, use sparingly)
# from django_redis import get_redis_connection
# con = get_redis_connection("default")
# keys = con.keys(f"{CACHE_KEY_PREFIX}:user:*")
# if keys:
#     con.delete(*keys)
```
