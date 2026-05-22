---
slug: microservices-inter-service-comm
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Microservices communicate either synchronously (HTTP/REST or gRPC for queries) or asynchronously (message bus for mutations and events).
content_id: "367d068e3e2227af"
tags: [microservices, inter-service, message-bus, service-discovery, async]
---
# Microservices Inter-Service Communication

## Summary

**One-sentence:** Microservices communicate either synchronously (HTTP/REST or gRPC for queries) or asynchronously (message bus for mutations and events).

**One-paragraph:** Microservices communicate either synchronously (HTTP/REST or gRPC for queries) or asynchronously (message bus for mutations and events). Async by default, sync when proven needed. Service discovery via Consul, Kubernetes DNS, or similar eliminates hardcoded URLs.

## Applies If (ALL must hold)

- Synchronous HTTP: queries where the caller needs an immediate response and the dependency is a single hop (user profile lookup, product detail fetch).
- Async message bus: mutations that span multiple services, events that fan out to multiple consumers, workflows where eventual consistency is acceptable.
- Service discovery: any environment with dynamic service registration (Kubernetes, Consul, ECS) where DNS or a registry replaces static config.

## Skip If (ANY kills it)

- Do not use synchronous HTTP chains longer than two hops inside a request handler — rewrite as saga or precomputed projection.
- Do not use async messaging when the caller requires guaranteed immediate consistency (payment authorization, inventory hard-reserve under contention).
- Do not hardcode service addresses — always use discovery or environment-injected config.

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
