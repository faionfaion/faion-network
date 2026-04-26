# Tailwind + Design Tokens

## Summary

Integrating design tokens into Tailwind CSS by mapping token values to CSS custom properties and referencing them in `tailwind.config.js` — using RGB channel syntax for color tokens to preserve opacity modifier functionality (`bg-primary/50`), and extending (not replacing) the default theme.

## Why

Hardcoded Tailwind utility values (`text-[#3B82F6]`, `p-[13px]`) scatter design decisions and break theming. A token-backed config where every color and spacing utility references a CSS variable enables dark mode, brand variants, and white-label theming with a single token file change.

## When To Use

- Bootstrapping a new Tailwind project that must support theming (dark mode, brand variants, white-label)
- Migrating an existing Tailwind codebase from hardcoded utility values to CSS-variable-backed tokens
- Generating `tailwind.config.js` theme overrides from a Style Dictionary token build output
- Auditing a Tailwind codebase for arbitrary values (`text-[#...]`, `p-[...]`) that should become tokens
- Setting up a Storybook token documentation layer alongside a Tailwind component library

## When NOT To Use

- Projects not using Tailwind — use Style Dictionary + CSS custom properties directly
- Pure CSS/SCSS codebases where Tailwind migration is not planned
- When design tokens are not yet defined or stable — generating config before taxonomy is finalized creates throwaway work
- Utility-class-only projects with zero theming requirements — CSS variable indirection adds complexity without payoff

## Content

| File | What's inside |
|------|---------------|
| `content/01-integration-rules.xml` | RGB channel pattern for color tokens, theme.extend vs theme replacement, CSS variable declaration pattern, opacity modifier compatibility, arbitrary-value audit discipline |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.js` | Tailwind config example with CSS variable references for color and spacing tokens using RGB channel pattern |
| `templates/build-tailwind-tokens.mjs` | Node.js script that reads tokens.json and outputs tailwind-theme.js + tokens.css with correct RGB channel handling |
