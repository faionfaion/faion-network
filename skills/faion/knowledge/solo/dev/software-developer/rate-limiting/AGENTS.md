# Rate Limiting

## Summary

API protection via configurable per-key rate limiters (fixed window, sliding window, token bucket) backed by Redis/Valkey, with standard `X-RateLimit-*` / `Retry-After` response headers and a 429 JSON error body. Every deployment must use Redis — in-memory limiters break at > 1 replica. Sliding window or GCRA is the default for user-facing endpoints; fixed window only for low-stakes counters.

## Why

Unthrottled public APIs are trivially abused (credential stuffing, scraping, cost amplification). Rate limiting is the first line of defense, but only when limiters are distributed (Redis, not per-process dicts) and keys are composed (ip + user + apikey + tenant). A single key type lets a CGNAT block punish thousands of legitimate users.

## When To Use

- Public APIs hit by anonymous or semi-trusted users (sign-up, OTP, search, password-reset).
- Tiered SaaS where plan = limit (free/plus/pro/enterprise).
- Expensive endpoints (export, report generation, LLM proxy, image upload).
- Auth endpoints to mitigate credential stuffing (per-IP + per-account limits).
- Edge layer protection in front of slow upstreams to shed load.

## When NOT To Use

- Internal service-to-service traffic with mTLS or service mesh — use authz + circuit breakers instead.
- Single-user CLI / desktop apps talking to a private backend — limits add no security value.
- Background workers reading from a queue — backpressure is queue depth, not rate.
- Quota / billing accounting — those need a metering system (Stripe Meter, OpenMeter), not a rate limiter.

## Content

| File | What's inside |
|------|---------------|
| `content/01-algorithms.xml` | Fixed window, sliding window, token bucket with Python code and rule on which to pick. |
| `content/02-implementation.xml` | FastAPI middleware pattern, tiered limits table, endpoint-specific config, response headers. |
| `content/03-antipatterns.xml` | In-memory limiter at scale, fixed-window burst, CDN IP punishing all traffic, IPv6 bypass, double-limiting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sliding-window.py` | Redis-backed sliding window limiter class, ready to drop into FastAPI middleware. |
| `templates/k6-rl-probe.js` | k6 script that verifies 429 response, Retry-After header, and rate limit headers. |

## Scripts

(none)
