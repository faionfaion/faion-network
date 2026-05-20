---
slug: mobile-ux-basics
tier: pro
group: ux
domain: ux-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A mobile-first design methodology covering touch target sizing, thumb-zone placement, navigation patterns, form optimization, performance budgets, and platform conventions (iOS vs Android).
content_id: "0de7d2ab38da2ef2"
tags: [mobile-ux, mobile-first, touch-design, responsive-design, performance]
---
# Mobile UX Basics: Touch Design, Navigation, and Performance

## Summary

**One-sentence:** A mobile-first design methodology covering touch target sizing, thumb-zone placement, navigation patterns, form optimization, performance budgets, and platform conventions (iOS vs Android).

**One-paragraph:** A mobile-first design methodology covering touch target sizing, thumb-zone placement, navigation patterns, form optimization, performance budgets, and platform conventions (iOS vs Android). Start with the smallest screen, expose only essential features, then enhance for larger viewports. Touch targets must be at least 44x44pt (iOS) or 48x48dp (Android) with 8px spacing between them. Lock the codebook before coding begins; adding themes mid-study invalidates cross-participant comparison.

## Applies If (ALL must hold)

- Auditing an existing mobile experience for thumb-zone, touch-target, performance, and platform-convention compliance.
- Pre-launch checklist enforcement before each mobile release: Lighthouse mobile score, accessibility, touch-target sizes.
- Code review for mobile-affecting PRs: flagging small touch targets, hidden navigation, blocking JS, missing input types.
- Cross-platform parity reviews: same flow on iOS vs Android — list of platform-convention divergences.

## Skip If (ANY kills it)

- Greenfield strategic mobile design — start with research (interviews, diary studies) before applying basics; this knowledge is downstream.
- Native-only platform-specific work where Apple HIG / Material 3 are the primary reference — load those directly.
- Single-component visual polish — that is UI/visual design feedback, not mobile-UX methodology.
- No mobile users in the product's audience — effort is wasted on unused contexts.

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

- parent skill: `pro/ux/ux-researcher/`
