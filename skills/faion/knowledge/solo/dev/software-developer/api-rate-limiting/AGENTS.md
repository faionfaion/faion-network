# API Rate Limiting

## Summary

Server-side request throttling using sliding-window, token-bucket, or fixed-window algorithms backed by a shared store (Redis/Valkey). Every public endpoint must have a per-identity limit; responses include `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, and `Retry-After` headers per the IETF draft. In-process counters are forbidden for multi-replica deployments.

## Why

Without shared-store rate limiting, a single client can exhaust server resources or bias billing. The IETF headers let well-behaved clients self-throttle, preventing retry storms. Sliding-window avoids the 2x burst at window boundaries that fixed-window allows.

## When To Use

- Public APIs exposed to untrusted callers (free/paid tiers, third-party integrations).
- Single-server deployments where one client can DoS the box.
- Expensive endpoints: search, exports, AI calls, OAuth token mint, mailers.
- Per-tenant fairness in multi-tenant SaaS.
- Abuse protection on `/login`, `/register`, `/forgot-password`.

## When Not To Use

- Pure internal RPC behind a private network or service mesh — use mTLS quotas instead.
- Latency-critical hot paths where a Redis round-trip would double response cost — push limiting to nginx/envoy.
- Single-user CLI tools or scripts on developer laptops.
- Idempotent webhooks from trusted partners with their own backpressure (Stripe, GitHub).

## Content

| File | What's inside |
|------|---------------|
| `content/01-algorithms.xml` | Fixed-window, sliding-window, token-bucket — when to pick each, Python impls. |
| `content/02-headers-and-responses.xml` | IETF header names, 429 response shape, Retry-After semantics, tiered limits table. |
| `content/03-antipatterns.xml` | In-process counters, keying on `request.client.host` behind proxy, missing Retry-After, clock skew. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sliding_window.py` | Redis sorted-set sliding-window implementation for FastAPI middleware. |
| `templates/k6-rate-limit-check.js` | k6 load script verifying rate-limit headers and 429 boundary behavior. |
