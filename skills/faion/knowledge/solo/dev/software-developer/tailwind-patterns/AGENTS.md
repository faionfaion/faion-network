# Tailwind Patterns

## Summary

Utility-first CSS methodology for building component-based UIs with Tailwind CSS. Uses `cva` for type-safe variants, `tailwind-merge`+`clsx` for class merging, and `tailwind.config.ts` tokens as the single source of truth. Every color and spacing value must map to a design token; arbitrary values (`w-[37px]`) are forbidden without justification.

## Why

Utility classes close the vocabulary: agents generate predictable, JIT-purge-safe class strings. Combined with `cva`, variant logic is explicit and diffable rather than buried in ternaries. Tailwind's config-driven tokens prevent style drift across teams and LLM-generated components.

## When To Use

- Building or maintaining React/Vue/Svelte/Next.js component libraries with utility-first CSS.
- Implementing a design system via `tailwind.config.ts` tokens (colors, spacing, typography, radii).
- Migrating from CSS-in-JS (Emotion, styled-components) to a build-time, SSR-friendly stack.
- LLM-driven UI generation where the styling vocabulary must be closed and predictable.
- shadcn/ui, daisyUI, or headless-UI workflows.

## When Not To Use

- Static brochureware where Tailwind's bundle and toolchain outweigh value; vanilla CSS suffices.
- Apps with deep runtime theming (per-tenant themes with hundreds of colors that don't map to tokens).
- Email templates — utility classes don't survive email clients; use MJML/react-email instead.
- Teams that strongly prefer scoped CSS or BEM.
- Projects whose component output must be CSS-class-free (web components without Shadow DOM utilities).

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Core rules: cn() helper, cva variants, responsive grid, dark mode, @apply usage. |
| `content/02-antipatterns.xml` | Failure modes: arbitrary values, class duplication, dynamic class purge, dark-mode omission. |

## Templates

| File | Purpose |
|------|---------|
| `templates/button-cva.tsx` | Button component scaffold with cva variants and cn() merger. |
| `templates/tailwind.config.ts` | Tailwind config with brand tokens, dark mode class strategy, plugins. |
| `templates/tw-dupes.sh` | Script to find className strings duplicated across 3+ components. |
