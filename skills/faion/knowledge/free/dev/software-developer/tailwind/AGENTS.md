---
slug: tailwind
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Utility-first CSS framework with JIT compilation; design tokens centralised in config; cn() + tailwind-merge resolves conflicts.
content_id: "eccdfbff4ca03e50"
complexity: light
produces: config
est_tokens: 3500
tags: [tailwind, css, styling, utility-first, design-tokens]
---
# Tailwind CSS

## Summary

**One-sentence:** Utility-first CSS framework with JIT compilation; design tokens centralised in config; cn() + tailwind-merge resolves conflicts.

**One-paragraph:** Utility-first CSS framework where styles are composed from atomic classes directly in markup. JIT compilation ships only the CSS classes actually used, keeping bundle size minimal. Centralising design tokens in tailwind.config prevents color/spacing drift across components. cn() + tailwind-merge resolves conflicting utilities and prevents className bugs.

**Ефективно для:** frontend-інженера, який стилізує компонентну систему — закриває петлю між дизайн-токенами в конфізі і композицією utility-класів у JSX без drift.

## Applies If (ALL must hold)

- Greenfield React / Vue / Svelte / Next.js / Astro projects needing utility-first styling.
- Design systems that need a single canonical token source.
- Component libraries that need consistent spacing/color/typography.
- Migrating off styled-components / emotion in favour of static CSS.

## Skip If (ANY kills it)

- Existing app deeply invested in CSS-in-JS — incremental migration only.
- Pure backend service.
- Animation-heavy work where CSS animations need full custom property control.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tailwind 4+ installed | package | npm i -D tailwindcss |
| tailwind.config.ts or @tailwind directives | TS/CSS | repo root |
| PostCSS or Vite | config | build pipeline |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/typescript-strict-mode` | Token types and cn() helper benefit from strict TS. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: tokens in config not in components, cn() + tailwind-merge for conditionals, no @apply for one-off styles, mobile-first responsive prefixes, dark mode via CSS variable strategy. | ~900 |
| `content/02-output-contract.xml` | essential | Shape: tailwind.config.ts with theme.extend; components compose utility strings via cn(); no inline style props with token-equivalent values. Forbidden: hardcoded #hex when token exists, @apply for one-off, classnames lib without merge. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: hardcoded colors/spacing in components, @apply abuse, classnames-without-merge, dynamic class string concatenation. | ~700 |
| `content/04-procedure.xml` | medium | Steps: install tailwind → declare tokens in config → author cn() helper → compose component classes → wire dark mode → audit drift. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: token exists? → use utility. One-off value? → arbitrary [value]. Conditional? → cn(). Repeated component pattern? → extract to component, not @apply. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-token-config` | haiku | Template fill. |
| `audit-class-drift` | sonnet | Detect hardcoded values that should be tokens. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.ts` | Tokens (colors, spacing, typography) declared via theme.extend. |
| `templates/cn.ts` | cn() helper combining clsx + tailwind-merge. |
| `templates/Component.tsx` | Component composing utilities via cn() with conditional variants. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tailwind.py` | Detect hardcoded hex / px values in JSX that have token equivalents; flag @apply outside utility layer. | Pre-commit. |

## Related

- [[typescript-strict-mode]]
- [[storybook-setup]]

## Decision tree

The tree at content/06-decision-tree.xml decides utility vs arbitrary value vs token addition, and cn() vs raw template string composition. Walk it any time a component needs a non-trivial className.
