# shadcn/ui Component Architecture

## Summary

Copy-into-codebase component architecture using shadcn/ui: Radix UI primitives + Tailwind + CVA variants. The team owns the component source (not an npm dependency). Primitives live in `components/ui/` (protected); feature compositions reference them from `components/<feature>/`. Design tokens live in CSS variables in `globals.css`.

## Why

shadcn gives accessible Radix primitives with CVA-driven variant management without the semver coupling of a library. Teams can fork and modify any component. The MCP server lets agents scaffold via `npx shadcn@latest add` without hand-writing boilerplate. Tailwind CSS variable tokens provide theme-ability and dark mode without hardcoded color values.

## When To Use

- Bootstrapping a Tailwind + Radix design system on Next.js, Remix, Vite+React, or Astro
- Solo/small teams that need to fork and tweak primitives without upstream coupling
- Projects where an agent can scaffold via the official CLI and layer compositions on top
- Products that need dark mode theming via CSS custom properties

## When NOT To Use

- Vue, Svelte, Solid — use the framework-specific port (shadcn-vue, shadcn-svelte)
- Regulated environments requiring versioned, audited UI dependencies with full supply-chain provenance
- Teams that want semver-guaranteed components — shadcn is a starter, not a maintained dependency
- Purely static layouts with no interactive behavior — a CSS-only kit is lighter

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Directory structure, token rules, variant design with CVA, component protection rules |
| `content/02-patterns.xml` | Primitive, composition, and compound component patterns; theming; anti-patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/scaffold.sh` | Bulk-scaffold shadcn primitives and generate barrel export |
