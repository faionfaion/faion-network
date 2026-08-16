# Design Tokens Basics

## Summary

**One-sentence:** Baseline design-tokens spec covering canonical categories (color, spacing, typography, radius, shadow, motion), naming convention, alias-vs-base layering, and single-source-of-truth contract; produces a tokens.json spec consumed by both design tools and code.

**One-paragraph:** Baseline design-tokens spec covering canonical categories (color, spacing, typography, radius, shadow, motion), naming convention, alias-vs-base layering, and single-source-of-truth contract; produces a tokens.json spec consumed by both design tools and code. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Solo founders building both web + iOS / Android shells.
- Component libraries publishing tokens to consumers.
- Migrations from ad-hoc hex codes to a token system.
- Pre-funding design hygiene for investor demos.

## Applies If (ALL must hold)

- Project has ≥2 surfaces (e.g. web + email or web + native) consuming styling decisions.
- Design and engineering pull from the same value pool (or aspire to).
- Multi-theme requirement (light/dark, brand variants) exists or is planned.
- Naming conventions are decided (or about to be).

## Skip If (ANY kills it)

- Single-surface project with no theme needs — overhead exceeds value.
- Org uses a centralised design platform that already publishes tokens — duplicate effort.
- Project is still in pre-design exploration — tokens are premature.

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
| [[design-tokens-implementation]] | upstream context this methodology builds on |
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
| `fill-design-tokens-basics-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md.j2` | Minimal skeleton conforming to the output contract |
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract Generated from `templates/output-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-design-tokens-basics.py --self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-tokens-basics.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[design-tokens-implementation]]
- [[css-in-js-basics]]
- [[accessibility]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "artefact_id": "design-tokens-basics-2026-05-23",
  "owner": "ruslan@faion.net",
  "last_touched": "2026-05-23T12:00:00Z",
  "template_version": "1.1.0",
  "status": "ready_for_review",
  "tokens_file_path": "draft",
  "categories": [
    "item-1",
    {
      "key": "value-1"
    },
    {
      "key": "value-2"
    },
    {
      "key": "value-3"
    },
    {
      "key": "value-4"
    },
    {
      "key": "value-5"
    }
  ],
  "naming_convention": "draft",
  "themes": [
    "item-1"
  ],
  "consumer_outputs": [
    "item-1"
  ]
}
```
