---
slug: bun-runtime
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Bun is a JavaScript/TypeScript runtime, bundler, test runner, and package manager in a single binary.
content_id: "27d7adc2ef318bd1"
tags: [bun, javascript, typescript, runtime, package-manager, test-runner]
---
# Bun Runtime

## Summary

**One-sentence:** Bun is a JavaScript/TypeScript runtime, bundler, test runner, and package manager in a single binary.

**One-paragraph:** Bun is a JavaScript/TypeScript runtime, bundler, test runner, and package manager in a single binary. It runs TypeScript directly without transpilation, provides native HTTP via Bun.serve, and replaces the npm + tsx + jest + esbuild stack. Startup latency, install time, and test speed are all significantly faster than Node equivalents. Default framework pairing is Hono; database ORM is Drizzle with bun:sqlite.

## Applies If (ALL must hold)

- Greenfield TypeScript backends where cold-start latency or CI install speed matters.
- CLI tools and build scripts that need fast execution.
- Hono / Elysia API servers targeting Bun.serve natively.
- Replacing npm + tsx + jest stack with a single dependency.
- Monorepos with frequent install cycles — Bun install is 10-30x faster.

## Skip If (ANY kills it)

- Long-running production Node.js services already battle-tested — Bun's Node compat is strong (>95%) but not 100%; surprising failures in node:cluster, worker_threads, native modules with node-gyp. Don't migrate stable infra without a parallel test rig.
- Apps depending on niche npm packages with native bindings (some Postgres / image libs) — Bun's NAPI is improving but not flawless.
- Edge providers (Vercel, Cloudflare Workers) that don't support Bun runtime — your app runs on V8, not Bun.
- Teams wedded to Jest's ecosystem (snapshot tooling, transformers) — bun test is fast and Jest-compatible-ish, but plugin ecosystem is thin.
- Windows-first dev teams — Bun on Windows works (since 2024) but lags macOS/Linux.

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
