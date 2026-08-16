# AI Incident Triage Matrix

## Summary

**One-sentence:** Numeric scoring rubric (1-5 anchored, weighted blend) that classifies an AI-feature incident across 5 lanes (model-regression / prompt-injection / data-drift / upstream-API / cost-runaway) and routes to lane-specific mitigation.

**One-paragraph:** Numeric scoring rubric (1-5 anchored, weighted blend) that classifies an AI-feature incident across 5 lanes (model-regression / prompt-injection / data-drift / upstream-API / cost-runaway) and routes to lane-specific mitigation. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- AI-incident postmortem requires explicit lane assignment перед mitigation.
- Multi-rater scoring (≥2) для рішень з $10k+ impact.
- Cross-cohort comparison: 50+ AI incidents/квартал → потрібен trend.
- Incident triage CI: автоматичні signals (cost spike, refusal rate, drift score).

## Applies If (ALL must hold)

- AI incident postmortem exists with reproducible evidence (traces, logs, dashboards).
- Multiple raters available for stakes ≥$10k.
- Weights pre-registered in repo before scoring.
- Mitigation lanes (model regression / prompt injection / data drift / upstream API / cost runaway) have named owners.

## Skip If (ANY kills it)

- n<3 instances per quarter — gut feel faster than rubric.
- Decisions are single-criterion (cost-only, latency-only) — full rubric is overhead.
- Raters untrained / no calibration examples available.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incident postmortem | Markdown / Confluence page | On-call rotation / SRE |
| Dimension anchor sheet | YAML / spreadsheet | Team rubric author |
| Pre-registered weights | YAML in repo | Rubric owner |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-incident-triage-matrix` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.yaml` | Rubric definition — dimensions + anchors (1/3/5) + weights |
| `templates/rubric-instance.json` | Instance of a filled rubric (scores + evidence) |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-incident-triage-matrix.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ai/ml-engineer/AGENTS.md`
- [[ai-feedback-triage-protocol]]
- [[shadow-traffic-rollout-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rubric.yaml`

```yaml
incident_id: <STR>
dimensions:
  - name: user_impact
    anchors:
      1: "0 users affected"
      3: "<100 users"
      5: ">10k users"
  - name: regression_magnitude
    anchors:
      1: "<2%"
      3: "5-15%"
      5: ">20%"
  - name: blast_radius
    anchors:
      1: "single endpoint"
      3: "single feature"
      5: "all AI flows"
weights:        # pre-registered; lock before scoring
  user_impact: 0.4
  regression_magnitude: 0.4
  blast_radius: 0.2
raters: []
```

### `templates/rubric-instance.json`

```json
{
  "incident_id": "INC-2026-04-12-001",
  "dimensions": [
    {
      "name": "user_impact",
      "anchors": {
        "1": "0 users",
        "3": "<100 users",
        "5": ">10k users"
      }
    },
    {
      "name": "regression_magnitude",
      "anchors": {
        "1": "<2%",
        "3": "5-15%",
        "5": ">20%"
      }
    },
    {
      "name": "blast_radius",
      "anchors": {
        "1": "single endpoint",
        "3": "single feature",
        "5": "all AI flows"
      }
    }
  ],
  "scores": [
    {
      "dimension": "user_impact",
      "score": 4,
      "evidence": "log shows 4.2k users hit error path in 1h"
    },
    {
      "dimension": "regression_magnitude",
      "score": 3,
      "evidence": "p50 quality -0.08 vs baseline"
    },
    {
      "dimension": "blast_radius",
      "score": 3,
      "evidence": "single feature (refund-chat)"
    }
  ],
  "weights": {
    "user_impact": 0.4,
    "regression_magnitude": 0.4,
    "blast_radius": 0.2
  },
  "composite": 3.4,
  "lane": "model-regression",
  "raters": [
    "jane@team.io",
    "alex@team.io"
  ],
  "evidence_refs": [
    "dashboard://incidents/INC-2026-04-12-001",
    "log://prom/refund-chat"
  ]
}
```
