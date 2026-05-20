---
slug: api-rate-limiting
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Throttle API consumers using sliding window (fairness), fixed window (simplicity), or token bucket (burst control) algorithms.
content_id: "0cc2824b27b5ab75"
tags: [api-design, rate-limiting, scaling, redis, performance]
---
# API Rate Limiting

## Summary

**One-sentence:** Throttle API consumers using sliding window (fairness), fixed window (simplicity), or token bucket (burst control) algorithms.

**One-paragraph:** Throttle API consumers using sliding window (fairness), fixed window (simplicity), or token bucket (burst control) algorithms. Every 429 response includes X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, and Retry-After headers. Limits are tiered by plan; endpoints with expensive operations use tighter per-route limits. Redis backs distributed deployments.

## Applies If (ALL must hold)

- Public APIs where abuse, scraping, or unintentional client loops can degrade service for paying customers — rate limiting is mandatory before launch.
- Tiered SaaS pricing models that gate value by request volume (free / plus / pro / enterprise) and need per-key quotas.
- Cost-sensitive endpoints fronting paid third-party services (LLM inference, geocoding, SMS) where one runaway client triggers real financial loss.
- Auth and password-reset endpoints where rate limiting + lockout deters credential-stuffing and enumeration attacks.
- Distributed multi-instance services that must share counters; a Redis / Valkey-backed sliding window is the standard.

## Skip If (ANY kills it)

- Internal-only RPC between trusted services with stable load profiles — circuit breakers and concurrency limits are more useful than per-key rate limits.
- Pure static asset delivery (CDN handles abuse upstream).
- Workflows already gated by quotas at a different layer (DB connection pool, job queue concurrency) where adding HTTP rate limits hides the real bottleneck.
- Endpoints that must process every event (webhooks, IoT telemetry) — back-pressure with 503 + queues, not 429.

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

- parent skill: `solo/dev/api-developer/`
