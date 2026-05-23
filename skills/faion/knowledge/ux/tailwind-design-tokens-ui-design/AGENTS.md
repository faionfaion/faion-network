# Tailwind Design Tokens

## Summary

**One-sentence:** Bridges Tailwind config to a governed design-token layer so Tailwind utilities resolve to semantic tokens (color.feedback.error → bg-error-500) instead of magic numbers.

**One-paragraph:** Tailwind utility classes drift into magic numbers (text-[#FF6633], p-[12px]) without governance. This methodology pins a tokens-first Tailwind config: a script generates tailwind.config.js from a tokens.json (Style Dictionary or equivalent), Tailwind theme.colors / spacing / fontSize keys mirror the semantic tier, arbitrary value syntax (bracket notation) is CI-blocked. Tailwind utilities become a thin renderer of the token system, not a parallel source of truth.

**Ефективно для:**

- Solo founder using Tailwind + needing dark-mode / theming without rebuilding from scratch.
- Designer + AI agent pair where the agent emits Tailwind classes and must stay within tokens.
- Migrating an existing Tailwind project from arbitrary values to governed tokens.
- Adding a CI lint that blocks arbitrary value syntax.

## Applies If (ALL must hold)

- Project uses Tailwind v3.x or v4.x.
- Design tokens.json or equivalent is the source-of-truth.
- Build pipeline can run a tokens → tailwind.config.js generation step.
- CI can enforce a no-arbitrary-value rule.

## Skip If (ANY kills it)

- Project uses CSS-in-JS or vanilla CSS only — no Tailwind path.
- No tokens source — establish design-tokens-fundamentals first.
- Tailwind v2 or older — generator script targets v3+.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| tokens.json | JSON | Style Dictionary output |
| tailwind.config.js or v4 CSS-first config | JS / CSS | Frontend repo |
| CI lint config | yaml | Repo CI |
| Build tool (Vite / Next / Astro) | string | Frontend repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/design-tokens-fundamentals` | Token tiers consumed by the generator. |
| `solo/ux/handoff-spec-template` | Spec references Tailwind classes that resolve to tokens. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-tailwind-config` | sonnet | Per-project judgement on token-to-theme mapping. |
| `lint-arbitrary-values` | haiku | Deterministic regex scan for bracket syntax. |
| `multi-project-tokens-rollout` | opus | Cross-project synthesis for monorepos. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind-design-tokens.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/tailwind-design-tokens.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tailwind-design-tokens.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-tokens-fundamentals]]
- [[handoff-spec-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
