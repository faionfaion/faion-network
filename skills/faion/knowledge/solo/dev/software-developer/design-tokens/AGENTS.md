---
slug: design-tokens
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design tokens are the atomic values of a design system — colors, spacing, typography, shadows — stored as structured data with a three-tier hierarchy: primitive (raw values) → semantic (purpose-based aliases) → component (usage-specific).
content_id: "7f16a0941dce99d3"
tags: [design-system, tokens, style-dictionary, theming, figma]
---
# Design Tokens

## Summary

**One-sentence:** Design tokens are the atomic values of a design system — colors, spacing, typography, shadows — stored as structured data with a three-tier hierarchy: primitive (raw values) → semantic (purpose-based aliases) → component (usage-specific).

**One-paragraph:** Design tokens are the atomic values of a design system — colors, spacing, typography, shadows — stored as structured data with a three-tier hierarchy: primitive (raw values) → semantic (purpose-based aliases) → component (usage-specific). One JSON source of truth emits per-platform outputs (CSS vars, JS constants, iOS Swift, Android XML) via Style Dictionary.

## Applies If (ALL must hold)

- Building or extending a design system for web + mobile.
- Introducing dark mode or white-label theming.
- Bridging Figma to code so design and engineering stay in sync.
- Standardizing brand across multiple apps in a monorepo.
- Connecting a token pipeline to Tailwind config or platform constants.

## Skip If (ANY kills it)

- Single one-off marketing page — overhead beats payoff.
- Apps fully delegating to a UI library (Material, Mantine) with no re-skinning.
- Prototype work where designers iterate hourly — token churn outpaces pipeline cost.
- Pure server-rendered emails using external template SaaS that owns tokens.

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
