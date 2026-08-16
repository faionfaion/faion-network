# Agency Valuation Rubric

## Summary

**One-sentence:** Weighted 1-5 rubric that converts qualitative agency-quality signals (productized revenue %, retainer %, owner-dependency, niche stickiness) into a comparable 0-100 valuation multiplier on top of EBITDA.

**One-paragraph:** Weighted 1-5 rubric that converts qualitative agency-quality signals (productized revenue %, retainer %, owner-dependency, niche stickiness) into a comparable 0-100 valuation multiplier on top of EBITDA. The methodology pins inputs to citable sources, runs ≥3 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Founder pre-broker self-valuation before exit conversations.
- Comparing 3-5 agency acquisition targets against the same yardstick.
- Stress-testing a 3x EBITDA offer against rubric-driven adjustments.
- Annual owner-dependency audit to identify which scores to raise.

## Applies If (ALL must hold)

- The triggering activity for agency valuation rubric appears in the user's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/research/market-researcher/` parent skill context | vocabulary, neighbouring methodologies |
| [[niche-scorecard]] | upstream context this methodology builds on |
| [[business-model-planning]] | upstream context this methodology builds on |

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
| `fill-agency-valuation-rubric-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |


## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md.j2` | Minimal skeleton conforming to the output contract |
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract Generated from `templates/output-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-<slug>.py --self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-valuation-rubric.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |


## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[niche-scorecard]]
- [[business-model-planning]]
- [[competitor-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "owner": "ruslan@faion.net",
  "last_touched": "2026-05-23T12:00:00Z",
  "template_version": "1.1.0",
  "artefact_id": "agency-valuation-rubric-2026-05-23",
  "target_name": "draft",
  "ebitda_usd": 1.0,
  "scores": {
    "key": "value"
  },
  "weighted_total": 1.0,
  "multiplier": 1.0,
  "evidence": [
    {
      "source": "https://example.com/transcript/1",
      "citation": "verbatim user quote"
    }
  ],
  "decision": "draft"
}
```
