---
slug: design-tokens-fundamentals
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design tokens are named, platform-agnostic values (colors, spacing, typography) organized in a three-tier hierarchy — global (raw values) → semantic (intent aliases) → component (scoped) — that enable consistent theming, dark mode, and single-source-of-truth updates across platforms.
content_id: "cab4ee38609b44a1"
tags: [design-tokens, design-systems, theming, dark-mode, css-variables]
---
# Design Tokens Fundamentals

## Summary

**One-sentence:** Design tokens are named, platform-agnostic values (colors, spacing, typography) organized in a three-tier hierarchy — global (raw values) → semantic (intent aliases) → component (scoped) — that enable consistent theming, dark mode, and single-source-of-truth updates across platforms.

**One-paragraph:** Design tokens are named, platform-agnostic values (colors, spacing, typography) organized in a three-tier hierarchy — global (raw values) → semantic (intent aliases) → component (scoped) — that enable consistent theming, dark mode, and single-source-of-truth updates across platforms. A governed token layer ensures that renaming a primary color propagates everywhere and that Figma and code stay synchronized.

## Applies If (ALL must hold)

- Setting up a new design system from scratch (tokens are the foundation before any component library)
- Adding dark mode, theme switching, or white-label support to an existing codebase
- Auditing a codebase for hardcoded color/spacing/font values that should be tokenized
- Migrating from inline Tailwind classes or CSS magic numbers to a governed token layer
- Generating token documentation from a Figma Variables export or Style Dictionary config

## Skip If (ANY kills it)

- Single-component quick fixes — token infrastructure has setup cost not worth it for one-off styling
- Projects with a single theme and no planned theming requirements
- When the design tool (Figma) and codebase are not synchronized — tokens create false confidence if sources diverge
- Legacy jQuery / server-rendered projects without a CSS variable pipeline

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

- parent skill: `solo/ux/ui-designer/`
