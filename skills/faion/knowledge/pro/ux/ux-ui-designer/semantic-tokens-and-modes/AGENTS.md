# Semantic Tokens and Modes

## Summary

A methodology for structuring design tokens in three explicit layers — reference (raw palette/scale), system (semantic, mode-aware), component (component-scoped) — and driving them through a four-stage pipeline: author (Figma Variables) → export (REST API) → transform (Style Dictionary) → consume (CSS/Swift/Compose). Every semantic token must be defined in every mode (light, dark, high-contrast, brand). Raw reference values must never appear in product code; lint rules are mandatory.

## Why

Semantic tokens decouple visual intent from raw values, enabling light/dark/high-contrast, multi-brand, multi-platform, and density modes to be applied as config overlays rather than code forks. Without them, adding a dark mode requires a full codebase grep-and-replace. Naming governance prevents the most expensive failure mode: token proliferation that fragments rather than unifies the system.

## When To Use

- Adding light/dark/high-contrast modes to an existing token system.
- Multi-brand or white-label products where one library serves several visual identities.
- Multi-platform builds (web + iOS + Android) that share semantic intent but diverge in raw values.
- Density modes (compact/comfortable) for data-dense enterprise UIs.
- Migrating from raw CSS custom properties to a tokens-as-source-of-truth pipeline.

## When NOT To Use

- Single-theme product with no foreseeable theming requirement — semantic-token indirection adds no payoff.
- Pure marketing campaigns or one-off pages outside the system.
- Component libraries below ~30 components — overhead exceeds savings.
- Motion/animation primitives — semantic naming for durations rarely earns its keep.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Three-layer model, mode types, Figma Variables implementation, DTCG format rules |
| `content/02-agent-patterns.xml` | Four-stage pipeline, agent roles, naming governance, gotchas, tooling |

## Templates

| File | Purpose |
|------|---------|
| `templates/check-modes.mjs` | CI gate: fails build if any semantic token is missing a value in any required mode |

## Scripts

none
