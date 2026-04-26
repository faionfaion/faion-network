# pnpm Workspaces with Dependency Catalogs

## Summary

In a TypeScript / JavaScript monorepo, use pnpm 9+ with `workspaces` and the `catalog:` protocol to share external dependency versions across packages. One catalog entry in `pnpm-workspace.yaml` controls the version of `react`, `typescript`, `vitest`, etc., for every workspace package; every `package.json` references those entries with `"react": "catalog:"`. Internal packages link via `"workspace:*"`. The result: zero version drift, one bump updates the world, AI agents cannot accidentally introduce a `react@19.0` / `react@19.1` split by adding a dep to one package.

## Why

Multi-package monorepos accumulate "package A wants react 19.0, package B wants react 19.1" merge conflicts because every `package.json` is a private little manifest that diverges over time. Catalogs invert that: the version lives in one place, the manifests reference it. AI agents adding deps via `pnpm add react -F web` automatically pick up the catalog version (when configured), so the next agent on a different package sees the same React. pnpm's filtering (`--filter`) and strict peer-dep model also makes hermetic per-package builds tractable, which is the prerequisite for parallel AI worktrees.

## When To Use

- Any monorepo with two or more packages.
- Any team that has fought "package X wants react@19.0, package Y wants react@19.1" merge conflicts.
- Microfrontend / shared-library workspaces where consistency is an audit concern.
- Repos with parallel AI agents in worktrees that may add deps independently.

## When NOT To Use

- Single-package apps where npm or Bun is enough — catalogs add ceremony without payoff.
- Bun-native runtime projects that need `bun.lockb` parity with the runtime — use `bun install`.
- Yarn 4 PnP shops with working constraints — the migration cost rarely beats the status quo.
- Hybrid setups that must publish to npm with classic `dependencies` (publish step must replace `catalog:` and `workspace:*` with concrete versions; add a release script before adopting).

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The catalog rule, the `catalog:` and `workspace:*` protocols, and the publish-time replacement step. |
| `content/02-filtering.xml` | `pnpm --filter` patterns for partial installs, change-aware test runs, and worktree isolation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pnpm-workspace.yaml` | Workspace + catalog declaration with the most-shared packages. |
| `templates/package-json-fragment.json` | `package.json` fragment showing `catalog:` and `workspace:*` usage. |
