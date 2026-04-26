# Go Project Structure

## Summary

Standard Go project layout using `cmd/`, `internal/`, and an optional `pkg/` for code intended for external import. Applications live under `cmd/<name>/main.go`, private logic under `internal/{handler,service,repository,model,config}`. Dependency injection via constructors; no package-level globals. Graceful shutdown covers the HTTP server, DB pools, queue consumers, and long-running goroutines.

## Why

The `golang-standards/project-layout` community convention is not officially endorsed by the Go team, but its `cmd+internal` separation is widely understood, maps cleanly to vertical slices, and prevents the two most common structural bugs: package-level global state and cyclic imports. `pkg/` is routinely misused — it should contain code intended to be importable by other modules, which most services never need.

## When To Use

- Bootstrapping a new Go service or CLI that follows community norms.
- Splitting a single-package main into `internal/{handler,service,repository,model}` once it crosses ~1k LoC.
- Adding a second binary (background worker, admin CLI) as a second `cmd/<name>/main.go`.
- Standardizing layout across many services so on-call engineers find files in the same place.

## When NOT To Use

- Tiny single-file scripts or quick experiments — `main.go` next to `go.mod` is enough.
- Library-only repos — `cmd/`, `internal/`, `deployments/` are noise; structure by feature subpackages.
- Go modules being published publicly — heavy `internal/` use prevents downstream consumers.
- Monorepos with many services sharing a root — prefer one Go module per service.

## Content

| File | What's inside |
|------|---------------|
| `content/01-layout.xml` | Directory tree, module init, `cmd/api/main.go` with graceful shutdown. |
| `content/02-packages.xml` | `internal/config`, `internal/model`, `internal/repository`, `internal/service` patterns; DI via constructors. |
| `content/03-antipatterns.xml` | Cyclic imports, package-level globals, `pkg/` misuse, missing graceful shutdown for workers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/new-resource.sh` | Shell script to scaffold handler/service/repository/model for a new resource. |
| `templates/Makefile` | Standard Makefile with build, run, test, lint, docker targets. |
| `templates/Dockerfile` | Multi-stage distroless Dockerfile for Go services. |
