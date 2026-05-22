---
slug: go-standard-layout
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Organizes a Go project into cmd/, internal/, pkg/, and migrations/ directories.
content_id: "c5198cd547e903b3"
tags: [go, architecture, layering, best-practices, package-design]
---
# Go Standard Layout

## Summary

**One-sentence:** Organizes a Go project into cmd/, internal/, pkg/, and migrations/ directories.

**One-paragraph:** Organizes a Go project into cmd/, internal/, pkg/, and migrations/ directories. internal/ enforces package privacy at the Go toolchain level, cmd/ supports multiple binary entry points, and sub-packages (handler/, service/, repository/, model/) enforce a layered architecture with dependency flow from handler down to repository.

## Applies If (ALL must hold)

- Starting any new Go service or CLI tool
- Refactoring a flat Go codebase that has grown beyond 3-4 files
- Adding a second binary to an existing project
- Setting up a project intended to be imported by external modules (pkg/)
- Bootstrapping a new Go service or CLI: agent scaffolds cmd/ + internal/ + pkg/ plus go.mod, Makefile, Dockerfile, and CI
- Refactoring a flat single-package Go project that has outgrown a single directory
- Multi-binary repos (API + worker + CLI sharing a domain)
- Enforcing import boundaries in a modular monolith written in Go (internal/ + per-feature subpackages)

## Skip If (ANY kills it)

- Single-file scripts or one-shot utilities — overhead is not justified
- Prototypes under 200 LOC — premature structure adds friction before requirements settle
- Generated code output directories — follow the generator's own conventions
- Tiny utility CLI / library with <5 files — keep it flat
- Strict adherence to the unofficial golang-standards/project-layout repo
- Polyglot monorepos where a Go package is one of many — adapt to monorepo conventions (Bazel, Nx)
- One-shot Lambdas / small Cloud Functions where main.go next to the manifest beats deep folders
- Plugin systems requiring pure pkg/ exports — internal/ would block third-party integrators by design

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

- parent skill: `solo/dev/software-developer/`
