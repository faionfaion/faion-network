---
slug: rust-backend
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Opinionated layout and patterns for Rust HTTP services using Axum: one AppError enum per service with IntoResponse mapping to RFC 7807, layered modules (routes/, handlers/, services/, models/, db/), AppState shared via Arc, CPU-bound work on spawn_blocking, and a vertical-slice delivery model (models → db → services → handlers → routes + tests in one PR).
content_id: "7cf3eaabcf1cf1c7"
tags: [rust, axum, backend, async, tokio]
---
# Rust Backend (Axum)

## Summary

**One-sentence:** Opinionated layout and patterns for Rust HTTP services using Axum: one AppError enum per service with IntoResponse mapping to RFC 7807, layered modules (routes/, handlers/, services/, models/, db/), AppState shared via Arc, CPU-bound work on spawn_blocking, and a vertical-slice delivery model (models → db → services → handlers → routes + tests in one PR).

**One-paragraph:** Opinionated layout and patterns for Rust HTTP services using Axum: one AppError enum per service with IntoResponse mapping to RFC 7807, layered modules (routes/, handlers/, services/, models/, db/), AppState shared via Arc, CPU-bound work on spawn_blocking, and a vertical-slice delivery model (models → db → services → handlers → routes + tests in one PR).

## Applies If (ALL must hold)

- Greenfield Rust HTTP service needing full project layout + handlers + services + DB + tests.
- Migrating a Python/Node service to Rust for tail-latency or memory reasons.
- Standardizing several Rust services on one shape (same AppError, handler/service/db split, test scaffolding).
- Onboarding new contributors who need a working CRUD slice without learning Tokio/Axum trivia first.

## Skip If (ANY kills it)

- Library crates (no HTTP) — only the project-structure portion applies.
- gRPC-only services — use tonic; handler shape differs.
- Lambda/Cloud-Functions — lambda_runtime plus a minimal handler is leaner.
- Embedded/no_std — use embassy instead.
- Cross-runtime libraries — drop Tokio specifics.

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
