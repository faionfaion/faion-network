---
slug: pnpm-package-management
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Fast, disk-efficient package manager using a content-addressable store and symlinks for strict dependency isolation.
content_id: "a00e7bb5e5f9160f"
tags: [pnpm, package-management, monorepo, nodejs, ci]
---
# pnpm Package Management

## Summary

**One-sentence:** Fast, disk-efficient package manager using a content-addressable store and symlinks for strict dependency isolation.

**One-paragraph:** Fast, disk-efficient package manager using a content-addressable store and symlinks for strict dependency isolation. The concrete rule: always --frozen-lockfile in CI, pin manager version via "packageManager": "pnpm@9.x.y" in root package.json, and block accidental npm/yarn use via a preinstall script. shamefully-hoist=true is the universal wrong fix — reject any PR adding it without justification.

## Applies If (ALL must hold)

- All new Node.js/TypeScript projects unless org policy requires npm/yarn
- Monorepos with 3+ packages: pnpm workspaces are faster and first-class
- CI pipelines where install time matters; pnpm + store cache shaves minutes
- Projects with phantom-dependency bugs (imports work locally, fail elsewhere)
- Container builds wanting layer-cached deps via pnpm fetch

## Skip If (ANY kills it)

- React Native projects pinned to npm/yarn by Metro/Expo (Expo SDK <= 50 had pnpm rough edges)
- One-file scripts where npm exec/bunx is lighter
- Deploy targets with configs expecting package-lock.json that cannot be updated
- Hosting platforms that don't support pnpm out of the box without explicit packageManager field (rare in 2026)

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

- parent skill: `solo/dev/automation-tooling/`
