---
slug: rate-limiting
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: API protection via configurable per-key rate limiters (fixed window, sliding window, token bucket) backed by Redis/Valkey, with standard X-RateLimit-* / Retry-After response headers and a 429 JSON error body.
content_id: "11914d9d761e11c9"
tags: [rate-limiting, api-security, fastapi, redis, throttling]
---
# Rate Limiting with Redis and Standard Headers

## Summary

**One-sentence:** API protection via configurable per-key rate limiters (fixed window, sliding window, token bucket) backed by Redis/Valkey, with standard X-RateLimit-* / Retry-After response headers and a 429 JSON error body.

**One-paragraph:** API protection via configurable per-key rate limiters (fixed window, sliding window, token bucket) backed by Redis/Valkey, with standard X-RateLimit-* / Retry-After response headers and a 429 JSON error body. Every deployment must use Redis — in-memory limiters break at greater than 1 replica. Sliding window or GCRA is the default for user-facing endpoints; fixed window only for low-stakes counters.

## Applies If (ALL must hold)

- Public APIs hit by anonymous or semi-trusted users (sign-up, OTP, search, password-reset).
- Tiered SaaS where plan = limit (free/plus/pro/enterprise).
- Expensive endpoints (export, report generation, LLM proxy, image upload).
- Auth endpoints to mitigate credential stuffing (per-IP + per-account limits).
- Edge layer protection in front of slow upstreams to shed load.

## Skip If (ANY kills it)

- Internal service-to-service traffic with mTLS or service mesh — use authz + circuit breakers instead.
- Single-user CLI / desktop apps talking to a private backend — limits add no security value.
- Background workers reading from a queue — backpressure is queue depth, not rate.
- Quota / billing accounting — those need a metering system (Stripe Meter, OpenMeter), not a rate limiter.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/software-developer/`
