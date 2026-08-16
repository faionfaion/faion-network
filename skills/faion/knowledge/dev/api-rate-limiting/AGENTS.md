# API Rate Limiting

## Summary

**One-sentence:** Designs a per-key rate-limit policy with sliding-window or token-bucket algorithm, 429 envelope (RFC 7807 + Retry-After), and per-tier quotas keyed off the auth scheme.

**One-paragraph:** Rate limiting that fires too late causes outages; firing too early kills legitimate clients. This methodology designs a rate-limit policy keyed off the AUTH-* artefact (token / user / api-key), picks algorithm (sliding-window for fairness, token-bucket for burst tolerance), sets per-tier quotas, and wires a 429 response with RFC 7807 envelope + Retry-After. Output: rate-limit policy + per-tier table + k6 verification script.

**Ефективно для:**

- Solo dev who got a $400 surprise bill from a runaway client.
- Public API where free / paid / partner tiers need different quotas.
- Adding burst tolerance for a billing endpoint hit at hour boundaries.
- Wiring Retry-After header so well-behaved clients back off automatically.

## Applies If (ALL must hold)

- API has identifiable callers (per AUTH-* key).
- Storage available for the limiter (Redis / Valkey / in-memory at small scale).
- Author has authority to set quota policy.

## Skip If (ANY kills it)

- Internal-only RPC behind a service mesh (mesh handles rate-limiting).
- Public read-only endpoint where CDN absorbs traffic.
- Bot-detection layer (separate methodology).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Auth artefact | AUTH-* spec_id | api-authentication |
| Caller-tier inventory | free / paid / partner / internal | PM |
| Redis or Valkey | connection string | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-authentication]] | Source of the limiter key (token / user / api-key). |
| [[api-error-handling]] | 429 envelope reuses the RFC 7807 shape. |

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
| `api_rate_limiting_draft` | sonnet | Bounded synthesis. |
| `api_rate_limiting_validate` | haiku | Mechanical schema check. |
| `api_rate_limiting_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sliding_window.py` | Stdlib sliding-window limiter keyed on auth identity |
| `templates/k6-rate-limit-check.js` | k6 load script that verifies 429 + Retry-After at burst boundary |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-rate-limiting artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-rate-limiting artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-rate-limiting.py` | Validate api-rate-limiting artefact against schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[caching-strategy]]
- [[api-authentication]]
- [[api-error-handling]]
- [[api-rest-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/sliding_window.py`

```python
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
```

### `templates/k6-rate-limit-check.js`

```javascript
 */
// k6-rate-limit-check.js — verify rate limit headers and 429 boundary behavior.
// Usage: k6 run -e BASE=https://api.example.com -e TOKEN=your_token k6-rate-limit-check.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = { vus: 5, duration: '90s' };

export default function () {
  const r = http.get(`${__ENV.BASE}/api/search?q=hello`, {
    headers: { Authorization: `Bearer ${__ENV.TOKEN}` },
    tags: { name: 'search' },
  });
  check(r, {
    'has RateLimit-Limit header': (x) =>
      !!x.headers['X-Ratelimit-Limit'] || !!x.headers['Ratelimit-Limit'],
    'on 429 has Retry-After': (x) =>
      x.status !== 429 || !!x.headers['Retry-After'],
    'no 5xx': (x) => x.status < 500,
  });
  sleep(0.1);
}
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-rate-limiting.json",
  "type": "object",
  "required": [
    "policy_id",
    "algorithm",
    "key_source",
    "tiers",
    "envelope_type_uri"
  ],
  "properties": {
    "policy_id": {
      "type": "string",
      "pattern": "^RL-[A-Z0-9-]{2,40}$"
    },
    "algorithm": {
      "type": "string",
      "enum": [
        "sliding-window",
        "token-bucket",
        "fixed-window",
        "leaky-bucket"
      ]
    },
    "key_source": {
      "type": "string",
      "enum": [
        "jwt-sub",
        "session-uid",
        "api-key-id",
        "oauth-client-id"
      ]
    },
    "tiers": {
      "type": "object",
      "minProperties": 2,
      "additionalProperties": {
        "type": "object",
        "required": [
          "per_second",
          "per_minute",
          "per_hour"
        ],
        "properties": {
          "per_second": {
            "type": "integer",
            "minimum": 1
          },
          "per_minute": {
            "type": "integer",
            "minimum": 1
          },
          "per_hour": {
            "type": "integer",
            "minimum": 1
          }
        }
      }
    },
    "envelope_type_uri": {
      "type": "string",
      "format": "uri"
    },
    "metrics_emitted": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "policy_id": "RL-PUBLIC-API",
  "algorithm": "sliding-window",
  "key_source": "jwt-sub",
  "tiers": {
    "free": {
      "per_second": 5,
      "per_minute": 60,
      "per_hour": 1000
    },
    "paid": {
      "per_second": 20,
      "per_minute": 600,
      "per_hour": 20000
    },
    "partner": {
      "per_second": 50,
      "per_minute": 1500,
      "per_hour": 60000
    }
  },
  "envelope_type_uri": "https://api.example.com/errors/rate-limited",
  "metrics_emitted": [
    "rate_limit_hits_total",
    "rate_limit_rejected_total",
    "rate_limit_latency_ms"
  ]
}
```
