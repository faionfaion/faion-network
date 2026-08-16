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
| `content/01-core-rules.xml` | essential | 11 testable rules: mobile-first cascade, finite breakpoint catalogue, container queries, 44px targets, viewport meta, safe-area, hover not load-bearing, fluid sizing over fixed px, dvh on iOS, multi-viewport verification gate, skip contract | 1500 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix, incl. fixed-px widths and `100vh` on iOS | 1000 |
| `content/04-procedure.xml` | essential | 10-step procedure with input/action/output per step, ending on the four-width verification gate | 1000 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-mobile-responsive-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |
| `run-verification-gate` | haiku | Execute the Playwright widths and read the overflow assertions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md.j2` | Minimal skeleton conforming to the output contract |
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract Generated from `templates/output-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-mobile-responsive.py --self-test` |
| `templates/playwright-devices.ts` | Playwright project matrix for mobile / tablet / desktop device profiles |
| `templates/responsive-check.ts` | Multi-viewport screenshot run with a horizontal-overflow assertion per width |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "artefact_id": "mobile-responsive-2026-05-23",
  "owner": "ruslan@faion.net",
  "last_touched": "2026-05-23T12:00:00Z",
  "template_version": "1.1.0",
  "status": "ready_for_review",
  "breakpoints": [
    "item-1",
    {
      "key": "value-1"
    },
    {
      "key": "value-2"
    }
  ],
  "container_query_policy": "draft",
  "touch_target_min_px": 44,
  "viewport_meta": "draft",
  "safe_area_policy": "draft",
  "hover_policy": "draft"
}
```
