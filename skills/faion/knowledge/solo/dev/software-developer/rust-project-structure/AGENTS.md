# Rust Project Structure

## Summary

Layered module structure for Rust HTTP services (Axum/Actix-web/Poem): `routes/ → handlers/ → services/ → db/ + models/ + middleware/`. Centralized error type in `error.rs`. Shared `AppState` struct with `Clone + Arc<T>` fields for testable dependency injection.

## Why

Flat `main.rs` prototypes become unmaintainable past ~1k LOC. The layered structure enforces that handlers stay thin (no DB queries), services hold business logic, and DB access is isolated. Centralized `AppError` in `error.rs` prevents error-type proliferation and ensures every error maps to a defined HTTP status.

## When To Use

- Bootstrapping a new Rust HTTP service (Axum, Actix-web, Poem, Salvo)
- Migrating a single-file `main.rs` prototype before it grows past ~1k LOC
- Multi-crate workspaces with shared domain types in a library crate

## When NOT To Use

- One-off CLI tools or scripts — a flat `src/main.rs` is sufficient
- Async libraries with no HTTP server — drop `routes/`/`handlers/`, keep `lib.rs` + module tree
- gRPC-only services — tonic generates stubs in a different shape
- Frameworks that prescribe their own layout (Rocket, Loco) — use the framework's idiom

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Directory layout, AppState rules, error centralization, module visibility rules |
| `content/02-router-setup.xml` | Axum Router setup with nested routes, AppState injection, middleware layering |

## Templates

| File | Purpose |
|------|---------|
| `templates/new-axum-svc.sh` | Bootstrap script: cargo init + add deps + create module skeleton + error.rs |
