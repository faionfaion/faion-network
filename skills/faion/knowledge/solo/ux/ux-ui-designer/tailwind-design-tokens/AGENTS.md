# Tailwind + Design Tokens

## Summary

Map design tokens (colors, spacing, typography) to Tailwind's theme config via CSS custom properties, so the design system and component library share a single source of truth. All `tailwind.config.js` values must reference `var(--token-name)` — no hardcoded hex or pixel values. Semantic tokens (color.action.primary) are exposed in Tailwind; primitive tokens (raw hex) stay in CSS variables only.

## Why

Hardcoded values in Tailwind classes create drift between Figma design tokens and code, break multi-brand/white-label theming, and require global find-replace for any visual update. CSS custom properties as the bridge enable runtime theming without rebuilding Tailwind. The token-first approach also unlocks Figma Variables → code pipelines via Style Dictionary.

## When To Use

- Setting up a new project's design system foundation (define tokens once, use everywhere)
- Migrating hardcoded hex values and magic numbers to semantic token classes
- Bridging a Figma design system (with Variables/Tokens) to a Tailwind CSS implementation
- Multi-brand or white-label products where the same component library needs per-tenant theming
- When Tailwind utilities and custom components must share the same spacing/color values

## When NOT To Use

- Projects with no design system requirements — raw Tailwind utilities are sufficient
- Teams not using Tailwind — use CSS custom properties directly or Style Dictionary alone
- Projects where design tokens are owned by a design-ops team and locked from code edits
- Prototype/throwaway work where systematic tokens add overhead with no payoff

## Content

| File | What's inside |
|------|---------------|
| `content/01-token-architecture.xml` | Primitive vs. semantic token split, CSS variable bridge pattern, Tailwind config structure, dark-mode scoping, JIT safelist requirement |
| `content/02-antipatterns.xml` | Hardcoded values in config, opacity modifier failure with hex tokens, token naming drift, dynamic class assembly breaking JIT purge |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.js` | Example Tailwind config mapping semantic tokens to CSS variables for colors, spacing, and typography |
| `templates/tokens.css` | Companion CSS file declaring all custom properties at `:root` |
| `templates/sd.config.js` | Style Dictionary build script: transforms W3C DTCG token JSON to Tailwind config + CSS variables |
