# Go Standard Layout

## Summary

Organizes a Go project into `cmd/`, `internal/`, `pkg/`, and `migrations/` directories. `internal/` enforces package privacy at the Go toolchain level, `cmd/` supports multiple binary entry points, and sub-packages (`handler/`, `service/`, `repository/`, `model/`) enforce a layered architecture with dependency flow from handler down to repository.

## Why

Go's `internal/` keyword prevents other modules from importing your private packages — the compiler enforces it, not convention. Splitting concerns into layers prevents circular dependencies, makes testing with mocks straightforward (interfaces at the consumer side), and scales naturally from one binary to many.

## When To Use

- Starting any new Go service or CLI tool
- Refactoring a flat Go codebase that has grown beyond 3-4 files
- Adding a second binary to an existing project
- Setting up a project intended to be imported by external modules (`pkg/`)

## When NOT To Use

- Single-file scripts or one-shot utilities — overhead is not justified
- Prototypes under 200 LOC — premature structure adds friction before requirements settle
- Generated code output directories — follow the generator's own conventions

## Content

| File | What's inside |
|------|---------------|
| `content/01-layout.xml` | Directory tree, layer responsibilities, rules for `internal/` vs `pkg/` |
| `content/02-examples.xml` | Handler example with interface injection; antipatterns (flat structure, God package) |

## Templates

| File | Purpose |
|------|---------|
| `templates/handler.go` | Minimal handler struct with constructor and one endpoint |
