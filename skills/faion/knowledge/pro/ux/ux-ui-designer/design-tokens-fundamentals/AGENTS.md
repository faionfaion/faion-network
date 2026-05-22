---
slug: design-tokens-fundamentals
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three-tier token architecture (primitive, semantic, component) keeps single source of truth via W3C DTCG JSON and Style Dictionary.
content_id: "cab4ee38609b44a1"
tags: [design-tokens, w3c-dtcg, semantic-naming, theming, accessibility]
---
# Design Tokens Fundamentals

## Summary

**One-sentence:** Three-tier token architecture (primitive, semantic, component) keeps single source of truth via W3C DTCG JSON and Style Dictionary.

**One-paragraph:** Three-tier token architecture (primitive, semantic, component) keeps single source of truth via W3C DTCG JSON and Style Dictionary. Semantic naming enables theming without component changes. Purpose-named tokens survive dark mode and theme swaps.

## Applies If (ALL must hold)

- Bootstrapping a design system targeting two or more platforms.
- Migrating from ad-hoc CSS variables to a single source of truth.
- Adding dark/light/high-contrast modes to a shipped product.
- Designer-developer round-trip workflows where Figma values drift from code.
- Multi-brand white-label products that need theme swaps without rebuild.

## Skip If (ANY kills it)

- Single-page MVP with one designer/developer — overhead exceeds value until month 3+.
- Static two-page marketing site — Tailwind defaults suffice.
- Throwaway internal tools with no design-language target.
- Teams that haven't agreed on semantic naming yet — resolve naming first.

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

- parent skill: `pro/ux/ux-ui-designer/`
