---
slug: code-decomposition-patterns
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Fat files (controllers >100 lines, React components >150 lines, settings >150 lines) reduce testability, increase merge conflicts, and obscure responsibility.
content_id: "58e6faadf73e3749"
tags: [refactoring, decomposition, patterns, architecture, code-organization]
---
# Code Decomposition Patterns

## Summary

**One-sentence:** Fat files (controllers >100 lines, React components >150 lines, settings >150 lines) reduce testability, increase merge conflicts, and obscure responsibility.

**One-paragraph:** Fat files (controllers >100 lines, React components >150 lines, settings >150 lines) reduce testability, increase merge conflicts, and obscure responsibility. Named patterns give agents and reviewers a shared vocabulary and precise post-conditions: view files stay thin, services are framework-free, components compose, config splits by environment.

## Applies If (ALL must hold)

- Controller/view exceeds 100 lines with mixed HTTP handling and business logic → Extract Service.
- React/Vue component exceeds 150 lines with multiple UI concerns → Extract Component.
- Flat directory exceeds 20 files or team ownership is unclear → Extract Module.
- Settings file exceeds 150 lines or mixes environment-specific config → Extract Configuration.
- TypeScript files mix types with logic or types are reused across multiple files → Extract Types.
- New feature scaffolding where the agent must lay out files before writing code.

## Skip If (ANY kills it)

- Features totalling ≤200 lines — applying a pattern creates more files than logic.
- Framework-mandated single files (e.g., Django `urls.py`) — forced coupling is not a decomposition target.
- Generated code or ORM migrations — structural changes break the generator contract.
- Performance-critical hot loops where indirection has a measured cost.

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

- parent skill: `free/dev/code-quality/`
