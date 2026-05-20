---
slug: api-gateway-patterns
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An API gateway is a single entry point for all client requests to backend services, acting as a reverse proxy for cross-cutting concerns.
content_id: "b760d2e20b391f0f"
tags: [api-gateway, architecture, microservices, bff, routing]
---
# API Gateway Patterns and Technology Selection

## Summary

**One-sentence:** An API gateway is a single entry point for all client requests to backend services, acting as a reverse proxy for cross-cutting concerns.

**One-paragraph:** An API gateway is a single entry point for all client requests to backend services, acting as a reverse proxy for cross-cutting concerns. Pick the right pattern (simple routing, BFF, aggregation, or edge+mesh) based on client diversity and backend topology, then select the right technology from Kong, AWS API Gateway, Traefik, Envoy, APISIX, Apigee, or Apollo Router.

## Applies If (ALL must hold)

- Designing the front door for a new microservices or serverless system.
- Multiple client types (web, mobile, IoT, partner APIs) with different data and auth needs.
- Centralizing auth, rate limiting, routing, or observability across services.
- Migrating from monolith to microservices and needing a stable external surface.
- Selecting between gateway technologies given infra, team, and performance constraints.

## Skip If (ANY kills it)

- Single monolith with one host — a reverse proxy (nginx, Caddy) is sufficient; gateway adds latency and ops cost without benefit.
- Internal east-west traffic between services on a service mesh — that is mesh territory (Istio/Linkerd), not edge gateway.
- Simple Lambda + Function URL deployments where API Gateway adds no value over direct invocation.
- Real-time bidirectional streams that need persistent connections at scale — use AppSync, a dedicated WS gateway, or NATS/Centrifugo instead.

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

- parent skill: `solo/dev/software-architect/`
