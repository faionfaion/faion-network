# Go Project Structure

## Summary

Standard Go project layout following community conventions: `cmd/<bin>/` for entry points,
`internal/` for private app code, `pkg/` only for truly public API. Dependencies wired by hand
in `cmd/.../main.go`; no DI framework until hand-wiring exceeds ~100 lines. Core rules:
`internal/` default, `CGO_ENABLED=0` in containers, one `.golangci.yml` shared by local dev
and CI.

## Why

Go's toolchain enforces `internal/` boundaries, preventing accidental coupling across packages.
Starting flat and promoting to structure only when justified avoids premature abstraction. Cyclic
imports — Go's most common agent mistake — are caught at compile time; extracting a shared
types package into `internal/model` resolves them without exposing symbols unnecessarily.

## When To Use

- Bootstrapping a new Go service, CLI, or library
- Refactoring a flat single-package program that has crossed ~3 entry points or ~5 domain concepts
- Standardizing across multiple Go services so agents can navigate predictably
- Wiring DI manually with constructors in `cmd/<bin>/main.go`

## When NOT To Use

- One-file scripts and learning exercises — flat layout beats premature structure
- Pure libraries: don't add `internal/` and `cmd/` if you only ship exported packages
- Code generators that define their own layout (`buf`, `kubebuilder`, `cobra-cli`)
- Multi-language monorepos where Go is one of N — follow the org-wide layout
- When team consensus differs — enforcing against the team will lose

## Content

| File | What's inside |
|------|---------------|
| `content/01-layout.xml` | Directory tree, `internal/` vs `pkg/`, module init, anti-patterns |
| `content/02-wiring.xml` | `cmd/api/main.go` entry point, config, graceful shutdown, DI by hand |
| `content/03-quality.xml` | Makefile targets, multi-stage Dockerfile, golangci-lint, test conventions |

## Templates

| File | Purpose |
|------|---------|
| `templates/scaffold-go.sh` | Bash script to materialise standard tree from module path + binary names |
| `templates/Makefile` | Build, test, lint, coverage, Docker targets |
