---
slug: go-layout-layer-rules
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The Go standard layout only enforces package visibility via internal/ — it does NOT enforce dependency direction between layers.
content_id: "0d51169e2a6d8dfb"
tags: [go, dependency-direction, layer-architecture, golangci-lint]
---
# Go Standard Layout — Layer Dependency Rules

## Summary

**One-sentence:** The Go standard layout only enforces package visibility via internal/ — it does NOT enforce dependency direction between layers.

**One-paragraph:** The Go standard layout only enforces package visibility via internal/ — it does NOT enforce dependency direction between layers. Without depguard or equivalent import linting, handler packages freely import repository packages directly, bypassing the service layer. Explicit rules + automated linting are required to make the layout load-bearing.

## Applies If (ALL must hold)

- Any Go service following the standard layout where you want the layer seams to be mechanically enforced, not just conventional.
- Team or multi-agent settings where different authors might shortcut handler-to-repository imports.
- Services large enough that a single violated import boundary significantly increases coupling.
- CI pipelines that must gate on architecture violations the way they gate on test failures.

## Skip If (ANY kills it)

- Tiny CLIs or scripts — the overhead of a linter config and interface-at-consumer discipline exceeds the value.
- Services already using a different architecture (hexagonal, package-by-feature) — applying these rules on top of a different model causes confusion.

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
