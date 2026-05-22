---
slug: api-gateway-patterns
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Centralized API gateway for microservices: routing, JWT/mTLS auth, rate limiting per consumer, CORS, request tracing via X-Request-ID, circuit breakers, and edge caching.
content_id: "b760d2e20b391f0f"
tags: [microservices, api-gateway, kong, aws-api-gateway, bff]
---
# API Gateway Patterns

## Summary

**One-sentence:** Centralized API gateway for microservices: routing, JWT/mTLS auth, rate limiting per consumer, CORS, request tracing via X-Request-ID, circuit breakers, and edge caching.

**One-paragraph:** Centralized API gateway for microservices: routing, JWT/mTLS auth, rate limiting per consumer, CORS, request tracing via X-Request-ID, circuit breakers, and edge caching. Covers Kong (declarative kong.yml), AWS API Gateway (Serverless/Terraform), Nginx, and BFF (Backend-for-Frontend) aggregation. Gateway must stay stateless and "boring" — no business logic in plugins.

## Applies If (ALL must hold)

- Multi-service backend needing centralized auth, rate limiting, request tracing, CORS.
- Migrating monolith to microservices: front old + new behind one gateway, then peel off routes.
- Public APIs with plan-based quotas (free/pro) — Kong, AWS APIGW, Apigee handle usage plans natively.
- BFF per channel (web, mobile, partner) with different auth/aggregation needs.

## Skip If (ANY kills it)

- Single-service apps — a gateway is one more thing to operate.
- Sub-1ms latency hot paths — each gateway hop adds 1–5ms; use a sidecar service mesh instead.
- Internal east-west service-to-service traffic — service mesh (Linkerd, Istio) fits better.
- Teams that cannot afford Kong/Envoy + config plane operational complexity.

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

- parent skill: `pro/dev/software-developer/`
