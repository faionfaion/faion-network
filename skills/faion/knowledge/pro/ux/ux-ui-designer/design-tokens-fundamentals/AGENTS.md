# Design Tokens Fundamentals

## Summary

Design tokens are named, platform-agnostic values (colors, spacing, typography) organized in three tiers: primitive (raw values) → semantic (purpose-named aliases) → component (component-scoped). Components must reference only semantic tokens, never primitive. Token names must express purpose, not appearance (`color.text.muted`, not `color.gray.600`). Emit W3C DTCG JSON and generate platform outputs via Style Dictionary.

## Why

Ad-hoc CSS variables and Tailwind configs create designer-developer drift: values in Figma diverge from code within one sprint. Three-tier token architecture with a CI contrast-lint step keeps a single source of truth across web, iOS, Android, and visionOS surfaces. Semantic naming makes dark/high-contrast mode swaps possible without touching component code.

## When To Use

- Bootstrapping a design system targeting two or more platforms.
- Migrating from ad-hoc CSS variables to a single source of truth.
- Adding dark/light/high-contrast modes to a shipped product.
- Designer-developer round-trip workflows where Figma values drift from code.
- Multi-brand white-label products that need theme swaps without rebuild.

## When NOT To Use

- Single-page MVP with one designer/developer — overhead exceeds value until month 3+.
- Static two-page marketing site — Tailwind defaults suffice.
- Throwaway internal tools with no design-language target.
- Teams that haven't agreed on semantic naming yet — resolve naming first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-token-structure.xml` | Three-tier model, token type definitions, W3C DTCG JSON schema example. |
| `content/02-rules-and-antipatterns.xml` | Naming rules, contrast-pairing rule, depth limit rule, antipatterns, agentic gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens-skeleton.json` | W3C DTCG 3-tier token skeleton (primitive / semantic / component). |
| `templates/token-contrast.mjs` | CI script: fail if any semantic text/background pair is below WCAG AA 4.5:1. |
