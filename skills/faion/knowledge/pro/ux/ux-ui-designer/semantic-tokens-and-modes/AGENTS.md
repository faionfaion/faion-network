---
slug: semantic-tokens-and-modes
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for structuring design tokens in three explicit layers — reference (raw palette/scale), system (semantic, mode-aware), component (component-scoped) — and driving them through a four-stage pipeline: author (Figma Variables) → export (REST API) → transform (Style Dictionary) → consume (CSS/Swift/Compose).
content_id: "20e934c1b5c9dd87"
tags: [design-tokens, semantic-tokens, modes, style-dictionary, theming]
---
# Semantic Tokens and Modes

## Summary

**One-sentence:** A methodology for structuring design tokens in three explicit layers — reference (raw palette/scale), system (semantic, mode-aware), component (component-scoped) — and driving them through a four-stage pipeline: author (Figma Variables) → export (REST API) → transform (Style Dictionary) → consume (CSS/Swift/Compose).

**One-paragraph:** A methodology for structuring design tokens in three explicit layers — reference (raw palette/scale), system (semantic, mode-aware), component (component-scoped) — and driving them through a four-stage pipeline: author (Figma Variables) → export (REST API) → transform (Style Dictionary) → consume (CSS/Swift/Compose). Every semantic token must be defined in every mode (light, dark, high-contrast, brand). Raw reference values must never appear in product code; lint rules are mandatory.

## Applies If (ALL must hold)

- Adding light/dark/high-contrast modes to an existing token system.
- Multi-brand or white-label products where one library serves several visual identities.
- Multi-platform builds (web + iOS + Android) that share semantic intent but diverge in raw values.
- Density modes (compact/comfortable) for data-dense enterprise UIs.
- Migrating from raw CSS custom properties to a tokens-as-source-of-truth pipeline.

## Skip If (ANY kills it)

- Single-theme product with no foreseeable theming requirement — semantic-token indirection adds no payoff.
- Pure marketing campaigns or one-off pages outside the system.
- Component libraries below ~30 components — overhead exceeds savings.
- Motion/animation primitives — semantic naming for durations rarely earns its keep.

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
