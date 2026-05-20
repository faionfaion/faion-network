---
slug: react-patterns
tier: free
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Feature-based folder structure, typed functional components, custom hooks, Context provider pattern, state management decision tree, and memoization rules for maintainable React apps.
content_id: "0bf7c3bbbfa64206"
tags: [react, hooks, typescript]
---
# React Patterns

## Summary

**One-sentence:** Feature-based folder structure, typed functional components, custom hooks, Context provider pattern, state management decision tree, and memoization rules for maintainable React apps.

**One-paragraph:** Feature-based folder structure, typed functional components, custom hooks, Context provider pattern, state management decision tree, and memoization rules for maintainable React apps.

## Applies If (ALL must hold)

- Building a new React feature module (auth, dashboard, checkout)
- Deciding where to put state (server vs. local vs. global)
- Extracting reusable async data-fetching logic into a custom hook
- Wrapping third-party state in a typed Context provider
- Optimizing a component that profiling shows as a bottleneck

## Skip If (ANY kills it)

- Simple presentational components with no state — just write JSX
- When TanStack Query is already in use for server state — don't duplicate with useEffect fetching
- When Zustand already handles global UI state — don't add a Context layer on top

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
