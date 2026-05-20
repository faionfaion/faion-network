---
slug: api-gateway-patterns
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Centralize cross-cutting concerns (TLS, JWT, rate-limit, CORS, observability) at one declarative ingress.
content_id: "b760d2e20b391f0f"
tags: [api-gateway, routing, microservices, kong, nginx, bff, rate-limiting, jwt]
---
# API Gateway Patterns

## Summary

**One-sentence:** Centralize cross-cutting concerns (TLS, JWT, rate-limit, CORS, observability) at one declarative ingress.

**One-paragraph:** Centralize cross-cutting concerns (TLS, JWT, rate-limit, CORS, observability) at one declarative ingress. GitOps-managed, stateless, Redis-backed limiters, explicit per-route timeouts, BFF fan-out via concurrent calls.

## Applies If (ALL must hold)

- Multi-service backends needing one stable public URL regardless of internal topology
- Mobile + Web + Partner clients with different payload shapes (BFF pattern)
- Enforcing org-wide policies (mTLS, JWT, audit logging) without per-service duplication
- Strangler-fig migrations routing legacy paths to old service, new paths to new service
- You need centralized observability (one Prometheus scrape target, one access-log sink) for traffic across many services
- You are exposing two or more internal services to the public internet and want a uniform TLS + auth surface

## Skip If (ANY kills it)

- Single-service apps where Nginx + app middleware suffice — full gateway is operational overhead
- Latency-critical hot paths (real-time bidding, HFT) — prefer sidecar/mesh direct path
- Greenfield prototypes — start with a reverse proxy, add gateway when second service ships
- Pure static asset delivery (CDN handles routing, caching, TLS)
- Internal service-to-service mesh — use a service mesh (Istio, Linkerd) instead of an ingress gateway

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
