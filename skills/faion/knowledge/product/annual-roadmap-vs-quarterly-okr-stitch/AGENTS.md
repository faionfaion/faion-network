# Annual Roadmap vs Quarterly OKR Stitch

## Summary

**One-sentence:** Stitches an annual roadmap into a quarterly OKR cascade so the year's bet and the quarter's KRs stay coupled; output is a stitch spec with traceability matrix.

**One-paragraph:** Stitches an annual roadmap into a quarterly OKR cascade so the year's bet and the quarter's KRs stay coupled; output is a stitch spec with traceability matrix. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Annual planning that historically drifts from quarterly OKRs by Q3.
- Post-Series-A scale-up where roadmap and OKRs are owned by different leads.
- Investor / board memo: pin one traceability matrix from annual bets to quarterly KRs.
- Quarterly re-plan: which annual bets are on-pace, lagging, off-pace.

## Applies If (ALL must hold)

- Annual roadmap exists with ≥3 named bets.
- Quarterly OKR process is in place.
- Named owner per annual bet + per OKR.
- Traceability matrix can be drafted in a single doc.

## Skip If (ANY kills it)

- No annual roadmap defined yet — apply roadmap design methodology first.
- No quarterly OKR process — apply okr-design methodology first.
- Roadmap and OKRs deliberately decoupled by leadership choice — respect.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Annual roadmap | list of annual bets with success metric | leadership |
| Quarterly OKR list | current quarter OKRs + KRs | PMs |
| Owner roster | bet -> owner + OKR -> owner | org chart |
| Traceability matrix template | blank matrix to fill | PM ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-annual-roadmap-vs-quarterly-okr-stitch` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-annual-roadmap-vs-quarterly-okr-stitch.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[north-star-vs-okr-confidence-calibration]]
- [[kpi-tree-construction]]
- [[ai-feature-spec-contract]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "stitch_id": "stitch-acme-2026",
  "owner": "cpo@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "annual_bets": [
    {
      "id": "b-1",
      "name": "Win mid-market",
      "metric": "5 mid-market logos",
      "owner": "head-sales@acme.io"
    }
  ],
  "quarterly_okrs": [
    {
      "id": "o-1",
      "quarter": "Q2-2026",
      "objective": "Land 2 mid-market logos",
      "krs": [
        {
          "id": "kr-1",
          "name": "2 signed contracts",
          "target": 2,
          "current": 1,
          "owner": "ae@acme.io"
        }
      ]
    }
  ],
  "traceability_matrix": [
    {
      "bet_id": "b-1",
      "okr_id": "o-1",
      "evidence": "OKR doc Q2-2026"
    }
  ],
  "off_pace_flags": [
    {
      "bet_id": "b-1",
      "status": "on-pace",
      "evidence": "BI dashboard 2026-05-22"
    }
  ],
  "review_cadence": "monthly stitch review",
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
