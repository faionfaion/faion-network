# shadcn/ui

## Summary

shadcn/ui is a copy-in component system: primitives are copied to `components/ui/` via the CLI
(`npx shadcn@latest add`), not installed as an npm dependency. Components are built on Radix
headless primitives for accessibility, styled with Tailwind using CSS variable tokens (HSL
triplets, not hex) in `globals.css`, and composed into feature components under
`components/<feature>/`. Never edit `components/ui/` after the initial add — treat it as vendored.

## Why

Copy-in gives full ownership without an npm upgrade path, while Radix wires all ARIA and keyboard
behavior automatically. CSS variable theming (`--primary: 221 83% 53%`) enables dark mode and
brand switching in one file. The `cva()` + `cn()` pattern provides type-safe variant composition
without runtime overhead.

## When To Use

- React app on Tailwind needing a stylable, accessible component baseline you can fork freely.
- Greenfield SaaS or dashboards where you control design tokens via CSS variables.
- Design system in flux: copy-in lets each project diverge without npm dep drift.
- You want Radix primitives' a11y wiring without committing to a closed component library.

## When NOT To Use

- Non-React stacks (Vue, Svelte, vanilla) — community ports lack agent-friendly tooling.
- Need vendor-supported components with SLAs — use MUI, Mantine, or Ant Design.
- Strict design system with zero tolerance for upstream drift; each copy creates a fork.
- Extreme bundle-size constraints; CVA + tailwind-merge add measurable overhead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Rules: treat ui/ as vendored, CSS variable tokens only, cva() for variants, cn() mandatory, feature component prefixing. |
| `content/02-examples.xml` | Button (CVA), compound Card, dark mode globals.css, Server Component "use client" gotcha. |

## Templates

| File | Purpose |
|------|---------|
| `templates/globals.css` | CSS variable theme block for light and dark mode (HSL triplets). |
| `templates/cn.ts` | Canonical `cn()` helper using clsx + tailwind-merge. |
| `templates/check-shadcn-pristine.sh` | CI guard: fail if `components/ui/*` was hand-edited outside the allowlist. |
