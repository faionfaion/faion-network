---
slug: rust-backend
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Opinionated Axum service layout: AppError + IntoResponse mapping to RFC 7807, layered modules, Arc-shared AppState, spawn_blocking for CPU-bound work, vertical-slice delivery.
content_id: "128ab84beab42f85"
complexity: deep
produces: code
est_tokens: 4600
tags: [rust, axum, backend, async, tokio]
---
# Rust Backend (Axum)

## Summary

**One-sentence:** Opinionated Axum service layout: AppError + IntoResponse mapping to RFC 7807, layered modules, Arc-shared AppState, spawn_blocking for CPU-bound work, vertical-slice delivery.

**One-paragraph:** Opinionated layout and patterns for Rust HTTP services using Axum: one AppError enum per service with IntoResponse mapping to RFC 7807, layered modules (routes/, handlers/, services/, models/, db/), AppState shared via Arc, CPU-bound work on spawn_blocking, and a vertical-slice delivery model (models → db → services → handlers → routes + tests in one PR). Output is the Cargo project skeleton + a complete vertical slice.

**Ефективно для:**

- Greenfield Rust HTTP service needing project layout + handlers + services + DB + tests.
- Migrating a Python/Node service to Rust for tail-latency or memory reasons.
- Standardising several Rust services on one shape (same AppError, handler/service/db split).
- Onboarding new contributors with a working CRUD slice before learning Tokio/Axum trivia.

## Applies If (ALL must hold)

- Greenfield Rust HTTP service needing full project layout + handlers + services + DB + tests.
- Migrating a Python/Node service to Rust for tail-latency or memory reasons.
- Standardising several Rust services on one shape.
- Onboarding new contributors who need a working CRUD slice without learning Tokio/Axum trivia first.

## Skip If (ANY kills it)

- Library crates (no HTTP) — only the project-structure portion applies.
- gRPC-only services — use tonic; handler shape differs.
- Lambda / Cloud-Functions — lambda_runtime plus a minimal handler is leaner.
- Embedded / no_std — use embassy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Crate name + service name | string | team |
| Database driver choice | Cargo crate | team — sqlx / sea-orm / diesel |
| First resource definition | yaml / md | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems/rust-project-structure/AGENTS.md` | module layout precedes handler patterns |
| `pro/dev/backend-systems/rust-error-handling/AGENTS.md` | AppError pattern is shared |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-cargo` | sonnet | Layout decisions are mostly mechanical. |
| `write-vertical-slice` | sonnet | Writing handler/service/db/tests requires sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/app-error.rs` | AppError enum with IntoResponse mapping to RFC 7807 |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-backend.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[rust-project-structure]]
- [[rust-http-handlers]]
- [[rust-error-handling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
