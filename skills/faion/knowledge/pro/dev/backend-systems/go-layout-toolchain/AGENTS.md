---
slug: go-layout-toolchain
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The Go standard layout is toolchain-agnostic, but each slot in the layout (cmd/, internal/handler, internal/repository, migrations/) maps to a preferred set of tools.
content_id: "379c7b5ac8836674"
tags: [go, toolchain, golangci-lint, testcontainers]
---
# Go Standard Layout — Toolchain Reference

## Summary

**One-sentence:** The Go standard layout is toolchain-agnostic, but each slot in the layout (cmd/, internal/handler, internal/repository, migrations/) maps to a preferred set of tools.

**One-paragraph:** The Go standard layout is toolchain-agnostic, but each slot in the layout (cmd/, internal/handler, internal/repository, migrations/) maps to a preferred set of tools. This reference pairs tools to layout slots so agents select the right binary for the job rather than inventing combinations.

## Applies If (ALL must hold)

- Starting a new Go service and selecting tools for each layout layer.
- Onboarding an agent to an existing Go service to prevent it from introducing incompatible tools.
- Code review where the agent must verify that tools are used in the correct layer.

## Skip If (ANY kills it)

- Projects with a locked-in toolchain documented in go-stack.md — use the project-specific record instead.
- Non-Go projects — toolchain selections are Go-specific.

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
