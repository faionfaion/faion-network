# Monorepo Setup (Turborepo)

## Summary

Turborepo is a high-performance build system for JavaScript/TypeScript monorepos. It provides intelligent caching, parallel task execution, and incremental builds across multiple packages and apps. The core rule: every cacheable task must declare explicit `outputs` and `dependsOn`; omitting either causes stale or no-cache builds.

## Why

Monorepos with shared packages waste CI time rebuilding unchanged code. Turborepo's content-hashed task cache eliminates redundant rebuilds — a 5-minute CI step becomes 5 seconds after the first run. Task pipeline declaration (`dependsOn: ["^build"]`) ensures correct execution order across workspace packages.

## When To Use

- 2+ JS/TS apps sharing UI components, types, or utility packages
- Solo or small team running web + admin + marketing site from one repo with shared lint/format/CI
- Projects where CI build time is dominated by re-running unchanged work
- Microservices in TS/JS where shared types (zod schemas, OpenAPI clients) need a single source of truth

## When NOT To Use

- Single app, no shared code — Turbo overhead exceeds benefit
- Polyglot monorepos (Go + TS + Python) — Turbo only orchestrates JS scripts; use Bazel, Pants, or Moon instead
- Projects needing sophisticated dependency graphs (codegen → build → release) — Nx or Bazel scales further
- Teams already on Lerna or Yarn Workspaces with no perf pain — migration cost may not pay back

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Workspace layout, package conventions, `apps/` vs `packages/` split |
| `content/02-pipeline.xml` | `turbo.json` task pipeline, caching rules, `dependsOn`, `outputs`, `env` declarations |
| `content/03-antipatterns.xml` | Circular deps, missing task deps, caching non-deterministic tasks, phantom deps |

## Templates

| File | Purpose |
|------|---------|
| `templates/turbo.json` | Reference `turbo.json` with correct pipeline, cache flags, and env declarations |
| `templates/pnpm-workspace.yaml` | pnpm workspace glob configuration |
| `templates/tsconfig-base.json` | Shared TypeScript base config for library and app packages |
