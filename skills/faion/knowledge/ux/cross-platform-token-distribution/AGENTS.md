# Cross-Platform Token Distribution

## Summary

**One-sentence:** Produces a Style-Dictionary-driven token distribution pipeline emitting CSS, iOS Swift, Android XML, and Tailwind config from a single W3C DTCG source.

**One-paragraph:** Design tokens are the single source of truth for color/spacing/typography across platforms. The pipeline reads W3C DTCG JSON, transforms platform-specific (web CSS variables / iOS Swift / Android XML / Tailwind utility config), and emits per-platform bundles with semantic naming preserved. Versioned per-token; CI lints for divergence; designers and devs edit only the canonical source.

**Ефективно для:**

- Multi-platform продукт (web + iOS + Android) — single source of truth.
- Tailwind+CSS variables: один pipeline emit обидва.
- Avoid drift коли designer змінює primary color у Figma а dev забуває.
- Theming (light/dark/brand variants) з одного канонічного джерела.

## Applies If (ALL must hold)

- Product ships to >=2 platforms requiring token sync.
- W3C DTCG JSON is the source of truth.
- Style Dictionary (or equivalent transform) is acceptable in the build pipeline.

## Skip If (ANY kills it)

- Single-platform web-only product — direct CSS variables suffice.
- No design system formalised — apply design-tokens-fundamentals first.
- Codeless prototype — pipeline overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Canonical tokens JSON | W3C DTCG | design system |
| Target platforms list | list (web/iOS/Android/Tailwind) | product brief |
| Style Dictionary config | JSON | this methodology template |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[design-tokens-fundamentals]] | Three-tier (primitive/semantic/component) architecture this distributes |
| [[w3c-design-tokens-standard]] | DTCG spec underpins the source |

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
| `templates/tokens.json` | Canonical W3C DTCG tokens skeleton (primitive + semantic + component layers) |
| `templates/sd-config.json` | Style Dictionary config defining per-platform transforms + output paths |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cross-platform-token-distribution.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[design-tokens-fundamentals]]
- [[w3c-design-tokens-standard]]
- [[design-system-success-factors]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
