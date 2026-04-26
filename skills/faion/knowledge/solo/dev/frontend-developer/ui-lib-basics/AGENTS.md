# UI Component Library Basics

## Summary

A UI component library provides reusable, accessible interface primitives (buttons, inputs, modals) built once and shared across features. The library enforces a three-layer hierarchy: `primitives/` (single responsibility), `composite/` (composed from primitives), and `patterns/` (complex UI patterns). Components must use `forwardRef`, named exports only, and ship with Storybook stories and tests.

## Why

Rebuilding the same Button or Input per feature accumulates inconsistency, accessibility gaps, and bundle duplication. A shared library forces decisions once, gates regressions with visual + a11y CI, and lets agents focus on feature logic rather than styling primitives from scratch.

## When To Use

- Multiple features or apps share UI primitives and you keep re-implementing buttons, modals, inputs.
- Team or agent fleet is producing inconsistent patterns; a centralized library enforces a standard.
- You need accessibility built in once (focus rings, ARIA wiring) instead of audited per PR.
- Setting up a monorepo where primitives live in a shared `packages/ui/`.

## When NOT To Use

- Single small app where YAGNI applies; a flat `components/` folder is enough.
- Fast-evolving product still finding its visual language; premature abstraction freezes decisions.
- You can adopt shadcn/ui or an existing library — building from scratch rarely pays off solo.
- Marketing site with brochure pages; library overhead exceeds reuse.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Directory layout, naming rules, export conventions, bundle-size budget config. |
| `content/02-component-rules.xml` | forwardRef, named exports, ARIA wiring, CSS variable theming rules with Button/Input examples. |
| `content/03-antipatterns.xml` | Prop explosion, tight coupling, CSS leakage, Storybook drift, barrel-file tree-shaking. |

## Templates

| File | Purpose |
|------|---------|
| `templates/new-component.sh` | Scaffold script: creates story-first component skeleton (stories → impl → index). |
| `templates/size-limit.json` | Bundle-size budget per export for CI enforcement. |

## Scripts

none
