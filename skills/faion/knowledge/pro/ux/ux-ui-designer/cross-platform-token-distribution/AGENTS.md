---
slug: cross-platform-token-distribution
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design tokens define a system's colors, spacing, typography, and other design properties.
content_id: "56e9659da11bd971"
tags: [design-tokens, design-systems, cross-platform, token-distribution, style-dictionary]
---
# Cross-Platform Token Distribution

## Summary

**One-sentence:** Design tokens define a system's colors, spacing, typography, and other design properties.

**One-paragraph:** Design tokens define a system's colors, spacing, typography, and other design properties. Distributing tokens across platforms requires a transformation pipeline that converts a single source (usually Figma or JSON) into platform-specific outputs: CSS variables for web, Swift structs for iOS, XML resources for Android, and JavaScript objects for React Native. This methodology establishes tooling and process to keep tokens synchronized across all platforms.

## Applies If (ALL must hold)

- Single source of truth for design tokens that ship to Web (CSS/SCSS), iOS (Swift/UIKit/SwiftUI), Android (XML/Compose), React Native.
- Replacing hand-maintained brand colors/spacing/type scales scattered across repos.
- Wiring Figma tokens into the repo via Tokens Studio, Specify, or Supernova plugins for designer-driven updates.
- Adding theming (light/dark/high-contrast) and brand variants without per-platform forks or duplication.
- Teams with a versioning and CI culture that can enforce token consistency across release cycles.

## Skip If (ANY kills it)

- One platform only and one product — Style Dictionary overhead is not worth the complexity for a single target.
- Tokens that are not values (animation easing curves, motion specs, temporal properties) — use platform-native specs instead.
- Highly dynamic runtime theming driven by API responses — use a runtime tokens service instead of static files.
- A team without a versioning and CI culture — token drift is worse than no system when the system is not enforced.

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
