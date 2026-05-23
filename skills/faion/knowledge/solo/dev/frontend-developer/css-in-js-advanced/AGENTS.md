---
slug: css-in-js-advanced
tier: solo
group: dev
domain: frontend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Advanced CSS-in-JS patterns covering SSR critical-CSS extraction, atomic compile-time variants, theme runtime swapping, and zero-runtime alternatives; produces a code scaffold + decision matrix selecting library (styled-components, Linaria, vanilla-extract, Panda CSS) per constraint."
content_id: "dcd37b91b84a7c26"
complexity: deep
produces: code
est_tokens: 4900
tags: ["frontend", "solo", "css-in-js", "performance", "ssr"]
---
# CSS-in-JS Advanced

## Summary

**One-sentence:** Advanced CSS-in-JS patterns covering SSR critical-CSS extraction, atomic compile-time variants, theme runtime swapping, and zero-runtime alternatives; produces a code scaffold + decision matrix selecting library (styled-components, Linaria, vanilla-extract, Panda CSS) per constraint.

**One-paragraph:** Advanced CSS-in-JS patterns covering SSR critical-CSS extraction, atomic compile-time variants, theme runtime swapping, and zero-runtime alternatives; produces a code scaffold + decision matrix selecting library (styled-components, Linaria, vanilla-extract, Panda CSS) per constraint. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Marketing pages where TTFB is a conversion factor.
- Multi-tenant SaaS with white-label theming.
- Component libraries needing zero-runtime extraction for consumers.
- Solo founders deciding the lib once and living with the choice for years.

## Applies If (ALL must hold)

- Project uses or is migrating to a CSS-in-JS solution.
- Performance budget exists (TTFB, bundle size, runtime CSS overhead).
- SSR or static-export is in use (Next.js, Remix, Astro, Gatsby).
- Themeing (light/dark, brand variants) or per-tenant styling is a requirement.

## Skip If (ANY kills it)

- Project is fine on plain CSS / Tailwind — no need to introduce JS-bound styling.
- Bundle size is not a constraint (internal admin tool) — runtime CSS-in-JS is fine.
- Component library is already stable — migrating is more risk than reward.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[css-in-js-basics]] | upstream context this methodology builds on |
| [[design-tokens-implementation]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-css-in-js-advanced-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-css-in-js-advanced.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-css-in-js-advanced.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[css-in-js-basics]]
- [[design-tokens-implementation]]
- [[design-tokens-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
