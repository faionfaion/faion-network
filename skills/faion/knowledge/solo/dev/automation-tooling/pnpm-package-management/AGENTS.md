# pnpm Package Management

## Summary

Fast, disk-efficient package manager using a content-addressable store and symlinks for strict dependency isolation. The concrete rule: always `--frozen-lockfile` in CI, pin manager version via `"packageManager": "pnpm@9.x.y"` in root `package.json`, and block accidental npm/yarn use via a `preinstall` script. `shamefully-hoist=true` is the universal wrong fix — reject any PR adding it without justification.

## Why

pnpm eliminates phantom dependencies (imports that work locally, fail in CI) by enforcing strict `node_modules` layout. The content-addressable store shares packages across projects, cutting disk use 50-90% on monorepos. `--filter '...[origin/main]'` enables building only changed packages in monorepos — the primary CI speed win over npm/yarn.

## When To Use

- All new Node.js/TypeScript projects unless org policy requires npm/yarn
- Monorepos with 3+ packages: pnpm workspaces are faster and first-class
- CI pipelines where install time matters; pnpm + store cache shaves minutes
- Projects with phantom-dependency bugs (imports work locally, fail elsewhere)
- Container builds wanting layer-cached deps via `pnpm fetch`

## When NOT To Use

- React Native projects pinned to npm/yarn by Metro/Expo (Expo SDK <= 50 had pnpm rough edges)
- One-file scripts where `npm exec`/`bunx` is lighter
- Deploy targets with configs expecting `package-lock.json` that cannot be updated

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup-and-config.xml` | Installation, .npmrc config, workspace setup, lockfile rules |
| `content/02-workspace-commands.xml` | Monorepo commands (--filter, -r, workspace:*), dep management, publishing, store management |
| `content/03-antipatterns.xml` | Common failures: shameful hoisting, mixing package managers, pnpm patch mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/npmrc` | Strict .npmrc config (engine-strict, frozen lockfile, no shameful hoist) |
| `templates/pnpm-workspace.yaml` | Workspace definition for apps/packages/tools monorepo layout |
| `templates/ci-pnpm.yml` | GitHub Actions workflow with pnpm store cache and frozen-lockfile install |
| `templates/dockerfile-pnpm` | Multi-stage Dockerfile using pnpm fetch for layer caching |
