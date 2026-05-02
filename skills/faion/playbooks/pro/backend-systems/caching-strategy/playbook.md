---
name: caching-strategy
description: Build a 3-layer cache plan — Cloudflare CDN for static assets, Redis for sessions and hot DB queries, in-app LRU for hot lookup tables — with event-driven invalidation.
tier: pro
group: backend-systems
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working 3-layer caching architecture: Cloudflare CDN serving static assets with 1-year immutable headers, Redis caching sessions and hot DB queries with 5-minute TTL, and an in-process LRU cache for hot lookup tables. You will also have event-driven invalidation wired into every write path so stale data does not reach users.

## Prerequisites

- A Django or FastAPI backend with at least one read-heavy API endpoint.
- Redis running and reachable (local port 6379, or a managed instance such as Redis Cloud or AWS ElastiCache).
- A Cloudflare account with your domain proxied (orange cloud active).
- `redis-py` installed: `pip install redis`.
- `cachetools` installed: `pip install cachetools`.
- Familiarity with Python decorators and Django/FastAPI middleware.

## Steps

### Layer 1: Cloudflare CDN for static assets

1. Open Cloudflare dashboard → your domain → **Rules** → **Cache Rules** → **Create rule**.

2. Set match condition: `(http.request.uri.path matches "^\/(static|assets|media)\/")`.

3. Under **Cache** settings, set **Browser TTL** to `1 year` and **Edge Cache TTL** to `1 year`.

4. In your web server or Django `staticfiles` config, set `Cache-Control: public, max-age=31536000, immutable` on all static file responses. For Django with WhiteNoise:

```python
# settings.py
WHITENOISE_MAX_AGE = 31536000  # 1 year
WHITENOISE_IMMUTABLE_FILE_TEST = lambda path, url: url.startswith("/static/")
```

5. For API responses that are public and change on a known schedule (product catalog, public article list), add `Cache-Control: public, max-age=300, stale-while-revalidate=60` in the view:

```python
# FastAPI example — public product listing endpoint
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/api/products")
async def list_products(response: Response):
    response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=60"
    return await fetch_products_from_db()
```

6. For personalized responses (user profile, cart), always use `Cache-Control: private, max-age=0, must-revalidate` to prevent CDN from serving one user's data to another.

### Layer 2: Redis for sessions and hot DB queries

7. Initialize the Redis client once at app startup:

```python
# cache/redis_client.py
import redis
import os

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)
```

8. Implement the cache-aside pattern for hot DB queries. Use TTL with ±15% jitter to prevent synchronized expiry stampedes:

```python
# cache/patterns.py
import json
import secrets
from cache.redis_client import redis_client

BASE_TTL = {
    "user_profile":    300,    # 5 minutes
    "product_detail":  300,    # 5 minutes
    "category_list":   3600,   # 1 hour
    "static_config":   86400,  # 24 hours
}

def _ttl_with_jitter(base: int, jitter_pct: float = 0.15) -> int:
    r = int(base * jitter_pct)
    offset = secrets.randbelow(2 * r + 1) - r
    return max(1, base + offset)

def cache_aside(cache_key: str, loader, ttl: int) -> dict:
    """Read from Redis; on miss, load from DB and write back."""
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    data = loader()
    if data is not None:
        redis_client.setex(cache_key, _ttl_with_jitter(ttl), json.dumps(data))
    return data

# Usage in a view
def get_user_profile(user_id: str) -> dict:
    return cache_aside(
        cache_key=f"user:profile:{user_id}",
        loader=lambda: User.objects.filter(pk=user_id).values().first(),
        ttl=BASE_TTL["user_profile"],
    )
```

9. For Django sessions, switch the session backend to Redis:

```python
# settings.py
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "socket_connect_timeout": 2,
            "socket_timeout": 2,
        },
    }
}
```

### Layer 3: In-process LRU for hot lookup tables

10. Use `cachetools.TTLCache` with a `threading.Lock` for lookup tables that are read on every request (permission tables, feature flags, rate-limit config). Keep values ≤1KB per entry in L1; store larger objects in Redis only:

```python
# cache/app_cache.py
import threading
from cachetools import TTLCache, cached

_permission_cache = TTLCache(maxsize=2000, ttl=120)
_permission_lock = threading.Lock()

@cached(_permission_cache, lock=_permission_lock)
def get_user_permissions(user_id: int) -> frozenset:
    """L1 cached: returns frozenset of permission codenames for user_id."""
    from django.contrib.auth.models import User
    user = User.objects.prefetch_related("user_permissions", "groups__permissions").get(pk=user_id)
    return frozenset(
        perm.codename
        for perm in user.user_permissions.all()
    ) | frozenset(
        perm.codename
        for group in user.groups.all()
        for perm in group.permissions.all()
    )

def invalidate_user_permissions(user_id: int):
    """Call from the write path whenever roles or permissions change."""
    with _permission_lock:
        key = (user_id,)
        if key in _permission_cache:
            del _permission_cache[key]
```

### Event-driven cache invalidation

11. Wire invalidation into every write path that mutates a cached entity. Use a `CacheInvalidator` to keep invalidation co-located with writes:

