---
slug: api-rate-limiting
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Server-side request throttling using sliding-window, token-bucket, or fixed-window algorithms backed by a shared store (Redis/Valkey).
content_id: "0cc2824b27b5ab75"
tags: [rate-limiting, api, throttling, anti-abuse, redis]
---
# API Rate Limiting

## Summary

**One-sentence:** Server-side request throttling using sliding-window, token-bucket, or fixed-window algorithms backed by a shared store (Redis/Valkey).

**One-paragraph:** Server-side request throttling using sliding-window, token-bucket, or fixed-window algorithms backed by a shared store (Redis/Valkey). Every public endpoint must have a per-identity limit; responses include `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, and `Retry-After` headers per the IETF draft. In-process counters are forbidden for multi-replica deployments.

## Applies If (ALL must hold)

- Public APIs exposed to untrusted callers (free/paid tiers, third-party integrations)
- Single-server deployments where one client can DoS the box
- Expensive endpoints: search, exports, AI calls, OAuth token mint, mailers
- Per-tenant fairness in multi-tenant SaaS
- Abuse protection on `/login`, `/register`, `/forgot-password`

## Skip If (ANY kills it)

- Pure internal RPC behind a private network or service mesh — use mTLS quotas instead
- Latency-critical hot paths where a Redis round-trip would double response cost — push limiting to nginx/envoy
- Single-user CLI tools or scripts on developer laptops
- Idempotent webhooks from trusted partners with their own backpressure (Stripe, GitHub)

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
