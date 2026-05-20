---
slug: practices-js-ts-stack
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Six conventions for the JS/TS stack: typed React components with explicit interface props, custom hooks for shared async logic, strict TypeScript compiler options, standard Node.
content_id: "b1129db476a94788"
tags: [typescript, react, nextjs, frontend, coding-standards]
---
# JavaScript/TypeScript Stack Practices

## Summary

**One-sentence:** Six conventions for the JS/TS stack: typed React components with explicit interface props, custom hooks for shared async logic, strict TypeScript compiler options, standard Node.

**One-paragraph:** Six conventions for the JS/TS stack: typed React components with explicit interface props, custom hooks for shared async logic, strict TypeScript compiler options, standard Node.js project layout, Next.js App Router file structure, state management selection table, and CSS architecture selection by context.

## Applies If (ALL must hold)

- Greenfield React/Next.js service scaffolding — use as template for component and routing structure.
- Adding TypeScript to an existing JS project — use the strict tsconfig as the starting point.
- Evaluating state management approach for a new feature.
- Code review gate for any PR touching React components or hooks.

## Skip If (ANY kills it)

- Frontend component library authoring (Storybook, design tokens) — see practices-frontend-components.
- Architecture decisions (microservices vs modular monolith) — see dev-methodologies-architecture.
- Next.js 15+ React Server Components with partial prerendering — this covers App Router basics; advanced RSC patterns are in best-practices-2026.
- Projects using Vue, Svelte, or Astro — patterns are React/Next-specific.

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

- parent skill: `solo/dev/automation-tooling/`
