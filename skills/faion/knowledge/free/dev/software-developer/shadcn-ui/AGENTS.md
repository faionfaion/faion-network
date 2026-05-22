---
slug: shadcn-ui
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: shadcn/ui is a component system where primitives are copied into `components/ui/` (not installed as a package), styled with Tailwind CSS, managed with CVA variants, and built on Radix Primitives.
content_id: "0d4fb80a35d6d1f5"
tags: [shadcn, react, tailwind, radix, cva]
---
# shadcn/ui

## Summary

**One-sentence:** shadcn/ui is a component system where primitives are copied into `components/ui/` (not installed as a package), styled with Tailwind CSS, managed with CVA variants, and built on Radix Primitives.

**One-paragraph:** shadcn/ui is a component system where primitives are copied into `components/ui/` (not installed as a package), styled with Tailwind CSS, managed with CVA variants, and built on Radix Primitives. Core rule: never modify `components/ui/` files directly — extend via composition in `components/<feature>/`; use `cn()` as the only class merger; add `'use client'` only on leaf components that actually need state.

## Applies If (ALL must hold)

- New React/Next.js apps that need design-system primitives without locking into a third-party library version. Code is copied into the codebase, owned by the team.
- Internal tools / dashboards where Tailwind + Radix Primitives + CVA is already the stack.
- LLM-driven UI work — components are local TypeScript files agents can edit, not opaque npm packages they cannot reshape.
- Branding-heavy products where design tokens (`globals.css` CSS vars) need full control.
- Migration off Material UI / Chakra UI / Mantine where vendor lock-in or bundle size hurts.

## Skip If (ANY kills it)

- Apps that need a fully maintained, versioned component package — shadcn intentionally is not a package. You own bug fixes.
- Non-React stacks (Vue, Svelte, Angular). Use respective ports (`shadcn-vue`, `shadcn-svelte`) — same philosophy, different repo.
- Mobile-first React Native — shadcn assumes web DOM + Tailwind.
- Fast prototyping where you want zero design — fully designed kits (Mantine, Material) ship faster.
- Teams without Tailwind discipline — shadcn requires Tailwind config + `cn()` utility + understanding of CVA. Onboarding cost.

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

- parent skill: `free/dev/software-developer/`
