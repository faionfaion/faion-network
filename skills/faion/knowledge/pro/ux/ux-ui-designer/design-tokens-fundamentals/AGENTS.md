---
slug: design-tokens-fundamentals
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a three-tier (primitive → semantic → component) W3C DTCG token spec with accessibility-baked color pairs, motion variants, and logical spacing.
content_id: "7fb5e37f7aba04f7"
complexity: medium
produces: spec
est_tokens: 4500
tags: [design-tokens, w3c-dtcg, semantic-naming, theming, accessibility]
---
# Design Tokens Fundamentals

## Summary

**One-sentence:** Produces a three-tier (primitive → semantic → component) W3C DTCG token spec with accessibility-baked color pairs, motion variants, and logical spacing.

**One-paragraph:** Three-tier token architecture is the spec: primitive (raw values), semantic (intent-named — `color.text.primary`), component (component-specific — `button.primary.background`). W3C DTCG JSON is the canonical format; Style Dictionary transforms to platform-specific output. Accessibility is baked: every color pair carries a contrast ratio; every motion token carries a reduced-motion variant; every spacing token uses logical properties.

**Ефективно для:**

- Authoring tokens у W3C DTCG — single source of truth.
- Three-tier (primitive/semantic/component) — щоб theming не дублювало логіку.
- Baked a11y constraints — contrast ratio як обов'язкове поле.
- Logical spacing properties для RTL без додаткової роботи.

## Applies If (ALL must hold)

- Authoring or restructuring a design-system token layer.
- W3C DTCG JSON is acceptable as the source format.
- Multi-platform or multi-theme output is in scope.

## Skip If (ANY kills it)

- Single-page marketing site — direct CSS variables suffice.
- Token layer already structured and compliant — no rework needed.
- Hard-coded values acceptable in context (one-off internal tool).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Brand palette + scale | hex list / type ramp | brand guidelines |
| Target platforms | list | product brief |
| Theming requirements | light/dark/brand variant list | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[w3c-design-tokens-standard]] | DTCG spec underpins the canonical format |
| [[accessibility-first-design]] | A11y constraints baked into tokens |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens-skeleton.json` | Three-tier DTCG token skeleton with primitive/semantic/component layers |
| `templates/token-contrast.mjs` | Node CLI computing contrast_ratio for every text/bg pairing in tokens.json |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-tokens-fundamentals.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[w3c-design-tokens-standard]]
- [[cross-platform-token-distribution]]
- [[accessibility-first-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
