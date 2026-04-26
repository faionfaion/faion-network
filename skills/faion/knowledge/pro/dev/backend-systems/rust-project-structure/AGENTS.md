# Rust Project Structure (Axum/Actix)

## Summary

Directory layout for Rust HTTP services: `src/{config,error,routes,handlers,services,models,db,middleware}/` with a single `AppState` struct holding `Arc`-wrapped resources, `main.rs` kept under ~80 lines, and migrations in `migrations/`. Promotes to a Cargo workspace when a second binary or shared-types crate is needed.

## Why

Without a consistent module layout, agents mix Axum and Actix imports, create circular `mod.rs` dependencies, and scatter database logic into handlers. The routes/handlers/services/db split enforces a one-way dependency graph and makes CRUD vertical slices predictable to generate and review.

## When To Use

- Bootstrapping a new Rust web service with a production layout from day one.
- Splitting a single-file `main.rs` into modules once it exceeds ~500 lines.
- Creating a Cargo workspace for a service that will gain multiple crates.
- Adding a new feature area and choosing between binary, lib, or workspace member.
- Standardizing layout across a fleet of Rust services.

## When NOT To Use

- One-off scripts or proc-macros — keep flat in `src/main.rs`.
- Embedded/`no_std` projects — layout assumes async/Tokio.
- WASM-only crates — `wasm-bindgen` dominates the layout.
- Pure FFI shims — `build.rs` and bindgen dominate.

## Content

| File | What's inside |
|------|---------------|
| `content/01-directory-layout.xml` | Directory tree, module responsibilities, AppState shape rules. |
| `content/02-router-setup.xml` | Axum Router composition, route nesting, TraceLayer wiring. |
| `content/03-rules.xml` | Workspace promotion triggers, compile-time gotchas, agent pitfalls. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main_rs.rs` | Minimal main.rs: config load, state build, router compose, serve. |
| `templates/new_module.sh` | Shell scaffolder: creates routes/handlers/services/db/models files for a new entity. |
