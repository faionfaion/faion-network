# Tailwind Patterns

## Summary

Tailwind Patterns covers reusable variant composition on top of an existing Tailwind project using
`cva()` (class-variance-authority) for type-safe variant definitions and `cn()` (clsx +
tailwind-merge) for conflict-safe class merging. Every component has one `cva()` block next to it;
variants describe intent (`tone="danger"`) not style (`color="red"`). Dynamic class interpolation
(`bg-${color}-500`) is forbidden — JIT purges interpolated strings.

## Why

Raw utility strings copied across components defeat the utility-first value proposition. `cva()`
turns variant logic into a typed API that agents can extend without introducing class conflicts or
Tailwind-merge collisions. The pattern also makes components friendly to visual regression:
Storybook can matrix every variant automatically.

## When To Use

- Existing Tailwind project needing reusable variant patterns (button, badge, card, input) without
  pulling in a UI library.
- Type-safe class composition via `cva()` + `cn()` for AI-generated components.
- Migrating ad-hoc utility soup into named components without giving up utility-first.
- Building a private design system on top of Tailwind for a single product.

## When NOT To Use

- Project does not yet have Tailwind configured — start with the `tailwind` methodology first.
- Static marketing site that ships once and is never refactored; raw utilities are fine.
- Team prefers CSS Modules or styled-components — mixing paradigms doubles the surface area.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Rules: one cva() per component, intent-based variant names, no dynamic interpolation, cn() mandatory, data-* selectors. |
| `content/02-patterns.xml` | Button, Input, Card, dark mode, animation patterns using cva() and cn(). |

## Templates

| File | Purpose |
|------|---------|
| `templates/cn.ts` | Canonical cn() helper (clsx + tailwind-merge). |
| `templates/button.tsx` | Full Button component with cva() variants (primary, secondary, outline, ghost, danger) and sizes. |
| `templates/input.tsx` | Input component with label, error, hint, aria wiring, and cva() state variants. |
| `templates/check-no-interp-classes.sh` | CI guard: fail on dynamic Tailwind class interpolation. |
