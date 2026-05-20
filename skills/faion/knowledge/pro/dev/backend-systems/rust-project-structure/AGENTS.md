---
slug: rust-project-structure
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Directory layout for Rust HTTP services: src/{config,error,routes,handlers,services,models,db,middleware}/ with a single AppState struct holding Arc-wrapped resources, main.
content_id: "acc7a79fdc60282d"
tags: [rust, axum, actix, project-structure, modules]
---
# Rust Project Structure (Axum/Actix)

## Summary

**One-sentence:** Directory layout for Rust HTTP services: src/{config,error,routes,handlers,services,models,db,middleware}/ with a single AppState struct holding Arc-wrapped resources, main.

**One-paragraph:** Directory layout for Rust HTTP services: src/{config,error,routes,handlers,services,models,db,middleware}/ with a single AppState struct holding Arc-wrapped resources, main.rs kept under ~80 lines, and migrations in migrations/. Promotes to a Cargo workspace when a second binary or shared-types crate is needed.

## Applies If (ALL must hold)

- Bootstrapping a new Rust web service with a production layout from day one.
- Splitting a single-file main.rs into modules once it exceeds ~500 lines.
- Creating a Cargo workspace for a service that will gain multiple crates.
- Adding a new feature area and choosing between binary, lib, or workspace member.
- Standardizing layout across a fleet of Rust services.

## Skip If (ANY kills it)

- One-off scripts or proc-macros — keep flat in src/main.rs.
- Embedded/no_std projects — layout assumes async/Tokio.
- WASM-only crates — wasm-bindgen dominates the layout.
- Pure FFI shims — build.rs and bindgen dominate.

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
