---
slug: tailwind-design-tokens
tier: solo
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Map design tokens (colors, spacing, typography) to Tailwind's theme config via CSS custom properties, so the design system and component library share a single source of truth.
content_id: "015e97fab8369c86"
tags: [tailwind, design-tokens, css-variables, theming, style-dictionary]
---
# Tailwind + Design Tokens

## Summary

**One-sentence:** Map design tokens (colors, spacing, typography) to Tailwind's theme config via CSS custom properties, so the design system and component library share a single source of truth.

**One-paragraph:** Map design tokens (colors, spacing, typography) to Tailwind's theme config via CSS custom properties, so the design system and component library share a single source of truth. All tailwind.config.js values must reference var(--token-name) — no hardcoded hex or pixel values. Semantic tokens (color.action.primary) are exposed in Tailwind; primitive tokens (raw hex) stay in CSS variables only.

## Applies If (ALL must hold)

- Setting up a new project's design system foundation (define tokens once, use everywhere)
- Migrating hardcoded hex values and magic numbers to semantic token classes
- Bridging a Figma design system (with Variables/Tokens) to a Tailwind CSS implementation
- Multi-brand or white-label products where the same component library needs per-tenant theming
- When Tailwind utilities and custom components must share the same spacing/color values

## Skip If (ANY kills it)

- Projects with no design system requirements — raw Tailwind utilities are sufficient
- Teams not using Tailwind — use CSS custom properties directly or Style Dictionary alone
- Projects where design tokens are owned by a design-ops team and locked from code edits
- Prototype/throwaway work where systematic tokens add overhead with no payoff

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

- parent skill: `solo/ux/ux-ui-designer/`
