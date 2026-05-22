---
slug: design-tokens-basics
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design tokens are the atomic values of a design system — colors, spacing, typography, radii, shadows — stored as platform-agnostic data.
content_id: "09a300e57f2ad3f4"
tags: [design-tokens, design-systems, theming, style-dictionary, figma]
---
# Design Tokens: Basics

## Summary

**One-sentence:** Design tokens are the atomic values of a design system — colors, spacing, typography, radii, shadows — stored as platform-agnostic data.

**One-paragraph:** Design tokens are the atomic values of a design system — colors, spacing, typography, radii, shadows — stored as platform-agnostic data. They enforce a three-level hierarchy: primitive (raw values) → semantic (purpose aliases) → component (per-component overrides), with a single source of truth that compiles to CSS variables, iOS Swift, Android XML, or any target. Without tokens, design decisions scatter across components as hardcoded hex values and magic numbers, making theming and rebrand work O(N) per component. Semantic tokens decouple purpose from value: changing the brand primary color requires one token update, not a grep-and-replace.

## Applies If (ALL must hold)

- Starting a design system from scratch — define primitive → semantic → component token tiers before writing components.
- Migrating ad-hoc CSS variables and hex values to a single source of truth (tokens.json or W3C Design Tokens Format Module).
- Setting up theming (light/dark, brand white-label) where switching only the semantic layer is enough to change appearance.
- Bridging Figma variables and code via Tokens Studio and Style Dictionary for design-to-dev handoff.
- Multi-platform design systems (web, iOS, Android) that need a single token source compiling to each platform's native format.

## Skip If (ANY kills it)

- One-off landing page with a single brand and no theming — direct CSS variables suffice.
- The entire app is built with Tailwind and the team is happy with tailwind.config.ts as the de facto token layer — adding Style Dictionary on top is duplicate work.
- Product in pre-PMF iteration where design is changing weekly — token churn will be brutal and the abstraction slows experiments.
- When a third-party component library owns all tokens and override is impractical or not allowed.

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