```python
# cache/invalidator.py
import json
from cache.redis_client import redis_client
from cache.app_cache import invalidate_user_permissions

class CacheInvalidator:
    def invalidate_user(self, user_id: str):
        """Delete all cache entries for a user — call on profile update."""
        redis_client.delete(
            f"user:profile:{user_id}",
            f"user:settings:{user_id}",
        )
        invalidate_user_permissions(int(user_id))

    def invalidate_product(self, product_id: str, category_id: str = None):
        """Delete product cache and optionally its category listing."""
        keys = [f"product:detail:{product_id}"]
        if category_id:
            keys.append(f"category:products:{category_id}")
        redis_client.delete(*keys)

invalidator = CacheInvalidator()

# In your update views or service layer:
# def update_user_profile(user_id, data):
#     User.objects.filter(pk=user_id).update(**data)
#     invalidator.invalidate_user(user_id)
```

12. For Cloudflare CDN purge when a public API response changes (product goes out of stock, article published), use the Cloudflare API:

```python
# cache/cdn_purge.py
import httpx
import os

CF_ZONE_ID = os.getenv("CF_ZONE_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")

def purge_cloudflare_urls(urls: list[str]):
    """Purge specific Cloudflare cache entries by URL."""
    if not CF_ZONE_ID or not CF_API_TOKEN:
        return
    httpx.post(
        f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/purge_cache",
        headers={"Authorization": f"Bearer {CF_API_TOKEN}"},
        json={"files": urls},
        timeout=5,
    )
```

## Verify

Run the following sequence to confirm all three cache layers are active:

```bash
# 1. Verify Redis is reachable and accepting writes
redis-cli -h localhost -p 6379 ping
# Expected: PONG

# 2. Load a hot endpoint once (cache miss → DB query → Redis write)
curl -s -o /dev/null -w "%{time_total}" https://myapp.com/api/products/42
# Note the time (e.g. 0.12s)

# 3. Load again (should be a Redis hit)
curl -s -o /dev/null -w "%{time_total}" https://myapp.com/api/products/42
# Expected: significantly lower (e.g. 0.02s)

# 4. Verify the key exists in Redis with TTL
redis-cli -h localhost -p 6379 TTL "product:detail:42"
# Expected: integer between 1 and 300 (within jitter range)

# 5. Verify CDN caching on static assets
curl -sI https://myapp.com/static/main.abc123.css | grep -i cache-control
# Expected: cache-control: public, max-age=31536000, immutable

# 6. Verify CDN response is served from edge (not origin)
curl -sI https://myapp.com/static/main.abc123.css | grep -i cf-cache-status
# Expected: CF-Cache-Status: HIT
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `redis.exceptions.ConnectionError` on startup | Redis not running or wrong host/port | Run `redis-cli ping`; check `REDIS_HOST`/`REDIS_PORT` env vars; verify firewall allows port 6379 |
| Cache miss every request despite `setex` call | `decode_responses=True` but serializer returns bytes | Ensure `json.dumps(data)` produces a string, not bytes; check `redis_client` is initialized with `decode_responses=True` |
| `CF-Cache-Status: MISS` on every static asset | Cloudflare cache rule not matching path | Open Cloudflare dash → Cache Rules → test the URL in the rule tester; confirm orange-cloud proxy is active |
| Permission cache not cleared after role change | Invalidation not wired into admin save | Add `invalidator.invalidate_user(user_id)` to the `post_save` signal for `User` and `Group` models |
| `TTLCache` raising `KeyError` under concurrent load | Missing `threading.Lock` on `TTLCache` | Wrap every `TTLCache` instance with `lock=threading.Lock()` in the `@cached` decorator; see Step 10 |
| Thundering herd after mass TTL expiry | All keys set with identical TTL | Apply `_ttl_with_jitter()` to every `setex` call; see Step 8 |
| Stale product data after stock update | Invalidation only clears `product:detail:*` but CDN still serves cached API JSON | Call `purge_cloudflare_urls(["/api/products/42"])` from the write path; see Step 12 |

## Next

- `redis-cluster-ha` — scale Redis beyond a single node with Redis Cluster or Sentinel for HA in agency-scale deployments.
- `cdn-performance-audit` — measure CDN cache-hit ratio in Cloudflare Analytics and identify endpoints still missing `Cache-Control` headers.
- Review `caching-stampede-prevention` methodology under `pro/dev/backend-systems/` if you see origin load spikes during cache warm-up.

## References

- [knowledge/pro/dev/backend-systems/caching-in-memory](../../../knowledge/pro/dev/backend-systems/caching-in-memory) — TTLCache thread-safety rule and WarmableCache double-checked locking pattern directly backs Steps 10–11 for the L1 in-process layer.
- [knowledge/pro/dev/backend-systems/caching-invalidation](../../../knowledge/pro/dev/backend-systems/caching-invalidation) — event-based invalidation and tag-based Redis patterns underpin the CacheInvalidator in Steps 11–12; TTL jitter rule from this methodology backs Step 8.
- [knowledge/pro/dev/backend-systems/caching-http-headers](../../../knowledge/pro/dev/backend-systems/caching-http-headers) — `Cache-Control: public/private/immutable` directive rules and CDN edge caching decisions directly drive Steps 1–6 for Layer 1.
