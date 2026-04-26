# Design Tokens: Basics

## Summary

Design tokens are the atomic values of a design system — colors, spacing, typography, radii — stored as platform-agnostic data. They enforce a three-level hierarchy: primitive (raw values) → semantic (purpose aliases) → component (per-component overrides), with a single source of truth that compiles to CSS variables, iOS Swift, Android XML, or any target.

## Why

Without tokens, design decisions scatter across components as hardcoded hex values and magic numbers, making theming and rebrand work O(N) per component. Semantic tokens decouple purpose from value: changing the brand primary color requires one token update, not a grep-and-replace. The three-level hierarchy prevents semantic tokens from referencing other semantic tokens (circular aliasing) while keeping component tokens narrowly scoped.

## When To Use

- Starting or scaling a design system
- Adding dark mode or white-label theming
- Unifying visual language across web, iOS, Android
- Design-to-dev handoff where tokens are the contract

## When NOT To Use

- One-off landing pages with no reuse — token overhead outweighs benefit
- Prototypes where values will change completely — define tokens only when the design stabilises
- When a third-party component library owns all tokens and override is impractical

## Content

| File | What's inside |
|------|---------------|
| `content/01-hierarchy.xml` | Primitive → semantic → component levels; naming rules; version control strategy |
| `content/02-token-formats.xml` | JSON token definitions for colors, spacing, typography, radius, shadow with examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/primitive.json` | Primitive token file: full color scale, spacing, fontSize, fontWeight, borderRadius, shadow |
| `templates/semantic.json` | Semantic token file: bg, text, border, action, status aliases for light theme |
| `templates/semantic-dark.json` | Dark theme semantic overrides |
