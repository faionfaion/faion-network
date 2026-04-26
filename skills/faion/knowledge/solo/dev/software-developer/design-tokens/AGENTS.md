# Design Tokens

## Summary

Design tokens are the atomic values of a design system — colors, spacing, typography, shadows — stored as structured data with a three-tier hierarchy: primitive (raw values) → semantic (purpose-based aliases) → component (usage-specific). One JSON source of truth emits per-platform outputs (CSS vars, JS constants, iOS Swift, Android XML) via Style Dictionary.

## Why

Without tokens, hardcoded hex values and magic numbers scatter across codebases, making theming impossible and brand changes surgical nightmares. The three-tier model separates "what the value is" from "what it means" from "where it's used," allowing dark mode, white-labeling, and platform consistency without forking components. Agents benefit because they pick values from a constrained vocabulary instead of inventing hex literals.

## When To Use

- Building or extending a design system for web + mobile
- Introducing dark mode or white-label theming
- Bridging Figma to code so design and engineering stay in sync
- Standardizing brand across multiple apps in a monorepo
- Connecting a token pipeline to Tailwind config or platform constants

## When NOT To Use

- Single one-off marketing page — overhead beats payoff
- Apps fully delegating to a UI library (Material, Mantine) with no re-skinning
- Prototype work where designers iterate hourly — token churn outpaces pipeline cost
- Pure server-rendered emails using external template SaaS that owns tokens

## Content

| File | What's inside |
|------|---------------|
| `content/01-token-hierarchy.xml` | Three-tier model, naming rules, JSON structure for primitive/semantic/component tokens |
| `content/02-rules-and-antipatterns.xml` | Concrete rules for naming, generation, contrast, versioning; antipatterns to avoid |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-tokens.mjs` | Style Dictionary pipeline emitting CSS vars + JS ES6 + iOS Swift from token JSON |
| `templates/primitive.json` | Primitive token JSON structure (colors, spacing, font, radius, shadow) |
| `templates/semantic.json` | Semantic token JSON (light theme aliases referencing primitives) |
