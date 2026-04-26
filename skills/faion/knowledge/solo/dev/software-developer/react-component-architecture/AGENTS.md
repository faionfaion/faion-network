# React Component Architecture

## Summary

A directory layout and component design system for React/Next.js projects: shared UI primitives in `components/ui/`, feature modules in `features/<name>/`, colocated tests and stories, named exports only, and data fetching confined to feature hooks or RSC. Component files are capped at ~250 lines; beyond that, extract subcomponents or hooks.

## Why

Without explicit boundaries, components accumulate logic, features leak into each other, and refactoring becomes risky. Colocation (component + test + story + types in one folder) makes renames mechanical. Named exports preserve tree-shaking and refactor tooling. Feature module isolation enforced by `eslint-plugin-boundaries` prevents cross-feature coupling from silently growing.

## When To Use

- Bootstrapping a new React/Next.js codebase and you need a defensible directory layout from day one.
- Refactoring a sprawling `components/` folder into feature-modules plus shared UI primitives.
- Building or extending a design system (Button, Card, Input) where compound and polymorphic patterns matter.
- Establishing coding standards an LLM agent will follow when generating new components.
- Migrating from Pages Router to App Router and deciding server vs client component boundaries.

## When NOT To Use

- One-off React prototypes or spikes — full architecture is overhead.
- Pure logic libraries with no JSX — use module-architecture guidance instead.
- React Native projects with platform-specific file suffixes — adapt, do not copy.
- When the project already mandates a different convention (Bulletproof React, Nx generators) — follow that instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-directory-layout.xml` | Directory tree rules: ui primitives, feature modules, hooks, utils; colocation pattern. |
| `content/02-component-patterns.xml` | Functional with forwardRef, compound, container/presenter, render props, polymorphic as. |
| `content/03-antipatterns.xml` | Prop drilling, giant components, business logic in JSX, default exports, deep import paths. |

## Templates

| File | Purpose |
|------|---------|
| `templates/button.tsx` | Button primitive with cva variants, forwardRef (React 18), full TypeScript props. |
| `templates/plopfile.cjs` | Plop generator: scaffolds component folder (tsx + test + stories + index.ts). |

## Scripts

(none)
