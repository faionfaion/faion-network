# Tailwind Architecture

## Summary

A utility-first CSS architecture for React/Vue/Svelte apps: design tokens live in `tailwind.config.ts` (or v4 `@theme`); all conditional class merging goes through a project-tuned `cn()` (`tailwind-merge` + `clsx`); variant-rich components use `cva` or `tv()`; `@apply` is restricted to `@layer components` only; `prettier-plugin-tailwindcss` enforces class order; `eslint-plugin-tailwindcss` blocks unknown utilities. Any duplicated 5+ utility chain across 3+ files becomes a primitive component.

## Why

Without `tailwind-merge`, conflicting utilities silently both apply. Without `cva`, variant logic explodes into ternary chains that are hard to extend. Without lint, dynamic class names (`bg-${color}-500`) silently break JIT purging in production. Centralizing tokens in config means one change propagates everywhere instead of grep-and-replace. Class ordering consistency makes diffs reviewable.

## When To Use

- Greenfield React/Vue/Svelte/Next.js apps where utility-first is the team standard
- Building design-token-driven Tailwind config for a multi-app design system
- Refactoring CSS Modules / styled-components / SCSS to Tailwind v3 / v4
- Auditing utility class chaos — extracting components, normalizing variants
- Wiring `tailwind-merge` + `cva` / `tv()` for variant-rich component libraries

## When NOT To Use

- Email HTML — CSS support is sparse, use inlining tools instead
- Strict CSP environments banning `style-src 'unsafe-inline'` for Tailwind's runtime
- Static-site generators with a hard 14KB CSS budget
- Server-rendered apps shipped to non-Tailwind designers maintaining handcrafted CSS

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture-rules.xml` | Token config rule, cn() rule, cva extraction threshold, @apply restriction |
| `content/02-antipatterns.xml` | Dynamic class purge failure, tailwind-merge drift, v3/v4 config mixing, deprecated opacity syntax |

## Templates

| File | Purpose |
|------|---------|
| `templates/cn.ts` | Project-tuned cn() helper combining clsx + tailwind-merge |
| `templates/tailwind.config.ts` | Design-token-driven config consuming Style Dictionary tokens |
| `templates/cva-variant-example.tsx` | Button component with cva variants (size, intent) + className passthrough |
