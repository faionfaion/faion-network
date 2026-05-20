---
slug: ts-strict-isolated
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every tsconfig.
content_id: "13dccf9cb09645d2"
tags: [typescript, strict-mode, isolated-declarations, project-references, monorepo]
---
# TypeScript Strict + isolatedDeclarations + Project References

## Summary

**One-sentence:** Every tsconfig.

**One-paragraph:** Every tsconfig.json in a TypeScript workspace must enable "strict": true, "noUncheckedIndexedAccess": true, "exactOptionalPropertyTypes": true, and (for libraries / shared packages) "isolatedDeclarations": true plus "composite": true with references to its dependency packages. This raises compile-time precision so that AI-generated code surfaces type errors instead of runtime bugs, and lets fast emitters (Biome, oxc, swc) produce .d.ts without invoking tsc for inference.

## Applies If (ALL must hold)

- Any monorepo with two or more packages.
- Any published library, regardless of size.
- Any application codebase larger than ~10k lines or with multiple AI agents editing concurrently.
- Greenfield TS projects, default-on.

## Skip If (ANY kills it)

- Throwaway single-file scripts, scratch Bun/Deno snippets, REPL experiments — strictness overhead outweighs the value at this size.
- Application entrypoints (apps, not libs) — keep strict and noUncheckedIndexedAccess on, but skip isolatedDeclarations since apps emit no .d.ts.
- Codebases mid-migration where flipping flags would block trunk for weeks — adopt incrementally with // @ts-expect-error budgets.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
