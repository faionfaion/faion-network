# Risk Assessment

## Summary

**One-sentence:** Likelihood × impact risk rubric scoring market, execution, technology, and regulatory risks on a 1-5 scale each, with named owners + mitigation actions per top-quartile risk.

**One-paragraph:** Likelihood × impact risk rubric scoring market, execution, technology, and regulatory risks on a 1-5 scale each, with named owners + mitigation actions per top-quartile risk. The methodology pins inputs to citable sources, runs ≥3 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Pre-spec risk register for a new product or pivot.
- Quarterly risk-review for an active product line.
- Investor-update preparation requiring a risk slide.
- Decision gates that need a defensible risk read before approval.

## Applies If (ALL must hold)

- The triggering activity for risk assessment appears in the user's workload at least once per cycle.
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
| [[market-analysis]] | upstream context this methodology builds on |
| [[competitor-analysis]] | upstream context this methodology builds on |

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
| `fill-risk-assessment-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |


## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md.j2` | Minimal skeleton conforming to the output contract |
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract Generated from `templates/output-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-<slug>.py --self-test` |
| `templates/pre-mortem.md.j2` | Multi-persona pre-mortem session converting imagined failure branches into scored risks and mitigations. |
| `templates/pre-mortem.md` | Multi-persona pre-mortem session converting imagined failure branches into scored risks and mitigations. Generated from `templates/pre-mortem.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/risk-register.md.j2` | Prioritized risk register (probability x impact scored) with response and contingency plans per risk. |
| `templates/risk-register.md` | Prioritized risk register (probability x impact scored) with response and contingency plans per risk. Generated from `templates/risk-register.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[market-analysis]]
- [[competitor-analysis]]
- [[agency-valuation-rubric]]

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
  "artefact_id": "risk-assessment-2026-05-23",
  "risks": [
    {
      "source": "https://example.com/source-1",
      "citation": "verbatim quote from source"
    }
  ],
  "matrix": {
    "key": "value"
  },
  "top_quartile": [
    {
      "source": "https://example.com/source-1",
      "citation": "verbatim quote from source"
    }
  ],
  "review_cycle": "draft",
  "evidence": [
    {
      "source": "https://example.com/transcript/1",
      "citation": "verbatim user quote"
    }
  ]
}
```
