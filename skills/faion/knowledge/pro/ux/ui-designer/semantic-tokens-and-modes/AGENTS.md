---
slug: semantic-tokens-and-modes
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A semantic token layer maps primitive values (`color.
content_id: "20e934c1b5c9dd87"
tags: [design-tokens, theming, semantic-layer, figma-variables]
---
# Semantic Tokens and Modes

## Summary

**One-sentence:** A semantic token layer maps primitive values (`color.

**One-paragraph:** A semantic token layer maps primitive values (`color.blue.500`) to purpose-based aliases (`color.action.primary`) that resolve to different values per mode (light/dark, high-contrast, compact density, brand). Modes are declared per collection in Figma Variables or token JSON; Style Dictionary emits platform-specific output per mode. Every alias must have a value in every declared mode, and contrast pairs must be co-located so validation is automatable.

## Applies If (ALL must hold)

- Building a token system that supports light/dark, high-contrast, density, or brand modes.
- Migrating from raw color/spacing tokens to a semantic layer.
- Wiring Figma Variables to Style Dictionary so designers and engineers share one source of truth.
- Adding a new mode without doubling component code paths.

## Skip If (ANY kills it)

- Single-theme apps where modes add cost without payoff — start with raw tokens, promote when the second theme arrives.
- Print or static asset pipelines where mode-switching does not apply.
- Pure animation/motion tokens where mode semantics are rarely meaningful.

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

- parent skill: `pro/ux/ui-designer/`
