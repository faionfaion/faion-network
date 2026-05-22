---
slug: tailwind
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Tailwind CSS is a utility-first framework configured via tailwind.
content_id: "eccdfbff4ca03e50"
tags: [tailwind, css, utility-first, design-tokens, styling]
---
# Tailwind CSS

## Summary

**One-sentence:** Tailwind CSS is a utility-first framework configured via tailwind.

**One-paragraph:** Tailwind CSS is a utility-first framework configured via tailwind.config.ts (v3) or a CSS-first @theme block (v4). Configure content globs explicitly to include all templates; theme tokens (colors, spacing, radii) live in the config or @theme, never as hardcoded hex in components. Use prettier-plugin-tailwindcss to canonicalize class order. @apply is allowed only in globals.css for thin reset helpers (≤3 utilities) — abstractions belong in components.

## Applies If (ALL must hold)

- Greenfield app or rewrite where you control HTML and want utility-first styling.
- Multi-developer or multi-agent project needing a stable, greppable styling surface.
- Fast iteration on visual design with token control via config.
- Pairing with React, Vue, Svelte, or HTMX where templating lives near markup.

## Skip If (ANY kills it)

- Brownfield app with mature CSS-in-JS or BEM conventions — mixing causes specificity wars.
- Email templates, PDFs, or print-first surfaces (Tailwind's reset and JIT do not target these).
- Library/SDK shipping CSS — utility classes leak global resets onto consumer apps.
- Strict design system that bans "magic numbers" — utilities make ad-hoc spacing too easy.

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
