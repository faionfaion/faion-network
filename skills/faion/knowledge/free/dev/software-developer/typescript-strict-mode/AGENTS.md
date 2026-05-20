---
slug: typescript-strict-mode
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: TypeScript strict mode is a compiler flag group (`strict: true` + four recommended extras) that eliminates implicit `any`, enforces null safety, catches unchecked index access, and requires explicit return types.
content_id: "12394fa50d7d784d"
tags: [typescript, strict-mode, type-safety, tsconfig, zod]
---
# TypeScript Strict Mode

## Summary

**One-sentence:** TypeScript strict mode is a compiler flag group (`strict: true` + four recommended extras) that eliminates implicit `any`, enforces null safety, catches unchecked index access, and requires explicit return types.

**One-paragraph:** TypeScript strict mode is a compiler flag group (`strict: true` + four recommended extras) that eliminates implicit `any`, enforces null safety, catches unchecked index access, and requires explicit return types. The canonical 2026 baseline adds `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitReturns`, and `noFallthroughCasesInSwitch` on top of `strict: true`. IO boundaries are validated with Zod; `unknown` replaces `any` throughout.

## Applies If (ALL must hold)

- All new TypeScript projects — strict mode is the only sane production default.
- JS-to-TS migrations — adopt incrementally per directory.
- Library / SDK development — `.d.ts` strictness is part of the API contract.
- Critical paths (auth, billing, IAM) where null/undefined bugs are unacceptable.
- LLM-authored codebases — strict is the cheapest static gate against hallucinated APIs.
- Migrating a JS codebase — adopt strict in stages (`strict: true` → `noImplicitAny` → `strictNullChecks` per directory).
- Multi-team monorepos where shared types are the integration contract.
- Critical paths (auth, billing, IAM, parsing) where null/undefined bugs are unacceptable.

## Skip If (ANY kills it)

- Throwaway prototypes / spike branches — strict mode doubles iteration cost.
- Bridging legacy JS with thousands of `noImplicitAny` violations — adopt per-file via `// @ts-check` first.
- Heavily dynamic plugin systems where types fight extension hooks — use Zod parse boundaries instead.
- Codebases with poorly typed third-party libs lacking `@types/*` — add typed adapters first.
- Codebases that depend on poorly typed third-party libs without `@types/*` — `skipLibCheck: true` + targeted `unknown` adapters first.
- Highly dynamic plugin systems where types fight extension hooks; structural alternatives (Zod schemas + parse boundaries) cleaner.

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
