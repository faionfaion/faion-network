---
slug: pnpm-package-management
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers pnpm configuration, workspace management, CI/CD integration, and security practices for JavaScript/TypeScript projects.
content_id: "a00e7bb5e5f9160f"
tags: [pnpm, package-management, monorepo, nodejs, javascript]
---
# pnpm Package Management

## Summary

**One-sentence:** Covers pnpm configuration, workspace management, CI/CD integration, and security practices for JavaScript/TypeScript projects.

**One-paragraph:** Covers pnpm configuration, workspace management, CI/CD integration, and security practices for JavaScript/TypeScript projects. Key rule: pin the pnpm version via `packageManager` field + `corepack`, always commit `pnpm-lock.yaml`, and never use `shamefully-hoist=true` — fix phantom deps via `.pnpmfile.cjs` instead.

## Applies If (ALL must hold)

- All new JavaScript/TypeScript projects (single-package or monorepo).
- Repos whose `packageManager` field specifies `pnpm`.
- CI/CD pipeline setup needing fast, reproducible installs.
- Migrating an npm/yarn repo to pnpm.
- Monorepo work requiring `pnpm --filter` + workspace protocol.

## Skip If (ANY kills it)

- Repos that mandate npm or yarn (legacy CI, customer constraint, polyrepo with hoisting deps).
- Single-file scripts using `npx` with no `package.json`.
- Electron or legacy native modules that assume hoisted layout.
- Projects using Bun or Deno as primary runtime where pnpm adds debug surface.

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

- parent skill: `free/dev/software-developer/`
