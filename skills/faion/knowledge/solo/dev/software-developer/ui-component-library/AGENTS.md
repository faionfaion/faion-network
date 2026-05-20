---
slug: ui-component-library
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Versioned, semver-controlled React component library with a layered structure (primitives → composite → patterns → layout), consistent prop API doctrine, design token integration, co-located Storybook stories + tests, and Radix UI/React Aria for interactive primitives.
content_id: "fda6367bddcdad09"
tags: [react, component-library, storybook, accessibility, design-tokens]
---
# UI Component Library

## Summary

**One-sentence:** Versioned, semver-controlled React component library with a layered structure (primitives → composite → patterns → layout), consistent prop API doctrine, design token integration, co-located Storybook stories + tests, and Radix UI/React Aria for interactive primitives.

**One-paragraph:** Versioned, semver-controlled React component library with a layered structure (primitives → composite → patterns → layout), consistent prop API doctrine, design token integration, co-located Storybook stories + tests, and Radix UI/React Aria for interactive primitives. Distinct from the shadcn copy-paste model — this methodology produces a packaged library.

## Applies If (ALL must hold)

- Multi-app monorepo that needs shared, versioned UI components (web, admin, mobile-web)
- Enforcing accessibility, theming, and prop API consistency via code review and audits
- Need semver-controlled exports consumed by multiple packages

## Skip If (ANY kills it)

- Single small app with no plans to share components — premature extraction adds overhead
- Heavy bespoke-per-page styling with low reuse (marketing landing pages, one-off campaigns)
- Replacing well-maintained external libraries (MUI, Mantine) without a clear extension story
- Team cannot commit to maintaining stories, tests, and tokens — the library will rot

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
