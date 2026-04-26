# Tailwind CSS

## Summary

Utility-first CSS framework where styles are composed from atomic classes directly in markup. Design tokens live in `tailwind.config.ts` `theme.extend`; components are composed via the `cn()` helper (`clsx` + `tailwind-merge`) and variant APIs (CVA / tailwind-variants). Class order follows the Concentric CSS convention: layout → box → border → bg → typography → effects.

## Why

JIT compilation ships only the CSS classes actually used, keeping bundle size minimal. Centralizing tokens in config prevents color/spacing drift across components. `cn()` + `tailwind-merge` resolves conflicting utilities and prevents className bugs. Agents pattern-match Tailwind reliably, making LLM-driven UI work predictable.

## When To Use

- Greenfield React / Vue / Svelte / Next.js / Astro projects needing utility-first styling.
- Design systems that need a single canonical token source.
- Component libraries built on shadcn/ui / Radix / Headless UI.
- LLM-driven UI: agents produce consistent Tailwind output.

## When NOT To Use

- Rails Asset Pipeline + Sass mixins or other server-rendered CSS architectures — doubles CSS strategy.
- Highly dynamic class strings (`bg-${color}-500`) — JIT purges them; use CSS Modules instead.
- Designer-owned codebases where designers write Sass — requires designer fluency in tokens.
- Print stylesheets — a dedicated `print.css` is cleaner than Tailwind print variants.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Utility-first principles, class ordering, design-token rules, `@apply` limits. |
| `content/02-patterns.xml` | `cn()` helper, variant pattern, responsive design, dark mode, common layout snippets. |
| `content/03-antipatterns.xml` | Inline styles, dynamic class strings, `@apply` overuse, arbitrary-value creep, safelist misuse. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.ts` | Config with semantic color tokens (CSS variables), custom spacing, typography, plugins. |
| `templates/cn-helper.ts` | `cn()` utility combining `clsx` + `tailwind-merge`. |
| `templates/cva-variant.tsx` | CVA-based component variant pattern. |
| `templates/css-budget.sh` | CI script: fail build if prod CSS exceeds gzipped budget. |
