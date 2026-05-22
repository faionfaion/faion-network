---
slug: take-home-rubric-template
tier: geek
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Versioned, owner-signed engineering take-home rubric: weighted criteria, anchor descriptions per band, calibration sample, hire/no-hire threshold."
content_id: "24b7b0d34626bcd8"
complexity: light
produces: rubric
est_tokens: 2900
tags: [hiring, take-home, rubric, interview, geek, dev]
---

# Take-Home Rubric Template

## Summary

**One-sentence:** Versioned, owner-signed engineering take-home rubric: weighted criteria, anchor descriptions per band, calibration sample, hire/no-hire threshold.

**One-paragraph:** Versioned, owner-signed engineering take-home rubric: weighted criteria, anchor descriptions per band, calibration sample, hire/no-hire threshold. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`rubric`) at a light complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Team runs a take-home stage in its engineering interview loop.
- Multiple reviewers will score the same submission independently.
- Hiring decision uses a written rubric, not gut-feel.

## Skip If (ANY kills it)

- Take-home stage already has a calibrated rubric in steady use — replace, do not duplicate.
- Hiring is greenfield prototype with no production users (scale doesn't justify rubric overhead).
- Regulatory / compliance constraints override generic rubric guidance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Take-home prompt | Markdown / PDF | hiring manager |
| Calibration submission | code repo | team lead |
| Owner sign-off slot | Slack / DocuSign | engineering director |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/interview-loop-charter` | Defines the broader interview loop this rubric slots into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `rubric_draft_inputs_summary` | haiku | Bounded transform of prompt → criteria list. |
| `rubric_synthesize_anchors` | sonnet | Per-criterion band-anchor authoring. |
| `rubric_review_for_bias` | opus | Cross-criteria bias and fairness audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/take-home-rubric.md` | Markdown skeleton with weighted criteria + band anchors. |
| `templates/take-home-rubric.json` | Machine-readable JSON of the rubric. |
| `templates/calibration-sample-score.md` | Filled-in calibration example. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-take-home-rubric-template.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/dev/`
- `[[interview-loop-charter]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether take-home-rubric-template applies: root question — "Is this an engineering take-home stage with ≥2 independent reviewers?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
