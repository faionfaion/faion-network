---
slug: ui-lib-basics
tier: solo
group: dev
domain: frontend-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A UI component library provides reusable, accessible interface primitives (buttons, inputs, modals) built once and shared across features.
content_id: "c79d2795c907d0d5"
tags: [ui-library, component-library, storybook, accessibility, design-system]
---
# UI Component Library Basics

## Summary

**One-sentence:** A UI component library provides reusable, accessible interface primitives (buttons, inputs, modals) built once and shared across features.

**One-paragraph:** A UI component library provides reusable, accessible interface primitives (buttons, inputs, modals) built once and shared across features. The library enforces a three-layer hierarchy: primitives/ (single responsibility), composite/ (composed from primitives), and patterns/ (complex UI patterns). Components must use forwardRef, named exports only, and ship with Storybook stories and tests.

## Applies If (ALL must hold)

- Multiple features or apps share UI primitives and you keep re-implementing buttons, modals, inputs.
- Team or agent fleet is producing inconsistent patterns; a centralized library enforces a standard.
- You need accessibility built in once (focus rings, ARIA wiring) instead of audited per PR.
- Setting up a monorepo where primitives live in a shared packages/ui/.

## Skip If (ANY kills it)

- Single small app where YAGNI applies; a flat components/ folder is enough.
- Fast-evolving product still finding its visual language; premature abstraction freezes decisions.
- You can adopt shadcn/ui or an existing library — building from scratch rarely pays off solo.
- Marketing site with brochure pages; library overhead exceeds reuse.

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

- parent skill: `solo/dev/frontend-developer/`
