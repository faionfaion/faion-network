---
slug: css-in-js
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for applying CSS-in-JS in React projects: use zero-runtime libraries (`vanilla-extract`, `linaria`, `panda-css`) for RSC and SSR builds; runtime libraries (`styled-components` v6, `@emotion/styled`) only for client-only SPAs.
content_id: "a4a6805a76b3f45d"
tags: [css-in-js, styling, react, design-system, typescript]
---
# CSS-in-JS

## Summary

**One-sentence:** A methodology for applying CSS-in-JS in React projects: use zero-runtime libraries (`vanilla-extract`, `linaria`, `panda-css`) for RSC and SSR builds; runtime libraries (`styled-components` v6, `@emotion/styled`) only for client-only SPAs.

**One-paragraph:** A methodology for applying CSS-in-JS in React projects: use zero-runtime libraries (`vanilla-extract`, `linaria`, `panda-css`) for RSC and SSR builds; runtime libraries (`styled-components` v6, `@emotion/styled`) only for client-only SPAs. Define styled components at module scope, never inside the function body. Use transient props (`$variant`, `$size`), co-locate tokens with TypeScript augmentation, and extract critical CSS for SSR to prevent FOUC. Runtime CSS-in-JS is incompatible with React Server Components and adds 10-30 KB of runtime overhead before any component styles. Defining `styled.X` inside render creates a new class on every render, causing class explosion and performance degradation.

## Applies If (ALL must hold)

- React or Vue components with truly dynamic styles computed from runtime props and state.
- Design systems where tokens need TS-typed access from inside components.
- A11y-driven theming (dark mode, high-contrast, prefers-reduced-motion).
- Component libraries shipped to npm expecting zero CSS-import setup.
- Migrating from inline `style={}` blobs to scoped maintainable styles.

## Skip If (ANY kills it)

- Next.js 15 and App Router with RSC: runtime CSS-in-JS breaks Server Components. Use Tailwind, CSS Modules, or `vanilla-extract`.
- Static marketing sites where CSS Modules or plain CSS ship less JS.
- Tailwind-standardized teams. Mixing creates a split design system.
- Embedded or size-constrained bundles (extension popups, AMP, email).
- React Native. Use StyleSheet API; CSS-in-JS libs that map onto RN carry maintenance risk.

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
