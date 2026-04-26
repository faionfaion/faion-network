# Design Tokens Implementation

## Summary

Design tokens form a three-layer hierarchy — **primitives** (raw hex/rem), **semantic**
(`bg.surface.default`), and **component** (`button.primary.bg`) — built from JSON/DTCG sources
and compiled to CSS custom properties, TypeScript, iOS Swift, and Android XML via Style Dictionary
or Terrazzo. App code consumes only the semantic and component layers. Mode switching (light/dark)
lives in separate mode files per mode; the semantic alias layer resolves at build time.

## Why

Without tokens, color and spacing are scattered across component files and impossible to theme,
migrate, or verify for WCAG contrast. A token pipeline separates *what a value is* (primitive)
from *what it means* (semantic), enabling multi-platform output from one source, mode switching
without component rewrites, and automated contrast-ratio validation in CI.

## When To Use

- Multi-platform product (web + iOS + Android) needing a single source of truth for color,
  typography, and spacing.
- Migrating ad-hoc CSS variables or Sass `$color-*` maps to a pipeline.
- Wiring Tailwind theme, CSS custom properties, and native platform outputs from one JSON source.
- Light/dark/high-contrast/brand modes via a semantic alias layer.
- Connecting Figma Variables → Tokens Studio → Style Dictionary → app codegen.

## When NOT To Use

- Single-app, single-platform project with stable styling (over-engineering for solos).
- Prototype/MVP where design churn outpaces token churn.
- Static marketing sites with no design system to maintain.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Layer hierarchy rules, mode file layout, CI validation, DTCG vs Tokens Studio divergence. |
| `content/02-examples.xml` | Style Dictionary config, CSS custom properties output, Tailwind integration, Figma sync CI. |

## Templates

| File | Purpose |
|------|---------|
| `templates/style-dictionary.config.js` | Style Dictionary v3 config emitting CSS, SCSS, JS, TS, JSON outputs. |
| `templates/tokens-semantic.json` | Semantic token layer example with alias references and $description fields. |
| `templates/sync-tokens.yml` | GitHub Actions workflow: tokens/ change → SD build → PR creation. |
