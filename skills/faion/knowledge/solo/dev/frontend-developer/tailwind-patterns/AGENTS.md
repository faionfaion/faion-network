---
slug: tailwind-patterns
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Tailwind Patterns covers reusable variant composition on top of an existing Tailwind project using `cva()` (class-variance-authority) for type-safe variant definitions and `cn()` (clsx + tailwind-merge) for conflict-safe class merging.
content_id: "d8efb6c8eb1057ee"
tags: [tailwind, cva, variants, components, design-patterns]
---
# Tailwind Patterns with CVA

## Summary

**One-sentence:** Tailwind Patterns covers reusable variant composition on top of an existing Tailwind project using `cva()` (class-variance-authority) for type-safe variant definitions and `cn()` (clsx + tailwind-merge) for conflict-safe class merging.

**One-paragraph:** Tailwind Patterns covers reusable variant composition on top of an existing Tailwind project using `cva()` (class-variance-authority) for type-safe variant definitions and `cn()` (clsx + tailwind-merge) for conflict-safe class merging. Every component has one `cva()` block next to it; variants describe intent (`tone="danger"`) not style (`color="red"`). Dynamic class interpolation (`bg-${color}-500`) is forbidden — JIT purges interpolated strings.

## Applies If (ALL must hold)

- Existing Tailwind project needing reusable variant patterns (button, badge, card, input) without pulling in a UI library.
- Type-safe class composition via `cva()` + `cn()` for AI-generated components.
- Migrating ad-hoc utility soup into named components without giving up utility-first.
- Building a private design system on top of Tailwind for a single product.

## Skip If (ANY kills it)

- Project does not yet have Tailwind configured — start with the `tailwind` methodology first.
- Static marketing site that ships once and is never refactored; raw utilities are fine.
- Team prefers CSS Modules or styled-components — mixing paradigms doubles the surface area.

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
