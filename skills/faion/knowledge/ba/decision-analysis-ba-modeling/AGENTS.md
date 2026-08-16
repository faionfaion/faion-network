# Decision Analysis

## Summary

**One-sentence:** 6-step decision-matrix process — define decision, options, weighted criteria locked pre-scoring, evidence-per-cell scores, sensitivity Monte Carlo, signed rationale.

**One-paragraph:** Structured option evaluation: define the decision and its reversal cost, enumerate options (with explicit "do nothing"), define and FREEZE weighted criteria before scoring, score each option×criterion cell with evidence URL, run ±20% weight Monte Carlo to surface ranking instability, and capture rationale in a signed decision-record. Output is a `decision-record` artefact that survives audit and prevents post-hoc rationalization.

**Ефективно для:**

- Strategic option choice ≥$10k or irreversible (architecture, vendor, hiring).
- Multi-criterion trade-offs де gut feel divergent across stakeholders.
- Post-incident decision audit ("why did we choose X?").
- Compliance / governance requiring documented rationale.

## Applies If (ALL must hold)

- Decision has ≥2 viable options + "do nothing" baseline.
- Decision is non-trivial (stakes ≥$10k, reversal cost meaningful, or strategic).
- Criteria can be enumerated and weighted (5-9 dimensions typical).
- Evidence (data, citations, benchmarks) is reachable per cell.

## Skip If (ANY kills it)

- Single-criterion decision (price-only, deadline-only).
- Reversible low-stakes choice (under $1k, undo cost ≈ 0).
- Time-critical incident response — pick fast, document later.
- Decisions where stakeholders refuse to commit weights — full rubric becomes theater.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision brief | 1-page Markdown | sponsor |
| Option catalogue | list with descriptions + costs | proposers |
| Criteria + draft weights | spreadsheet / YAML | BA + sponsor |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ai-acceptance-criteria-generator-reviewer]] | Sibling rubric pattern this methodology shares discipline with |
| [[ba-planning]] | Upstream BA governance that scopes who weighs in on the decision |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: weights locked pre-scoring, evidence per cell, "do nothing" included, sensitivity ±20%, signoff | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: weight reverse-engineering, missing "do nothing", anchor drift, single-rater high-stakes | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 750 |
| `content/05-examples.xml` | essential | Worked example: vendor selection across 3 options × 6 criteria | 700 |
| `content/06-decision-tree.xml` | essential | Routing on weight lock + evidence + Monte Carlo | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `criteria_definition` | sonnet | Light judgment on dimension naming + anchors. |
| `evidence_extraction` | haiku | Mechanical retrieval of evidence URLs per cell. |
| `sensitivity_analysis` | opus | Monte Carlo + rank-flip detection requires careful reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md.j2` | Markdown skeleton (decision, options, criteria, scores, sensitivity, signoff) |
| `templates/decision-record.md` | Markdown skeleton (decision, options, criteria, scores, sensitivity, signoff) Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable decision-record JSON |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.
| `templates/decision-analysis.md.j2` | decision-record skeleton (decision + options + criteria + scores + sensitivity + signoff) |
| `templates/decision-analysis.md` | decision-record skeleton (decision + options + criteria + scores + sensitivity + signoff) Generated from `templates/decision-analysis.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/decision-matrix-simple.md.j2` | lightweight 3-option × 3-criteria decision matrix |
| `templates/decision-matrix-simple.md` | lightweight 3-option × 3-criteria decision matrix Generated from `templates/decision-matrix-simple.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-acceptance-criteria-generator-reviewer]]
- [[ba-planning]]
- [[business-process-analysis]]
- [[interface-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on observable signals (weight lock timestamp, evidence completeness, sensitivity rank-flips) to the active rule. Use when in doubt whether the record is ready for sign-off.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "decision_id": "smoke-vendor",
  "options": [
    {
      "id": "do-nothing",
      "name": "Status quo",
      "is_baseline": true
    },
    {
      "id": "vendor-a",
      "name": "Vendor A"
    }
  ],
  "criteria": [
    {
      "id": "tco",
      "name": "TCO",
      "weight": 0.5
    },
    {
      "id": "fit",
      "name": "Fit",
      "weight": 0.3
    },
    {
      "id": "risk",
      "name": "Risk",
      "weight": 0.2
    }
  ],
  "weights_locked_at": "2026-05-23T08:00:00Z",
  "scores": [
    {
      "option_id": "do-nothing",
      "criterion_id": "tco",
      "score": 3,
      "evidence": "baseline.md#L1"
    },
    {
      "option_id": "do-nothing",
      "criterion_id": "fit",
      "score": 2,
      "evidence": "baseline.md#L4"
    },
    {
      "option_id": "do-nothing",
      "criterion_id": "risk",
      "score": 5,
      "evidence": "baseline.md#L7"
    },
    {
      "option_id": "vendor-a",
      "criterion_id": "tco",
      "score": 4,
      "evidence": "a-tco.pdf#p12"
    },
    {
      "option_id": "vendor-a",
      "criterion_id": "fit",
      "score": 4,
      "evidence": "a-demo.mp4#10:00"
    },
    {
      "option_id": "vendor-a",
      "criterion_id": "risk",
      "score": 3,
      "evidence": "a-soc2.pdf"
    }
  ],
  "sensitivity": {
    "monte_carlo_runs": 1000,
    "weight_jitter_pct": 20,
    "rank_flip_rate": 0.05,
    "unstable_pairs": []
  },
  "approver": {
    "name": "Pedro Silva",
    "role": "CFO",
    "signoff_ts": "2026-05-23T11:00:00Z"
  },
  "rationale": "Vendor A wins; sensitivity flip rate 5% well under 15% threshold."
}
```
