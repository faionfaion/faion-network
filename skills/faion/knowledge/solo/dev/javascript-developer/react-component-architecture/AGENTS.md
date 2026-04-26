# React Component Architecture

## Summary

Scalable React component structure using feature-based modules, colocation, and compound component patterns. The core rule: establish the CVA/variant pattern in one reference component (Button) before generating others — agents copy existing patterns reliably when a reference exists; barrel files must export types alongside components.

## Why

Flat `components/` folders grow unmanageable beyond ~20 files, and business logic mixed into components makes them untestable. Feature-based modules (`features/auth/`, `features/dashboard/`) colocate related components, hooks, types, and API calls so a feature can be understood and modified without touching unrelated code. Container/presenter split keeps presentational components pure and independently testable.

## When To Use

- New React or Next.js project deciding folder structure before writing any components
- Refactoring a flat `components/` folder that has grown beyond 20 files
- Reviewing a component for single-responsibility violations before merging a PR
- Generating a new UI primitive (Button, Input, Card) following the codebase's established variant system

## When NOT To Use

- Very small apps (1-3 pages, fewer than 10 components) — structure overhead exceeds benefit
- Pure server-rendered applications with minimal interactivity — use Next.js server components pattern
- Component libraries consumed externally — those have different export and versioning constraints

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Directory layout, component folder anatomy, feature module boundaries |
| `content/02-patterns.xml` | Functional component with CVA, compound component, container/presenter, render props, polymorphic |
| `content/03-antipatterns.xml` | Prop drilling, giant components, business logic in components |

## Templates

| File | Purpose |
|------|---------|
| `templates/button-component.tsx` | Reference Button: forwardRef, CVA variants, loading state, displayName |
| `templates/compound-card.tsx` | Compound component pattern: Card with Header, Title, Content, Footer sub-components |
| `templates/scaffold-component.sh` | Bash script to scaffold component folder with tsx/test/stories/index files |
