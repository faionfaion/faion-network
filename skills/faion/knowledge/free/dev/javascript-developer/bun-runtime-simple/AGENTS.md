---
slug: bun-runtime-simple
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Bun is a high-performance JavaScript runtime with built-in TypeScript support, a fast HTTP server (Bun.
content_id: "2b80461370facee6"
tags: [bun, runtime, typescript, http-server, javascript]
---
# Bun Runtime

## Summary

**One-sentence:** Bun is a high-performance JavaScript runtime with built-in TypeScript support, a fast HTTP server (Bun.

**One-paragraph:** Bun is a high-performance JavaScript runtime with built-in TypeScript support, a fast HTTP server (Bun.serve), native file I/O (Bun.file/Bun.write), built-in password hashing, automatic .env loading, and a Jest-compatible test runner. Use Hono as the preferred web framework. Bun eliminates the need for dotenv, bcrypt, node-fetch, and separate test runners.

## Applies If (ALL must hold)

- New TypeScript projects requiring maximum startup or throughput performance
- Projects needing a unified runtime + test + bundler toolchain
- Replacing node-fetch, bcrypt, or dotenv in an existing project
- Monorepos benefiting from Bun's fast install speed

## Skip If (ANY kills it)

- AWS Lambda deployments (Bun support is limited; use Node.js target)
- Projects with C++ native addon dependencies that lack Bun bindings
- Enterprise environments with strict Node.js LTS runtime policies
- When migrating: verify all dependencies work in Bun before committing

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

- parent skill: `free/dev/javascript-developer/`
