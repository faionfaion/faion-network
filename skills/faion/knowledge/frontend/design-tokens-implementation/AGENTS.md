# Design Tokens Implementation

## Summary

**One-sentence:** Implementation playbook for design tokens: tokens.json schema, style-dictionary (or equivalent) build pipeline, CI sync to platform outputs, and a Figma-to-code round-trip; produces a working tokens repo with build + lint + sync scripts.

**One-paragraph:** Implementation playbook for design tokens: tokens.json schema, style-dictionary (or equivalent) build pipeline, CI sync to platform outputs, and a Figma-to-code round-trip; produces a working tokens repo with build + lint + sync scripts. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Component-library authors publishing tokens to npm consumers.
- Cross-platform shells needing identical tokens in web + iOS + Android.
- Figma + code design-engineering loops where tokens must round-trip.
- Solo founders avoiding manual sync between design and code.

## Applies If (ALL must hold)

- A design-tokens-basics spec already exists or is being authored in parallel.
- Build tooling (npm scripts, Make, Just) is in use.
- At least one consumer output is required (CSS variables, JS constants, native platform constants).
- CI is configured.

## Skip If (ANY kills it)

- Spec is not yet drafted — finish design-tokens-basics first.
- Only one consumer (CSS variables in one app) — direct CSS variables file is fine.
- Org uses a hosted token platform (Tokens Studio Cloud, Specify) — different methodology.

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
| [[design-tokens-basics]] | upstream context this methodology builds on |
| [[css-in-js-basics]] | sibling discipline cited in decision tree |

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
| `fill-design-tokens-implementation-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-design-tokens-implementation.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-tokens-implementation.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[design-tokens-basics]]
- [[css-in-js-basics]]
- [[css-in-js-advanced]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
