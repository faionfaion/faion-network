---
slug: pnpm-catalogs
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: In a TypeScript / JavaScript monorepo, use pnpm 9+ with `workspaces` and the `catalog:` protocol to share external dependency versions across packages.
content_id: "6c28a72561ac01e3"
tags: [pnpm, monorepo, workspaces, dependency-catalog, typescript]
---
# pnpm Workspaces with Dependency Catalogs

## Summary

**One-sentence:** In a TypeScript / JavaScript monorepo, use pnpm 9+ with `workspaces` and the `catalog:` protocol to share external dependency versions across packages.

**One-paragraph:** In a TypeScript / JavaScript monorepo, use pnpm 9+ with `workspaces` and the `catalog:` protocol to share external dependency versions across packages. One catalog entry in `pnpm-workspace.yaml` controls the version of `react`, `typescript`, `vitest`, etc., for every workspace package; every `package.json` references those entries with `"react": "catalog:"`. Internal packages link via `"workspace:*"`. The result: zero version drift, one bump updates the world, AI agents cannot accidentally introduce a `react@19.0` / `react@19.1` split by adding a dep to one package.

## Applies If (ALL must hold)

- Any monorepo with two or more packages.
- Any team that has fought "package X wants react@19.0, package Y wants react@19.1" merge conflicts.
- Microfrontend / shared-library workspaces where consistency is an audit concern.
- Repos with parallel AI agents in worktrees that may add deps independently.

## Skip If (ANY kills it)

- Single-package apps where npm or Bun is enough — catalogs add ceremony without payoff.
- Bun-native runtime projects that need `bun.lockb` parity with the runtime — use `bun install`.
- Yarn 4 PnP shops with working constraints — the migration cost rarely beats the status quo.
- Hybrid setups that must publish to npm with classic `dependencies` (publish step must replace `catalog:` and `workspace:*` with concrete versions; add a release script before adopting).

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
