---
slug: design-tokens-implementation
tier: solo
group: dev
domain: frontend-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design tokens form a three-layer hierarchy — primitives (raw hex/rem), semantic (bg.
content_id: "40a8e728842b2b33"
tags: [design-tokens, style-dictionary, token-pipeline, theming, multi-platform]
---
# Design Tokens Implementation

## Summary

**One-sentence:** Design tokens form a three-layer hierarchy — primitives (raw hex/rem), semantic (bg.

**One-paragraph:** Design tokens form a three-layer hierarchy — primitives (raw hex/rem), semantic (bg.surface.default), and component (button.primary.bg) — built from JSON/DTCG sources and compiled to CSS custom properties, TypeScript, iOS Swift, and Android XML via Style Dictionary or Terrazzo. App code consumes only the semantic and component layers. Mode switching (light/dark/high-contrast) lives in separate mode files per mode; the semantic alias layer resolves at build time. Without a token pipeline, color and spacing scatter across component files and become impossible to theme, migrate, or verify for WCAG contrast.

## Applies If (ALL must hold)

- Multi-platform product (web + iOS + Android) needing a single source of truth for color, typography, and spacing.
- Migrating ad-hoc CSS variables or Sass $color-* maps to a centralized pipeline.
- Wiring Tailwind theme, CSS custom properties, and native platform outputs from one JSON source without duplication.
- Light/dark/high-contrast/brand modes via a semantic alias layer that switches at build time.
- Connecting Figma Variables → Tokens Studio → Style Dictionary → app codegen for design-to-dev automation.
- Teams that need auditable token changes (git diff on JSON before and after rebuilds).

## Skip If (ANY kills it)

- Single-app, single-platform project with stable styling — over-engineering for solos. Use Tailwind config or CSS custom properties directly.
- Prototype/MVP where design churn outpaces token churn — the abstraction adds overhead without payoff.
- Static marketing sites with no design system to maintain — direct CSS suffices.
- When the organization will never use more than one platform or theme variant.

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
