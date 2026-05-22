---
slug: ui-lib-patterns
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced patterns for UI libraries: compound components, accessible modal portals, and Storybook CSF 3 stories with testing.
content_id: "ddfdcb74cbc2439a"
tags: [react, components, ui-libraries, storybook, accessibility]
---
# UI Library Advanced Patterns

## Summary

**One-sentence:** Advanced patterns for UI libraries: compound components, accessible modal portals, and Storybook CSF 3 stories with testing.

**One-paragraph:** Advanced patterns for UI libraries: compound components, accessible modal portals, and Storybook CSF 3 stories with testing. Ship primitives as 4-file units.

## Applies If (ALL must hold)

- Building compound components (Tabs, Accordion, Card) for an in-house UI library.
- Implementing accessible Modal/Dialog/Popover with portal, focus trap, ESC handling.
- Producing a Component.stories.tsx for every primitive in a Storybook-backed library.
- Migrating a one-off component into a reusable, typed library entry.

## Skip If (ANY kills it)

- One-off page UI that will never be reused — compound pattern adds context overhead with no payoff.
- Apps already using Radix UI or React Aria — wrap those instead of re-implementing dialog semantics.
- Server Components-only trees: compound components rely on React context, requiring 'use client'.

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
