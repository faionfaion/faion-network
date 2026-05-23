---
slug: semantic-tokens-and-modes
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a three-layer design-token configuration (reference / system / component) with mode coverage across light/dark/HC/brand and a Style Dictionary build pipeline emitting platform tokens.
content_id: "20e934c1b5c9dd87"
complexity: medium
produces: config
est_tokens: 4400
tags: [design-tokens, semantic-tokens, modes, style-dictionary, theming]
---
# Semantic Tokens and Modes

## Summary

**One-sentence:** Produces a three-layer design-token configuration (reference / system / component) in DTCG format with full mode coverage and a Style Dictionary pipeline that emits CSS / Swift / Compose outputs.

**One-paragraph:** Design tokens are decoupled into three explicit layers — reference (raw palette/scale), system (semantic, mode-aware), component (component-scoped) — and driven through a four-stage pipeline: author (Figma Variables) → export (REST API) → transform (Style Dictionary) → consume (CSS/Swift/Compose). Every semantic token MUST have a value in every required mode (light / dark / high-contrast / brand). Raw reference values MUST NOT appear in component code; lint rules enforce. Component layer MUST NOT reference the reference layer directly — only through the system layer.

**Ефективно для:**

- Adding light/dark/high-contrast modes до існуючої token system без коду-forks.
- Multi-brand / white-label products де одна бібліотека обслуговує кілька visual identities.
- Multi-platform builds (web + iOS + Android) які діляться semantic intent.
- Density modes (compact / comfortable) для data-heavy enterprise UIs.

## Applies If (ALL must hold)

- Component library has ≥30 components or there is a foreseeable theming requirement.
- A Figma source-of-truth exists for token authoring (Figma Variables / Tokens Studio).
- Build pipeline can run Node/Style Dictionary in CI.

## Skip If (ANY kills it)

- Single-theme product with no future theming need — overhead exceeds payoff.
- One-off marketing pages outside the system.
- Motion / animation primitives — semantic naming rarely earns its keep there.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Figma Variables export | JSON via REST API | design system Figma file |
| Required-mode list | YAML or Markdown | design system charter |
| Platform output targets | list (css/swift/compose) | engineering |
| Lint config | ESLint / Stylelint | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[token-organization]] | Defines the naming convention this token configuration uses |
| [[design-tokens-fundamentals]] | Upstream conceptual baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: three-layer-strict, one-intent-per-token, mode-coverage-required, dtcg-format, no-raw-hex-in-components, visual-regression-per-mode | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for token-config artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: reference-jumping, brand-mode-duplication, missing-platform-transform, raw-hex-in-component | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: model layers → declare modes → wire pipeline → lint → visual-regression | 900 |
| `content/06-decision-tree.xml` | essential | Routing: scope-of-theming → number-of-modes → multi-platform yes/no → pipeline choice | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-figma-variables` | haiku | Mechanical REST API call. |
| `propose-semantic-naming` | sonnet | Light judgment on intent grouping. |
| `generate-style-dictionary-config` | sonnet | Template fill + transform selection. |
| `audit-mode-coverage` | haiku | Boolean check per token × mode. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens-semantic.json` | DTCG-format semantic-layer skeleton with mode collection |
| `templates/style-dictionary.config.cjs` | Style Dictionary build config emitting CSS / Swift / Compose |
| `templates/check-modes.mjs` | CI gate: fails build if any semantic token is missing a value in any required mode |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-semantic-tokens-and-modes.py` | Validate the token-config artefact against the schema | Pre-commit; CI before Style Dictionary build |

## Related

- [[token-organization]]
- [[cross-platform-token-distribution]]
- [[design-tokens-fundamentals]]
- [[w3c-design-tokens-standard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on scope-of-theming (single / light+dark / multi-brand / density-aware) and platform count (web-only / multi-platform). Each leaf references a rule from `01-core-rules.xml` and dictates whether the system layer must add a mode collection, whether Style Dictionary needs a platform transform, and whether visual regression must snapshot every mode.
