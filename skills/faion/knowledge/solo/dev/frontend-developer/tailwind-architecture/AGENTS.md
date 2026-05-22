---
slug: tailwind-architecture
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for structuring Tailwind CSS in production React/Next.
content_id: "c1e1a963e330cd87"
tags: [tailwind, architecture, design-tokens, css-variables, component-variants]
---
# Tailwind Architecture in Production

## Summary

**One-sentence:** Patterns for structuring Tailwind CSS in production React/Next.

**One-paragraph:** Patterns for structuring Tailwind CSS in production React/Next.js apps. Covers utility-first composition with a `cn()` merge helper, class ordering (concentric CSS), variant patterns, design token mapping via CSS variables in `tailwind.config.js`, disciplined `@apply` usage, and CSS layer management.

## Applies If (ALL must hold)

- Greenfield React / Next.js / Vue / Svelte / Astro projects committing to utility-first CSS as the single styling layer for the lifetime of the codebase.
- Design-system codification: consolidating brand tokens (colors, spacing, type, radii) into `tailwind.config.ts` `theme.extend` plus CSS variables for runtime theming.
- shadcn/ui-based component libraries — Tailwind is the assumed substrate for Radix/Headless UI primitives.
- LLM-driven UI authoring — agents pattern-match Tailwind utilities reliably and produce predictable bundle output.
- Multi-package monorepos that need a shared `tailwind-config` package consumed by app, marketing site, email templates, and Storybook.

## Skip If (ANY kills it)

- Apps with established server-rendered CSS pipelines (Rails Asset Pipeline + Sass partials, Phoenix LiveView component libs) where bolting on Tailwind doubles the styling strategy.
- Print-heavy outputs (PDFs, invoices) — Tailwind's `print:` variants exist but a dedicated `print.css` is cleaner and easier to audit.
- Codebases where most styling is highly dynamic (`bg-${brandColor}-${shade}`) — JIT purge will silently delete classes; CSS Modules + CSS variables are simpler.
- Teams shipping a CSS-Modules / vanilla-extract migration in flight; mixing layers regresses bundle predictability.
- Tiny static sites where hand-written CSS (<2KB) beats the Tailwind toolchain overhead.

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
