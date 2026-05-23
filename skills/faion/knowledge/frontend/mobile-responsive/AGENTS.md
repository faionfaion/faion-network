# Mobile Responsive

## Summary

**One-sentence:** Mobile-first responsive design spec: breakpoint catalogue, container-query strategy, touch-target minimums, viewport-meta + safe-area handling, and per-component breakpoint policy; produces a spec the codebase asserts against in lint + tests.

**One-paragraph:** Mobile-first responsive design spec: breakpoint catalogue, container-query strategy, touch-target minimums, viewport-meta + safe-area handling, and per-component breakpoint policy; produces a spec the codebase asserts against in lint + tests. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- SaaS dashboards bolted onto a mobile reality after desktop-first build.
- Marketing pages converting on mobile traffic.
- Component libraries publishing breakpoint conventions to consumers.
- Solo founders pre-empting mobile-first audits.

## Applies If (ALL must hold)

- Project targets mobile + desktop users.
- Operator can enforce breakpoint conventions in CSS / token system.
- Tooling supports container queries OR a polyfill strategy is acceptable.
- Touch + keyboard inputs both matter for the product.

## Skip If (ANY kills it)

- Desktop-only product (CAD-style tool, IDE) — overhead exceeds value.
- Pure web-view inside a native app — host app constrains responsiveness.
- Project uses a UI framework that ships its own breakpoint system (Bootstrap, MUI) — adopt theirs.

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
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-mobile-responsive-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-mobile-responsive.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mobile-responsive.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[design-tokens-basics]]
- [[css-in-js-basics]]
- [[accessibility]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
