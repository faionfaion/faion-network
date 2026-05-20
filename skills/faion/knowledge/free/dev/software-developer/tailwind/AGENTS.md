---
slug: tailwind
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Utility-first CSS framework where styles are composed from atomic classes directly in markup.
content_id: "eccdfbff4ca03e50"
tags: [tailwind, css, styling, utility-first, design-tokens]
---
# Tailwind CSS

## Summary

**One-sentence:** Utility-first CSS framework where styles are composed from atomic classes directly in markup.

**One-paragraph:** Utility-first CSS framework where styles are composed from atomic classes directly in markup. JIT compilation ships only the CSS classes actually used, keeping bundle size minimal. Centralizing tokens in config prevents color/spacing drift across components. `cn()` + `tailwind-merge` resolves conflicting utilities and prevents className bugs.

## Applies If (ALL must hold)

- Greenfield React / Vue / Svelte / Next.js / Astro projects needing utility-first styling.
- Design systems that need a single canonical token source.
- Component libraries built on shadcn/ui / Radix / Headless UI.
- LLM-driven UI: agents produce consistent Tailwind output.

## Skip If (ANY kills it)

- Rails Asset Pipeline + Sass mixins or other server-rendered CSS architectures — doubles CSS strategy.
- Highly dynamic class strings (`bg-${color}-500`) — JIT purges them; use CSS Modules instead.
- Designer-owned codebases where designers write Sass — requires designer fluency in tokens.
- Print stylesheets — a dedicated `print.css` is cleaner than Tailwind print variants.

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
