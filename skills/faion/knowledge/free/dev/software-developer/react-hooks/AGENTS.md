---
slug: react-hooks
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for writing correct React functional components using hooks: call hooks unconditionally at the top level, list exhaustive dependencies, return cleanup from every effect, and prefer derivation over synced state.
content_id: "d0967e30d75aa9b4"
tags: [react, hooks, javascript, typescript, functional-components]
---
# React Hooks Best Practices

## Summary

**One-sentence:** A methodology for writing correct React functional components using hooks: call hooks unconditionally at the top level, list exhaustive dependencies, return cleanup from every effect, and prefer derivation over synced state.

**One-paragraph:** A methodology for writing correct React functional components using hooks: call hooks unconditionally at the top level, list exhaustive dependencies, return cleanup from every effect, and prefer derivation over synced state. Memoize (useCallback/useMemo) only when passing to a memoized child or as a hook dependency—measure first.

## Applies If (ALL must hold)

- New functional components needing state, effects, refs, or context.
- Refactoring class components to hooks.
- Extracting repeated logic into a custom hook (useFoo).
- Performance audit: unnecessary re-renders, stale closures, memo bloat.
- Migrating from lifecycle-shim patterns to React 18+ idioms.

## Skip If (ANY kills it)

- React Server Components (RSC) — hooks are client-only; add 'use client' boundary or use Server Actions.
- Pre-React 16.8 codebases — upgrade React first.
- Heavy cross-page state (optimistic updates, conflict resolution) — use Zustand / Redux Toolkit / TanStack Query.
- Pure presentational components with no state — memoizing without measuring is premature.
- Form submits in Next.js App Router — use 'use server' actions instead.

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
