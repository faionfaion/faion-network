# shadcn/ui Architecture

## Summary

shadcn/ui components are vendored (copied, not installed as packages) into `components/ui/`. The architecture enforces three strict layers: `ui/` primitives are mutated only via `npx shadcn add`; `components/<feature>/` composes from `ui/`; `lib/` holds pure utilities. All variants use `cva()`. Theme via CSS variables only — no hex literals in feature components.

## Why

Without layer guards, agents edit `components/ui/button.tsx` directly to "fix one thing", breaking future `shadcn diff` upgrades. CI import rules (`dependency-cruiser` or `eslint-plugin-boundaries`) make the contract enforceable rather than social.

## When To Use

- Mid-to-large React + Tailwind app using shadcn/ui that needs directory ownership rules.
- Multiple agents or teams contributing components — prevents `ui/` becoming a junk drawer.
- Migrating from a closed UI library into a layered primitives → composite → feature structure.
- Monorepo where shadcn primitives live in a shared `packages/ui/`.

## When NOT To Use

- App with fewer than 20 components — flat `components/` is simpler.
- Stack is not React + Tailwind; these rules assume both.
- Project uses MUI/Mantine; different composition patterns apply.
- Pre-shadcn-init phase; set up `shadcn-ui` methodology first, then add architecture rules.

## Content

| File | What's inside |
|------|---------------|
| `content/01-layers.xml` | Three-layer contract, directory layout, `cn()` helper, CSS variable theming, multi-tenant scoping. |
| `content/02-rules.xml` | CVA variant rule, forwardRef, `"use client"` placement, monorepo `--cwd` flag, upgrade via `shadcn diff`. |
| `content/03-antipatterns.xml` | Editing ui/ directly, hardcoded hex, missing use-client, broken path aliases, cn() not imported. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dependency-cruiser.cjs` | Import layer guard: primitives must not import features; no cross-feature imports. |
| `templates/cn.ts` | Canonical `cn()` helper using clsx + tailwind-merge. |

## Scripts

none
