---
slug: shadcn-ui-architecture
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Copy-into-codebase component architecture using shadcn/ui: Radix UI primitives + Tailwind + CVA variants.
content_id: "f7d94871947a236f"
tags: [shadcn, ui-components, radix, tailwind, design-tokens]
---
# shadcn/ui Component Architecture

## Summary

**One-sentence:** Copy-into-codebase component architecture using shadcn/ui: Radix UI primitives + Tailwind + CVA variants.

**One-paragraph:** Copy-into-codebase component architecture using shadcn/ui: Radix UI primitives + Tailwind + CVA variants. The team owns the component source (not an npm dependency). Primitives live in `components/ui/` (protected); feature compositions reference them from `components/<feature>/`. Design tokens live in CSS variables in `globals.css`.

## Applies If (ALL must hold)

- Bootstrapping a Tailwind + Radix design system on Next.js, Remix, Vite+React, or Astro
- Solo/small teams that need to fork and tweak primitives without upstream coupling
- Projects where an agent can scaffold via the official CLI and layer compositions on top
- Products that need dark mode theming via CSS custom properties

## Skip If (ANY kills it)

- Vue, Svelte, Solid — use the framework-specific port (shadcn-vue, shadcn-svelte) instead
- Regulated environments requiring versioned, audited UI dependencies with full supply-chain provenance
- Teams that want semver-guaranteed components — shadcn is a starter, not a maintained dependency
- Purely static layouts with no interactive behavior — a CSS-only kit is lighter

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
