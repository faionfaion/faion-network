---
slug: javascript
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Universal coding standards for modern JS/TS (2025–2026): TypeScript 5.
content_id: "879cec1a8080b507"
tags: [javascript, typescript, react, nodejs, eslint, vitest]
---
# JavaScript / TypeScript Standards

## Summary

**One-sentence:** Universal coding standards for modern JS/TS (2025–2026): TypeScript 5.

**One-paragraph:** Universal coding standards for modern JS/TS (2025–2026): TypeScript 5.x with `strict: true`, named exports over default, `const` + arrow functions for callbacks, `pnpm` as default package manager, ESLint 9.x flat config + Prettier, Vitest for testing. React follows function components + hooks; Node.js follows controller → service → repository with centralized error handling. Strict type checking at compile time catches null-dereference, untyped params, and unreachable branches before production.

## Applies If (ALL must hold)

- Starting any new TypeScript project (frontend or backend)
- Adding React components, custom hooks, or context providers
- Building Express / Fastify / Bun HTTP services
- Writing unit, component, or API-level tests in Vitest / Jest
- Setting up package management, linting, and formatting for a new repo

## Skip If (ANY kills it)

- Legacy JavaScript projects where introducing TypeScript requires a full migration — scope first
- Projects locked to Node.js less than or equal to 16 — some ES2022 targets and pnpm features will not work
- Deno or edge-runtime projects with incompatible module resolution — verify toolchain support first
- Projects that use Yarn Plug'n'Play workspaces — pnpm config shown is incompatible

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
