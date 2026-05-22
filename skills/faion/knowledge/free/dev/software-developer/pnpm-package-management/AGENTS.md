---
slug: pnpm-package-management
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a reproducible pnpm setup — packageManager pin via corepack, committed pnpm-lock.yaml, no shamefully-hoist, .pnpmfile.cjs for phantom deps, workspace:* protocol, CI --frozen-lockfile gate.
content_id: "a00e7bb5e5f9160f"
complexity: light
produces: config
est_tokens: 2900
tags: [pnpm, package-management, corepack, workspace, monorepo]
---
# pnpm Package Management

## Summary

**One-sentence:** Produces a reproducible pnpm setup — packageManager pin via corepack, committed pnpm-lock.yaml, no shamefully-hoist, .pnpmfile.cjs for phantom deps, workspace:* protocol, CI --frozen-lockfile gate.

**One-paragraph:** Pin the pnpm version in root package.json `packageManager` field (corepack-managed). Always commit `pnpm-lock.yaml`. Keep `shamefully-hoist=false`; fix phantom-dep issues with the `readPackage` hook in `.pnpmfile.cjs`, never with hoisting. Reference internal packages by `workspace:*`; Changesets rewrites to real versions at publish. CI runs `pnpm install --frozen-lockfile` and caches the pnpm store keyed by `pnpm-lock.yaml` hash.

**Ефективно для:** new repos / monorepos adopting pnpm, migrations from npm/yarn where lockfile drift wastes hours, services suffering from phantom dependencies, CI suites with slow install times.

## Applies If (ALL must hold)

- JS/TS project on Node 18+.
- Team accepts pnpm as the package manager.
- CI can run corepack + pnpm.
- Monorepo with internal packages, OR single repo wanting reproducible installs.

## Skip If (ANY kills it)

- Project mandated to use npm or yarn for compliance reasons.
- Single-tool ecosystem (e.g. Deno) that doesn't need npm-shaped lockfiles.
- Plugin that ships as zero-dep (no install step).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pnpm version | semver string (e.g. `9.6.0`) | pnpm release notes |
| Node engines | `>=20.x` | infra |
| CI provider | string | infra ADR |
| Workspaces (if any) | YAML pnpm-workspace.yaml | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[javascript]]` | TS+lint+test stack interacts with the package manager. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: packageManager pin, no shamefully-hoist, workspace:*, frozen-lockfile in CI, .pnpmfile.cjs for phantom deps | ~600 |
| `content/02-output-contract.xml` | essential | Required files (package.json packageManager, .npmrc, .pnpmfile.cjs) + CI fields | ~500 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: unpinned pnpm, shamefully-hoist=true, npm install in CI, missing lockfile | ~500 |
| `content/06-decision-tree.xml` | essential | Root: "JS/TS project where pnpm is acceptable?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate configs | haiku | Boilerplate. |
| Migration from npm/yarn | sonnet | Lockfile conversion. |
| Phantom-dep diagnosis | opus | Multi-package reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/npmrc` | .npmrc with `engine-strict=true`, `strict-peer-dependencies=false` (or true if team accepts). |
| `templates/pnpm-bootstrap.sh` | Bootstrap script — corepack enable + install + verify. |
| `templates/gh-actions-ci.yml` | GitHub Actions CI with pnpm cache + frozen-lockfile. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pnpm-package-management.py` | Verifies packageManager field, lockfile presence, no shamefully-hoist in any .npmrc. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[javascript]]` — broader TS/JS standards

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: pnpm acceptable, corepack supported, lockfile commit acceptable.
