---
slug: ai-incident-triage-matrix
tier: pro
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Numeric scoring rubric (1-5 anchored, weighted blend) that classifies an AI-feature incident across 5 lanes (model-regression / prompt-injection / data-drift / upstream-API / cost-runaway) and routes to lane-specific mitigation.
content_id: "51d93796a7bb57d3"
complexity: medium
produces: rubric
est_tokens: 4400
tags: [ai, scorecard, incident, triage, ml-engineering]
---
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-incident-triage-matrix.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ai/ml-engineer/AGENTS.md`
- [[ai-feedback-triage-protocol]]
- [[shadow-traffic-rollout-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
