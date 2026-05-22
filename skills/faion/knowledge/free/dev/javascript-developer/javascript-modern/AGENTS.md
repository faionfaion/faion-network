---
slug: javascript-modern
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Core principles for new JS/TS projects in 2025-2026: TypeScript-first with strict mode, named exports, explicit public API types, pnpm as default package manager, ESLint 9.
content_id: "80122fe2da2f415b"
tags: [typescript, javascript, standards, eslint, package-manager]
---
# Modern JavaScript/TypeScript Standards

## Summary

**One-sentence:** Core principles for new JS/TS projects in 2025-2026: TypeScript-first with strict mode, named exports, explicit public API types, pnpm as default package manager, ESLint 9.

**One-paragraph:** Core principles for new JS/TS projects in 2025-2026: TypeScript-first with strict mode, named exports, explicit public API types, pnpm as default package manager, ESLint 9.x flat config, and a code placement decision tree. Supported runtimes: Node.js 22 LTS, Bun 1.x, browser ES2022+.

## Applies If (ALL must hold)

- Bootstrapping any new Node.js, Bun, or browser project
- Setting up ESLint in a TypeScript project for the first time
- Deciding whether to use default or named exports
- Choosing a package manager

## Skip If (ANY kills it)

- Existing projects with established tooling — migrate incrementally, not all at once
- AWS Lambda with vendor-locked Node.js 18 — use Node.js target, skip Bun
- Projects where Yarn 4.x workspaces are already in production

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
