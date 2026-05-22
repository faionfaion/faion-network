---
slug: go-backend
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-grade Go backend patterns with Gin and Echo frameworks.
content_id: "f3c43363bde0ba3d"
tags: [go, backend, gin, echo, rest-api]
---
# Go Backend Development Patterns

## Summary

**One-sentence:** Production-grade Go backend patterns with Gin and Echo frameworks.

**One-paragraph:** Production-grade Go backend patterns with Gin and Echo frameworks. Covers project structure (cmd/ + internal/ + pkg/), layered architecture (handler → service → repository), HTTP routers, request binding, worker pools, fan-out/fan-in concurrency, and centralized error handling. Defines interfaces at the consumer side for testability. Emphasizes context propagation, typed errors with HTTP status codes, graceful shutdown with WaitGroup, goroutine leak prevention, and middleware ordering pitfalls agents face.

## Applies If (ALL must hold)

- Bootstrapping a new Go service (Gin/Echo/Chi) with the cmd/ + internal/ + pkg/ layout.
- Adding HTTP handlers, middleware, request validation, or worker pools to an existing Go backend.
- Refactoring ad-hoc Go code into the layered handler → service → repository structure.
- Adding apperror-style typed errors and centralized error middleware.

## Skip If (ANY kills it)

- Greenfield where the team has more Python/TS experience and operational constraints don't justify Go's runtime profile. Python/Node might be faster to iterate on with less tooling overhead.
- Pure CLI tools — different layout (cmd/<tool>/main.go + flat libs); see go-project-structure. HTTP backend patterns don't apply to standalone binaries.
- Async-heavy event processing where a message bus + lightweight consumer in any language fits better than a long-lived HTTP service. Consider a dedicated event processor or worker service.
- Prototypes where dependency injection wiring would slow down iteration; prefer a single-file spike first. Layered architecture has overhead; spike first, structure second.
- Embedded systems or extremely resource-constrained environments where Go's memory footprint (10+ MB minimum) exceeds the budget. Use C/Rust instead.

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

- parent skill: `pro/dev/backend-systems/`
