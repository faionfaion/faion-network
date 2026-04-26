# React Hooks Best Practices

## Summary

A methodology for writing correct React functional components using hooks: call hooks unconditionally at the top level, list exhaustive dependencies, return cleanup from every effect, and prefer derivation over synced state. Memoize (`useCallback`/`useMemo`) only when passing to a memoized child or as a hook dependency — measure first.

## Why

The Rules of Hooks are syntactic contracts enforced at runtime: violating call-order (hooks in conditionals, loops) corrupts React's internal fiber state and produces subtle, non-reproducible bugs. Missing effect dependencies create stale closures that silently compute wrong values. Unnecessary memoization adds cost without benefit and obscures the data flow. These rules are non-obvious and consistently violated by LLMs trained on pre-2022 tutorials.

## When To Use

- New functional components needing state, effects, refs, or context.
- Refactoring class components to hooks.
- Extracting repeated logic into a custom hook (`useFoo`).
- Performance audit: unnecessary re-renders, stale closures, memo bloat.
- Migrating from lifecycle-shim patterns to React 18+ idioms.

## When NOT To Use

- React Server Components (RSC) — hooks are client-only; add `'use client'` boundary or use Server Actions.
- Pre-React 16.8 codebases — upgrade React first.
- Heavy cross-page state (optimistic updates, conflict resolution) — use Zustand / Redux Toolkit / TanStack Query.
- Pure presentational components with no state — memoizing without measuring is premature.
- Form submits in Next.js App Router — use `'use server'` actions instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Rules of Hooks, exhaustive-deps rule, cleanup rule, derivation-over-state rule |
| `content/02-examples.xml` | useState patterns, useEffect with abort, useCallback/useMemo, useRef, custom useFetch, useReducer, Context |
| `content/03-antipatterns.xml` | Antipatterns: hooks in conditions, missing deps (stale closure), object deps, styled inside render, useEffect for derived state |

## Templates

| File | Purpose |
|------|---------|
| `templates/use-fetch.tsx` | Strict-Mode-safe useFetch with AbortController cleanup and typed status |
