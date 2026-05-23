# CSS-in-JS Basics

## Summary

**One-sentence:** Baseline patterns for CSS-in-JS in component libraries: prop-driven styles, theme provider, scoped class names, and TypeScript-typed style props; produces a starter scaffold matching the chosen library with naming + file-layout conventions.

**One-paragraph:** Baseline patterns for CSS-in-JS in component libraries: prop-driven styles, theme provider, scoped class names, and TypeScript-typed style props; produces a starter scaffold matching the chosen library with naming + file-layout conventions. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- New component libraries deciding conventions before component-volume explodes.
- Existing libraries inconsistent in styling patterns.
- Onboarding contributors to a CSS-in-JS codebase.
- Solo founders shipping a design system without a UI engineer.

## Applies If (ALL must hold)

- Project picks a CSS-in-JS library (styled-components, Emotion, Stitches, etc.).
- Components have ≥2 visual variants requiring prop-driven styling.
- TypeScript is in use (or strict-mode JS).
- A theme provider OR design-token source exists or is planned.

## Skip If (ANY kills it)

- Project will not use CSS-in-JS — Tailwind, CSS modules, or vanilla CSS apply different methodologies.
- Library choice still undecided — finish the css-in-js-advanced decision first.
- Component library is single-variant — props-styling overhead exceeds value.

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
| [[css-in-js-advanced]] | upstream context this methodology builds on |
| [[design-tokens-basics]] | sibling discipline cited in decision tree |

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
| `fill-css-in-js-basics-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-css-in-js-basics.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-css-in-js-basics.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[css-in-js-advanced]]
- [[design-tokens-basics]]
- [[design-tokens-implementation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
