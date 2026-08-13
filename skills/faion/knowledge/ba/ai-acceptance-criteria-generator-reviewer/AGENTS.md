# AI Acceptance Criteria Generator Reviewer

## Summary

**One-sentence:** Reviewer rubric that scores LLM-drafted acceptance criteria across happy/negative/edge/perf/a11y dimensions and gates them on evidence + frozen weights.

**One-paragraph:** Modern BAs generate acceptance criteria with an LLM; the failure mode is half-baked AC slipping into the backlog. This methodology codifies the reviewer pass: a numeric 0-100 rubric with anchored dimensions (happy path, negative cases, edge cases, performance thresholds, accessibility), evidence-per-score discipline, frozen pre-scoring weights, and a reconciliation step when scores diverge. Output is a `rubric` artefact: `dimensions[]` + `instance_scores[]` + `weighted_total`.

**Ефективно для:**

- Reviewer pass на LLM-згенерованих acceptance criteria перед merge у backlog.
- Cohort comparison кількох AC варіантів від різних агентів / промптів.
- Audit trail для регульованих доменів — кожен score з evidence_ref.
- Calibration multi-rater сесії для P4 BA команди.

## Applies If (ALL must hold)

- LLM generates AC drafts at scale (≥3 stories/sprint) and a structured reviewer pass is required.
- Each criterion has a defined 1-5 anchor; raters trained on the rubric before scoring.
- Scores will be used for a binary decision (advance to dev, reject, rework).
- ≥2 raters per instance for any AC that gates a >$10k or strategic story.

## Skip If (ANY kills it)

- n < 3 AC sets — gut feel is faster and accuracy is similar.
- Decisions are single-criterion (deadline-only) — full rubric is overhead.
- One-off prototype AC that will be rewritten next sprint anyway.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| LLM-drafted AC set | Markdown / Gherkin | upstream story generator |
| Rubric anchors file | YAML / Markdown table | BA lead |
| Evidence pointers | URLs, doc paragraphs, trace IDs | story author / prompt log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[acceptance-criteria]] | Canonical AC format (Gherkin / G-W-T) and INVEST checks |
| [[ai-elicitation-prompt-patterns]] | The prompt patterns whose output this rubric scores |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: anchored scales, evidence per score, ≥2 raters for high-stakes, frozen weights | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing evidence, weight reverse-engineering, halo, generic anchors, single-rater high-stakes | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: define dimensions → freeze weights → score with evidence → reconcile → emit composite | 700 |
| `content/06-decision-tree.xml` | essential | Routing on AC stakes + rater count → which rule fires | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_criterion_score` | sonnet | Anchored 1-5 judgment per dimension. |
| `evidence_extraction` | haiku | Mechanical pull of quoted evidence from drafts. |
| `multi_rater_reconciliation` | opus | Resolve divergent scores with rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | Rubric skeleton with anchors_1_3_5 + weights + dimensions |
| `templates/_smoke-test.json` | Minimum viable filled-in rubric for one AC set |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-acceptance-criteria-generator-reviewer.py` | Validate emitted rubric against output-contract schema | CI on each rubric file; pre-commit gate |

## Related

- [[acceptance-criteria]]
- [[ai-elicitation-prompt-patterns]]
- [[ai-assisted-requirements-elicitation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on observable signals (AC stakes value, rater count, evidence completeness) to one of the 4 core rules. Use it when in doubt whether a single-rater pass suffices or reconciliation is required.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rubric.json`

```json
{
  "dimensions": [
    {
      "name": "happy_path",
      "anchors_1_3_5": {
        "1": "no happy path covered",
        "3": "one primary flow covered",
        "5": "all primary flows covered with preconditions"
      },
      "weight": 0.3
    },
    {
      "name": "negative_cases",
      "anchors_1_3_5": {
        "1": "no negative cases",
        "3": "1-2 common failure modes",
        "5": "all common failure modes + clear error contracts"
      },
      "weight": 0.25
    },
    {
      "name": "edge_cases",
      "anchors_1_3_5": {
        "1": "no edge handling",
        "3": "boundaries only (min/max)",
        "5": "boundary + null + overflow + concurrency"
      },
      "weight": 0.2
    },
    {
      "name": "performance_thresholds",
      "anchors_1_3_5": {
        "1": "no SLA stated",
        "3": "p95 latency target only",
        "5": "p50/p95/p99 + throughput + degradation policy"
      },
      "weight": 0.15
    },
    {
      "name": "accessibility",
      "anchors_1_3_5": {
        "1": "no a11y mention",
        "3": "WCAG AA target stated",
        "5": "AA + keyboard-only + screen-reader transcript per AC"
      },
      "weight": 0.1
    }
  ],
  "instance_scores": [],
  "rater_count": 1,
  "weighted_total": 0,
  "weights_locked_at": "REPLACE_WITH_ISO8601_BEFORE_SCORING"
}
```

### `templates/_smoke-test.json`

```json
{
  "dimensions": [
    {
      "name": "happy_path",
      "anchors_1_3_5": {
        "1": "missing",
        "3": "one path",
        "5": "all flows"
      },
      "weight": 0.5
    },
    {
      "name": "negative",
      "anchors_1_3_5": {
        "1": "none",
        "3": "some",
        "5": "all failure modes"
      },
      "weight": 0.3
    },
    {
      "name": "edge",
      "anchors_1_3_5": {
        "1": "none",
        "3": "boundary",
        "5": "boundary+null+overflow"
      },
      "weight": 0.2
    }
  ],
  "instance_scores": [
    {
      "instance_id": "AC-smoke",
      "dimension_scores": [
        {
          "dimension": "happy_path",
          "score": 4,
          "evidence_refs": [
            "draft.md#L1"
          ]
        },
        {
          "dimension": "negative",
          "score": 3,
          "evidence_refs": [
            "draft.md#L5"
          ]
        },
        {
          "dimension": "edge",
          "score": 5,
          "evidence_refs": [
            "draft.md#L9"
          ]
        }
      ]
    }
  ],
  "rater_count": 2,
  "weighted_total": 76.0,
  "weights_locked_at": "2026-05-23T09:00:00Z"
}
```
