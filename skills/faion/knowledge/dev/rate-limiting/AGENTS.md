# Rate Limiting

## Summary

**One-sentence:** Rate-limiting spec: algorithm (token bucket / fixed window / sliding log), key strategy (user / IP / tenant), storage (Redis), 429 response shape with Retry-After, and bypass list for health checks.

**One-paragraph:** Rate limiting fails when the algorithm is picked by intuition (per-minute counters reset cliffs), when the key is wrong (per-IP behind a NAT throttles a whole office), when the storage is unbounded (Redis OOMs on the limit keys themselves), and when the 429 response lacks Retry-After so clients hammer back instantly. This methodology produces a spec naming algorithm, key, storage backend with TTL, the 429 contract (status + Retry-After + RateLimit-Remaining headers), and a bypass list (health, metrics).

**Ефективно для:**

- API під DDoS / scraping - запровадити перші ліміти.
- Per-tenant ізоляція - один tenant не повинен валити інших.
- Login endpoint - захист від brute force.
- External API quota - дотримуватись upstream обмежень.
- Fair-use на free тарифі - cap на безкоштовних користувачів.

## Applies If (ALL must hold)

- Service exposes an HTTP API with public or multi-tenant traffic.
- Risk of abuse (scraping, brute force, runaway client) is non-zero.
- Redis or compatible in-memory store is available.
- Owner can sign off limit numbers per endpoint class.

## Skip If (ANY kills it)

- Service is internal-only behind authenticated VPN with trusted callers.
- Throughput SLO does not include fair-use constraints.
- Throttling at a sidecar (Envoy, nginx) covers the policy entirely.
- Project is a throwaway prototype with no production users.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Endpoint classification | table of endpoints with class (auth/read/write) | engineering |
| Limit budget | rps per class signed off by owner | product |
| Redis instance | host + ACL + maxmemory policy | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[nosql-patterns]] | Redis key namespace + TTL conventions reused for limit keys. |
| [[api-error-handling]] | 429 response shape inherits Problem+JSON pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: algorithm per class, key strategy, TTL on limit keys, 429+Retry-After, bypass list, fail-mode, burst documented | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step spec: classify, pick algorithm, pick key, wire storage, define 429 | ~900 |
| `content/05-examples.xml` | essential | Worked example for SaaS multi-tenant API | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-endpoints` | sonnet | Per-endpoint judgement on burst tolerance. |
| `pick-algorithm` | sonnet | Algorithm vs burst tradeoff per class. |
| `draft-redis-keys` | haiku | Mechanical naming + TTL. |
| `audit-bypass-list` | opus | Stakes high; bypassing too much defeats throttle, too little self-DoSes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate-limits.yaml` | Rate-limit policy YAML with per-class limits and bypass. |
| `templates/middleware.py` | Reference middleware sketch: token-bucket via Redis INCR + TTL. |
| `templates/sliding-window.py` | Redis ZSET-backed sliding window rate limiter with atomic Lua check-and-add. |
| `templates/k6-rl-probe.js` | k6 load-test probe verifying RateLimit-* headers and 429 + Retry-After. |
| `templates/_smoke-test.json` | Minimum viable rate-limit artefact for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rate-limiting.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[nosql-patterns]]
- [[api-error-handling]]
- [[security-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - traffic shape, key candidate, storage available, monitoring paths - onto a rule from `content/01-core-rules.xml`. Use it before wiring limits: it catches fixed-window cliff, per-IP NAT block, and missing health bypass upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rate-limits.yaml`

```yaml
version: 1
classes:
  - name: auth
    algorithm: token_bucket
    rps: 5
    burst: 10
  - name: read
    algorithm: sliding_window_counter
    rps: 100
    burst: 0
  - name: write
    algorithm: sliding_window_counter
    rps: 20
    burst: 0
key_strategy: user_id
storage:
  backend: redis
  ttl_seconds: 120
headers:
  retry_after: true
  ratelimit_remaining: true
fail_mode: open
bypass_paths:
  - /healthz
  - /metrics
```

### `templates/middleware.py`

```python
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
```

### `templates/sliding-window.py`

```python
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
```

### `templates/k6-rl-probe.js`

```javascript
// Usage: BASE=https://api.example.com TOKEN=xxx k6 run --vus 50 --duration 30s k6-rl-probe.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const URL   = __ENV.URL   || `${__ENV.BASE}/api/search`;
const TOKEN = __ENV.TOKEN || '';

export default function () {
  const res = http.get(URL, {
    headers: TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {},
  });

  check(res, {
    'has X-RateLimit-Limit header':     (r) => !!r.headers['X-Ratelimit-Limit'],
    'has X-RateLimit-Remaining header': (r) => !!r.headers['X-Ratelimit-Remaining'],
    '429 has Retry-After header':       (r) => r.status !== 429 || !!r.headers['Retry-After'],
    '429 body has retryAfter field':    (r) =>
      r.status !== 429 || r.json('error.retryAfter') !== null,
    'status is 200 or 429':             (r) => r.status === 200 || r.status === 429,
  });

  sleep(0.05);
}
```

### `templates/_smoke-test.json`

```json
{
  "classes": [
    {
      "name": "read",
      "algorithm": "sliding_window_counter",
      "rps": 100,
      "burst": 0
    }
  ],
  "key_strategy": "user_id",
  "storage": {
    "backend": "redis",
    "ttl_seconds": 60
  },
  "headers": {
    "retry_after": true,
    "ratelimit_remaining": true
  },
  "fail_mode": "open"
}
```
