---
slug: shadcn-ui
tier: solo
group: dev
domain: frontend-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: shadcn/ui is a copy-in component system: primitives are copied to components/ui/ via the CLI (npx shadcn@latest add), not installed as an npm dependency.
content_id: "0d4fb80a35d6d1f5"
tags: [shadcn-ui, components, tailwind, radix, accessibility]
---
# shadcn/ui

## Summary

**One-sentence:** shadcn/ui is a copy-in component system: primitives are copied to components/ui/ via the CLI (npx shadcn@latest add), not installed as an npm dependency.

**One-paragraph:** shadcn/ui is a copy-in component system: primitives are copied to components/ui/ via the CLI (npx shadcn@latest add), not installed as an npm dependency. Components are built on Radix headless primitives for accessibility, styled with Tailwind using CSS variable tokens (HSL triplets, not hex) in globals.css, and composed into feature components under components/<feature>/. Never edit components/ui/ after the initial add — treat it as vendored.

## Applies If (ALL must hold)

- React app on Tailwind needing a stylable, accessible component baseline you can fork freely.
- Greenfield SaaS or dashboards where you control design tokens via CSS variables.
- Design system in flux: copy-in lets each project diverge without npm dep drift.
- You want Radix primitives' a11y wiring without committing to a closed component library.

## Skip If (ANY kills it)

- Non-React stacks (Vue, Svelte, vanilla) — community ports lack agent-friendly tooling.
- Need vendor-supported components with SLAs — use MUI, Mantine, or Ant Design.
- Strict design system with zero tolerance for upstream drift; each copy creates a fork.
- Extreme bundle-size constraints; CVA + tailwind-merge add measurable overhead.

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
