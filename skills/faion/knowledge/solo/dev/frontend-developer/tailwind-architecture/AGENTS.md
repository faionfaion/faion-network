# Tailwind Architecture

## Summary

Patterns for structuring Tailwind CSS in production React/Next.js apps. Covers utility-first composition with a `cn()` merge helper, class ordering (concentric CSS), variant patterns, design token mapping via CSS variables in `tailwind.config.js`, disciplined `@apply` usage, and CSS layer management.

## Why

Unstructured Tailwind class strings become maintenance nightmares: merge conflicts on long class lists, specificity bugs from `@apply` overuse, and inconsistent ordering that makes diffs noisy. The concentric ordering and `cn()` helper eliminate class conflicts; centralising tokens in config prevents raw hex/px values from leaking into JSX; limiting `@apply` to `@layer components` keeps CSS bundle size predictable.

## When To Use

- Structuring a new Tailwind project from scratch
- Refactoring an existing project with inconsistent class ordering or frequent style conflicts
- Setting up dark mode or multi-theme support
- Adding a design token layer to an existing Tailwind config

## When NOT To Use

- Projects already committed to CSS Modules or styled-components — mixing paradigms adds complexity
- When the design system is token-driven from a separate source (e.g. Style Dictionary) and Tailwind is only a thin utility layer — token sync setup may not be worth it
- Micro-frontends where each team owns its own CSS strategy

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-patterns.xml` | cn() helper, variant patterns, responsive (mobile-first), concentric class ordering |
| `content/02-config-tokens.xml` | tailwind.config.js token mapping, CSS variables, @apply rules, CSS layers, dark mode |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.js` | Production config with semantic color/spacing tokens via CSS variables |
| `templates/utils.ts` | cn() helper (clsx + tailwind-merge) |
