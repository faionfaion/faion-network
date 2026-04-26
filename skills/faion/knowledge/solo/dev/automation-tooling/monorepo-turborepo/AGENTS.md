# Monorepo Setup (Turborepo)

## Summary

Turborepo is a high-performance build orchestrator for JavaScript/TypeScript monorepos. Structure code as `apps/` + `packages/` under pnpm workspaces, declare task dependencies in `turbo.json` (`tasks` field in v2), and let Turborepo cache and parallelize builds. Internal deps use `workspace:*`; shared config lives in `packages/config`.

## Why

Without a task graph, CI rebuilds everything on every push. Turborepo's content-addressable cache (local or remote) skips unchanged tasks, cuts CI time by 60-90%, and enforces correct build ordering via `dependsOn: ["^build"]`. Parallel execution and remote cache sharing across branches compound the savings.

## When To Use

- Multiple JS/TS apps that share UI components, types, or utilities.
- Migrating several npm repos into one workspace to reduce duplication.
- Adding remote caching to an existing multi-package repo.
- Standardizing tsconfig/eslint/prettier across packages via `packages/config`.
- CI builds taking > 2 min because unchanged packages rebuild.

## When NOT To Use

- Polyglot monorepos dominated by Python/Go/Rust — use Bazel or Pants.
- Single-app projects (no shared packages) — pnpm workspaces alone suffice.
- Serverless-first stacks where each function deploys independently and shared code is minimal.
- Teams with no remote cache strategy — local-only gives < 50% of potential savings.

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup.xml` | Directory layout, `turbo.json` (v2 `tasks`), workspace config, root `package.json`. |
| `content/02-packages.xml` | Per-app and per-library `package.json` + `tsconfig.json` patterns, shared ESLint config. |
| `content/03-antipatterns.xml` | Circular deps, missing task outputs, caching non-deterministic tasks, v1/v2 field confusion. |

## Templates

| File | Purpose |
|------|---------|
| `templates/turbo-v2.json` | Minimal `turbo.json` using `tasks` (v2) with build/lint/typecheck/test/dev. |
| `templates/tsconfig-base.json` | Strict shared base tsconfig for library packages. |
| `templates/ci-cache.yml` | GitHub Actions cache step for `node_modules/.cache`, `.turbo`, `.next/cache`. |

## Scripts

none
