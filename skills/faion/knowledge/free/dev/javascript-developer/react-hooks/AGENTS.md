---
slug: react-hooks
tier: free
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Functional component patterns using React's built-in hooks — state, effects, memoization, refs, reducers, context, and reusable custom hook extraction.
content_id: "d0967e30d75aa9b4"
tags: [react, hooks, functional-components, state-management, context]
---
# React Hooks

## Summary

**One-sentence:** Functional component patterns using React's built-in hooks — state, effects, memoization, refs, reducers, context, and reusable custom hook extraction.

**One-paragraph:** Functional component patterns using React's built-in hooks — state, effects, memoization, refs, reducers, context, and reusable custom hook extraction.

## Applies If (ALL must hold)

- All functional components needing local state or side effects
- Extracting reusable stateful logic into custom hooks
- Performance optimization via memoization (with profiling first)
- Sharing state across a component tree via Context

## Skip If (ANY kills it)

- Class components (use the React docs migration path)
- Logic that belongs in a state manager (Zustand, TanStack Query) — don't replicate server cache or global UI state with local hooks

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
