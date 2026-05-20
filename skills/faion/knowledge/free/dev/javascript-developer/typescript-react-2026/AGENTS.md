---
slug: typescript-react-2026
tier: free
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern patterns for TypeScript 5.
content_id: "cf979d8928342f3b"
tags: [typescript, react, nextjs, server-components, 2026]
---
# TypeScript & React 2026

## Summary

**One-sentence:** Modern patterns for TypeScript 5.

**One-paragraph:** Modern patterns for TypeScript 5.x strict mode, React 19 Server Components, Server Actions, and Next.js 15 App Router. Covers the complete stack for building performant, type-safe full-stack applications in 2026.

## Applies If (ALL must hold)

- Greenfield Next.js 15 + React 19 apps where Server Components and Server Actions are the default architecture.
- Migrating a Create React App or Vite SPA to Next.js App Router with a clear server/client component split.
- Tightening an existing TypeScript project's tsconfig.json to 2026 strict baseline.
- Adding form mutations via Server Actions instead of bespoke API routes + client fetch wrappers.
- Teams adopting React 19's new hooks (useActionState) and directive-based boundaries ('use client', 'use server').

## Skip If (ANY kills it)

- React Native / Expo — Server Components RFC for native is not stable; this methodology is web-only.
- Static-only marketing sites — Astro or Gatsby produce smaller bundles. Next.js 15 RSC adds runtime weight you don't need.
- Pages Router projects you intend to keep — most patterns assume App Router and break Pages Router data fetching.
- Library/SDK packages — verbatimModuleSyntax and allowImportingTsExtensions complicate dual-publish (CJS+ESM).
- Non-Vercel platforms without robust Node.js/RSC support (e.g., Cloudflare Workers with limited APIs).

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
