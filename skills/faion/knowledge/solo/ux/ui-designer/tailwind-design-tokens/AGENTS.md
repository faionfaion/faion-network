---
slug: tailwind-design-tokens
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Integrating design tokens into Tailwind CSS by mapping token values to CSS custom properties and referencing them in `tailwind.
content_id: "015e97fab8369c86"
tags: [tailwind, design-tokens, css-variables, theming, style-dictionary]
---
# Tailwind + Design Tokens

## Summary

**One-sentence:** Integrating design tokens into Tailwind CSS by mapping token values to CSS custom properties and referencing them in `tailwind.

**One-paragraph:** Integrating design tokens into Tailwind CSS by mapping token values to CSS custom properties and referencing them in `tailwind.config.js` — using RGB channel syntax for color tokens to preserve opacity modifier functionality (`bg-primary/50`), and extending (not replacing) the default theme.

## Applies If (ALL must hold)

- Bootstrapping a new Tailwind project that must support theming (dark mode, brand variants, white-label)
- Migrating an existing Tailwind codebase from hardcoded utility values to CSS-variable-backed tokens
- Generating `tailwind.config.js` theme overrides from a Style Dictionary token build output
- Auditing a Tailwind codebase for arbitrary values (`text-[#...]`, `p-[...]`) that should become tokens
- Setting up a Storybook token documentation layer alongside a Tailwind component library

## Skip If (ANY kills it)

- Projects not using Tailwind — use Style Dictionary + CSS custom properties directly
- Pure CSS/SCSS codebases where Tailwind migration is not planned
- When design tokens are not yet defined or stable — generating config before taxonomy is finalized creates throwaway work
- Utility-class-only projects with zero theming requirements — CSS variable indirection adds complexity without payoff

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

- parent skill: `solo/ux/ui-designer/`
