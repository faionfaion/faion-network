# shadcn/ui

## Summary

shadcn/ui is a component system where primitives are copied into `components/ui/` (not installed as a package), styled with Tailwind CSS, managed with CVA variants, and built on Radix Primitives. Core rule: never modify `components/ui/` files directly — extend via composition in `components/<feature>/`; use `cn()` as the only class merger; add `'use client'` only on leaf components that actually need state.

## Why

Owning component source eliminates vendor lock-in and lets agents edit component files directly. CSS variables in `globals.css` provide full dark-mode and brand control without hardcoded colors. Radix Primitives handle accessibility (focus management, ARIA, keyboard nav) so custom logic doesn't regress it. The copy-not-install model means upstream bug fixes require explicit import via `npx shadcn diff`, preventing silent regressions.

## When To Use

- New React/Next.js apps needing design-system primitives without locking into a third-party version.
- Internal tools / dashboards where Tailwind + Radix + CVA is the established stack.
- LLM-driven UI work where agents need to edit component files (not opaque npm packages).
- Branding-heavy products requiring full CSS variable control.
- Migrating off Material UI / Chakra UI / Mantine.

## When NOT To Use

- Apps needing a fully maintained, versioned external component package — shadcn intentionally is not one.
- Non-React stacks (Vue, Svelte, Angular) — use respective ports with their own docs.
- Mobile-first React Native — shadcn assumes web DOM + Tailwind.
- Fast prototyping where zero-design speed matters more than ownership.
- Teams without Tailwind discipline — onboarding cost for `cn()` + CVA is real.

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | Directory structure, primitive vs composition pattern, CVA variant management. |
| `content/02-theming.xml` | CSS variable setup, dark mode, design token discipline. |
| `content/03-forms.xml` | shadcn Form + react-hook-form + zod integration pattern. |
| `content/04-antipatterns.xml` | Hallucinated imports, `use client` over-application, inline colors, forwardRef loss. |

## Templates

| File | Purpose |
|------|---------|
| `templates/globals.css` | CSS variable theme skeleton (light + dark). |
| `templates/cn-util.ts` | `cn()` utility combining `clsx` + `tailwind-merge`. |
| `templates/shadcn-drift-check.sh` | Weekly CI script detecting local divergence from upstream registry. |
