---
slug: go-http-handlers
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for building Go HTTP services with Gin or Echo: explicit middleware stack (Recovery first, then Logger, then RequestID), thin handlers that only bind → call service → translate to HTTP, request structs with `binding:"required,.
content_id: "f153f4f0a4100705"
tags: [go, http, gin, echo, middleware]
---
# Go HTTP Handlers (Gin / Echo)

## Summary

**One-sentence:** A methodology for building Go HTTP services with Gin or Echo: explicit middleware stack (Recovery first, then Logger, then RequestID), thin handlers that only bind → call service → translate to HTTP, request structs with `binding:"required,.

**One-paragraph:** A methodology for building Go HTTP services with Gin or Echo: explicit middleware stack (Recovery first, then Logger, then RequestID), thin handlers that only bind → call service → translate to HTTP, request structs with `binding:"required,..."` tags, `c.Request.Context()` propagated to all downstream calls, and a graceful shutdown wrapper on SIGINT/SIGTERM. Choose Gin for ecosystem breadth; Echo for first-party middleware and interface-driven handlers.

## Applies If (ALL must hold)

- Building a Go HTTP service with ergonomic routing and middleware composition.
- Gin: JSON-heavy endpoints, gin-binding tag validation, broad middleware ecosystem.
- Echo: first-party JWT/CORS/rate-limit, interface-driven handlers, HTTP/2.
- Greenfield microservice on Linux/k8s where memory footprint matters.
- Migrating a Python/Node API to Go for throughput or cost reasons.

## Skip If (ANY kills it)

- Go 1.22+ shops where `net/http` ServeMux supports method+path routing and the team prefers stdlib-only.
- `fasthttp`-backed routers (Fiber) where stdlib middleware compatibility is required.
- gRPC-first services — drive HTTP via `grpc-gateway` instead.
- One-off CLIs or five-route admin tools.
- Teams already standardized on chi, Fiber, or huma — do not mix routers.

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

- parent skill: `free/dev/software-developer/`
