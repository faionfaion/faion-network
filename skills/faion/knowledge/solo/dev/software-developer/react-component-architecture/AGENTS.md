---
slug: react-component-architecture
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A directory layout and component design system for React/Next.
content_id: "cd2901f848c11557"
tags: [react, architecture, component-design, next.js, typescript]
---
# React Component Architecture: Layout, Patterns, and Isolation

## Summary

**One-sentence:** A directory layout and component design system for React/Next.

**One-paragraph:** A directory layout and component design system for React/Next.js projects: shared UI primitives in components/ui/, feature modules in features/<name>/, colocated tests and stories, named exports only, and data fetching confined to feature hooks or RSC. Component files are capped at ~250 lines; beyond that, extract subcomponents or hooks.

## Applies If (ALL must hold)

- Bootstrapping a new React/Next.js codebase and you need a defensible directory layout from day one.
- Refactoring a sprawling components/ folder into feature-modules plus shared UI primitives.
- Building or extending a design system (Button, Card, Input) where compound and polymorphic patterns matter.
- Establishing coding standards an LLM agent will follow when generating new components.
- Migrating from Pages Router to App Router and deciding server vs client component boundaries.

## Skip If (ANY kills it)

- One-off React prototypes or spikes — full architecture is overhead.
- Pure logic libraries with no JSX — use module-architecture guidance instead.
- React Native projects with platform-specific file suffixes — adapt, do not copy.
- When the project already mandates a different convention (Bulletproof React, Nx generators) — follow that instead.

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

- parent skill: `solo/dev/software-developer/`
