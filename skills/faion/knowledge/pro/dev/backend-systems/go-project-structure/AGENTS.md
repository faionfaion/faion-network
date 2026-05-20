---
slug: go-project-structure
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Standard Go project layout using cmd/, internal/, and an optional pkg/ for code intended for external import.
content_id: "50a320b0762ea1de"
tags: [go, project-structure, layout, golang-standards]
---
# Go Project Structure

## Summary

**One-sentence:** Standard Go project layout using cmd/, internal/, and an optional pkg/ for code intended for external import.

**One-paragraph:** Standard Go project layout using cmd/, internal/, and an optional pkg/ for code intended for external import. Applications live under cmd/<name>/main.go, private logic under internal/{handler,service,repository,model,config}. Dependency injection via constructors; no package-level globals. Graceful shutdown covers the HTTP server, DB pools, queue consumers, and long-running goroutines.

## Applies If (ALL must hold)

- Bootstrapping a new Go service or CLI that follows community norms.
- Splitting a single-package main into internal/{handler,service,repository,model} once it crosses ~1k LoC.
- Adding a second binary (background worker, admin CLI) as a second cmd/<name>/main.go.
- Standardizing layout across many services so on-call engineers find files in the same place.

## Skip If (ANY kills it)

- Tiny single-file scripts or quick experiments — main.go next to go.mod is enough.
- Library-only repos — cmd/, internal/, deployments/ are noise; structure by feature subpackages.
- Go modules being published publicly — heavy internal/ use prevents downstream consumers.
- Monorepos with many services sharing a root — prefer one Go module per service.

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
