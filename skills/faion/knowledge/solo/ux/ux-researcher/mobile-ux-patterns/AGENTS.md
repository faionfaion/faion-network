---
slug: mobile-ux-patterns
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Mobile-specific UI patterns for navigation (tab bars, hamburger menus), forms (progressive disclosure, inline validation), interactions (pull-to-refresh, swipe actions, long-press), loading states (skeleton screens), empty states, error recovery, and onboarding.
content_id: "eea1c2809014e13c"
tags: [mobile, patterns, ios, android, design]
---
# Mobile UX Patterns & Templates

## Summary

**One-sentence:** Mobile-specific UI patterns for navigation (tab bars, hamburger menus), forms (progressive disclosure, inline validation), interactions (pull-to-refresh, swipe actions, long-press), loading states (skeleton screens), empty states, error recovery, and onboarding.

**One-paragraph:** Mobile-specific UI patterns for navigation (tab bars, hamburger menus), forms (progressive disclosure, inline validation), interactions (pull-to-refresh, swipe actions, long-press), loading states (skeleton screens), empty states, error recovery, and onboarding. Each pattern includes specifications for iOS and Android with touch targets, animations, and accessibility guidelines.

## Applies If (ALL must hold)

- Designing mobile features for iOS or Android that need proven interaction models.
- Auditing an existing mobile app against platform guidelines (Apple HIG, Material Design) before launch.
- Documenting a new mobile pattern for a design system so it is reproducible across teams.
- Evaluating mobile UX debt—mapping deviations from established patterns to prioritize fixes.
- Training engineers on mobile conventions when building native components.

## Skip If (ANY kills it)

- When the product's core differentiator is a custom interaction model (e.g., gesture-first apps)—force-fitting standard patterns may reduce the differentiator.
- Designing for novel form factors (foldables, wearables, AR) where established mobile patterns do not apply.
- As a substitute for testing on real devices with real users—pattern compliance does not equal usability for your specific context.

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

- parent skill: `solo/ux/ux-researcher/`
