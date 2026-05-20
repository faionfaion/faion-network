---
slug: tailwind-architecture
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A utility-first CSS architecture for React/Vue/Svelte apps: design tokens live in `tailwind.
content_id: "c1e1a963e330cd87"
tags: [tailwind, css, design-tokens, utility-first, variants]
---
# Tailwind Architecture

## Summary

**One-sentence:** A utility-first CSS architecture for React/Vue/Svelte apps: design tokens live in `tailwind.

**One-paragraph:** A utility-first CSS architecture for React/Vue/Svelte apps: design tokens live in `tailwind.config.ts` (or v4 `@theme`); all conditional class merging goes through a project-tuned `cn()` (`tailwind-merge` + `clsx`); variant-rich components use `cva` or `tv()`; `@apply` is restricted to `@layer components` only; `prettier-plugin-tailwindcss` enforces class order; `eslint-plugin-tailwindcss` blocks unknown utilities. Any duplicated 5+ utility chain across 3+ files becomes a primitive component.

## Applies If (ALL must hold)

- Greenfield React/Vue/Svelte/Next.js apps where utility-first is the team standard
- Building design-token-driven Tailwind config for a multi-app design system
- Refactoring CSS Modules / styled-components / SCSS to Tailwind v3 / v4
- Auditing utility class chaos — extracting components, normalizing variants
- Wiring `tailwind-merge` + `cva` / `tv()` for variant-rich component libraries

## Skip If (ANY kills it)

- Email HTML — CSS support is sparse, use inlining tools instead
- Strict CSP environments banning `style-src 'unsafe-inline'` for Tailwind's runtime
- Static-site generators with a hard 14KB CSS budget
- Server-rendered apps shipped to non-Tailwind designers maintaining handcrafted CSS

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
