# Design Tokens Fundamentals

## Summary

Design tokens are named, platform-agnostic values (colors, spacing, typography) organized in a three-tier hierarchy — global (raw values) → semantic (intent aliases) → component (scoped) — that enable consistent theming, dark mode, and single-source-of-truth updates across platforms.

## Why

Hardcoded color and spacing values scatter design decisions across a codebase, making theming, dark mode, and brand updates expensive. A governed token layer — where semantic tokens always alias global tokens, never raw values — ensures that renaming `color.primary` propagates everywhere and that Figma and code stay synchronized.

## When To Use

- Setting up a new design system from scratch (tokens are the foundation before any component library)
- Adding dark mode, theme switching, or white-label support to an existing codebase
- Auditing a codebase for hardcoded color/spacing/font values that should be tokenized
- Migrating from inline Tailwind classes or CSS magic numbers to a governed token layer
- Generating token documentation from a Figma Variables export or Style Dictionary config

## When NOT To Use

- Single-component quick fixes — token infrastructure has setup cost not worth it for one-off styling
- Projects with a single theme and no planned theming requirements
- When the design tool (Figma) and codebase are not synchronized — tokens create false confidence if sources diverge
- Legacy jQuery / server-rendered projects without a CSS variable pipeline

## Content

| File | What's inside |
|------|---------------|
| `content/01-token-structure.xml` | Three token tiers, naming conventions, alias rules, W3C token JSON format, and the governance discipline required to prevent token sprawl |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens.json` | W3C-compliant design token JSON example with global, semantic, and component tiers for color and spacing |
| `templates/sd.config.js` | Style Dictionary build config generating CSS variables and JS/TS exports from token JSON |
