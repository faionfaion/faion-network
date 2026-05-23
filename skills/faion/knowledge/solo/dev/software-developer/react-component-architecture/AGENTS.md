---
slug: react-component-architecture
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: React component architecture spec: feature folders, server/client component split, no business logic in primitives, hooks discipline, props vs context decision, memoization rules.
content_id: "ac7213ed8991e6c4"
complexity: medium
produces: spec
est_tokens: 5100
tags: [react, components, architecture, hooks, state]
---
# React Component Architecture

## Summary

**One-sentence:** React component architecture spec: feature folders, server/client component split, no business logic in primitives, hooks discipline, props vs context decision, memoization rules.

**One-paragraph:** React apps rot when business logic leaks into primitives, when context is used as a global state bus, when useEffect runs business logic, and when components are memoised everywhere by reflex. This methodology produces a component-architecture spec naming feature folder shape, server vs client component boundaries (Next.js app router), primitive vs feature responsibility split, props vs context boundary, hook discipline (no side effects in render, effects only for sync-with-external), and a memoisation policy.

**Ефективно для:**

- Новий React/Next.js проект - зафіксувати feature folders + server/client split.
- Legacy app з 200+ компонентів - провести audit і split primitive vs feature.
- Context перетворився в global state bus - провести rectification.
- Memoization всюди без вимірів - впровадити policy.
- useEffect для бізнес-логіки - winnerless redesign.

## Applies If (ALL must hold)

- Codebase uses React 18+ or Next.js 13+ (app router).
- Team is shipping components iteratively (not a static site).
- There is a chosen styling system (Tailwind / CSS modules / vanilla extract).
- Build pipeline can enforce ESLint rules.

## Skip If (ANY kills it)

- Project is plain HTML + sprinkle of vanilla JS - no React.
- App is a tiny prototype with <10 components.
- Team has chosen a different framework (Vue, Svelte, Solid).
- Migration is in progress and the target architecture is documented elsewhere.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Routing decision | Next.js app router / pages / SPA | engineering |
| Styling system | Tailwind / CSS modules / vanilla extract | design |
| State scope map | list of state slices + scope (route / global / feature) | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[shadcn-ui-architecture]] | primitive layer composed from shadcn vendored primitives. |
| [[tailwind-architecture]] | styling layer this spec assumes is in place. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: feature folder, server/client split, no business in primitives, context boundary, effects discipline, memoisation policy, prop-drilling cap | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: routing, folders, primitives, state, memoisation | ~900 |
| `content/05-examples.xml` | essential | Worked example for a Next.js multi-tenant SaaS UI | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-routing` | haiku | Closed-set selection. |
| `design-feature-folders` | sonnet | Per-feature judgement. |
| `audit-primitive-leakage` | sonnet | Import-graph judgement. |
| `scope-state` | opus | Stakes high; wrong scope re-renders everything. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-skeleton.tsx` | Feature folder skeleton: components/, hooks/, lib/, index.ts barrel. |
| `templates/store.ts` | Feature-scoped Zustand store skeleton. |
| `templates/button.tsx` | Button UI primitive with cva variants and forwardRef. |
| `templates/plopfile.cjs` | Plop generator config: scaffold a feature folder from CLI. |
| `templates/_smoke-test.json` | Minimum viable architecture artefact for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-react-component-architecture.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[shadcn-ui-architecture]]
- [[tailwind-architecture]]
- [[ui-component-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - framework, state shape, primitive leakage, memo pressure - onto a rule from `content/01-core-rules.xml`. Use it before refactoring: it catches context-as-bus and business-in-primitive upstream.
