# pnpm Package Management

## Summary

Covers pnpm configuration, workspace management, CI/CD integration, and security practices for JavaScript/TypeScript projects. Key rule: pin the pnpm version via `packageManager` field + `corepack`, always commit `pnpm-lock.yaml`, and never use `shamefully-hoist=true` — fix phantom deps via `.pnpmfile.cjs` instead.

## Why

pnpm's content-addressable store and strict non-hoisted layout prevent phantom dependency bugs and supply-chain confusion attacks that npm/yarn permit. Without pinned toolchain (`corepack`), version drift causes lockfile churn and "works on my machine" failures in CI. `--frozen-lockfile` in CI catches accidental dependency mutations.

## When To Use

- All new JavaScript/TypeScript projects (single-package or monorepo).
- Repos whose `packageManager` field specifies `pnpm`.
- CI/CD pipeline setup needing fast, reproducible installs.
- Migrating an npm/yarn repo to pnpm.
- Monorepo work requiring `pnpm --filter` + workspace protocol.

## When NOT To Use

- Repos that mandate npm or yarn (legacy CI, customer constraint, polyrepo with hoisting deps).
- Single-file scripts using `npx` with no `package.json`.
- Electron or legacy native modules that assume hoisted layout.
- Projects using Bun or Deno as primary runtime where pnpm adds debug surface.

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup-config.xml` | Installation, `.npmrc` settings, `packageManager` pinning via `corepack`. |
| `content/02-workspaces.xml` | `pnpm-workspace.yaml`, `--filter` commands, `workspace:*` protocol. |
| `content/03-ci-docker.xml` | GitHub Actions workflow, Dockerfile with pnpm store cache. |
| `content/04-antipatterns.xml` | Mixing managers, missing lockfile, `shamefully-hoist=true`, phantom deps. |

## Templates

| File | Purpose |
|------|---------|
| `templates/npmrc` | Strict `.npmrc` with all recommended settings. |
| `templates/pnpm-bootstrap.sh` | Init script that pins toolchain and creates workspace scaffold. |
| `templates/gh-actions-ci.yml` | GitHub Actions workflow with pnpm cache. |
