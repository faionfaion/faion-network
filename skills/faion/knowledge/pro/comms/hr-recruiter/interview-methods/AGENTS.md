---
slug: interview-methods
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Structured-interview bundle (competencies → questions → scorecards → debrief): cap competencies at 4-6, behavioral anchors observable verbs only.
content_id: "de8c6812cf983c95"
complexity: medium
produces: spec
est_tokens: 5000
tags: [structured-interview, hiring, behavioral-interview, competencies, hr]
---
# Interview Methods

## Summary

**One-sentence:** Structured-interview bundle (competencies → questions → scorecards → debrief): cap competencies at 4-6, behavioral anchors observable verbs only.

**One-paragraph:** Structured-interview bundle (competencies → questions → scorecards → debrief): cap competencies at 4-6, behavioral anchors observable verbs only. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- standing up interview process from scratch for a new role family.
- audit existing process з interview-to-offer rate поза 15-25% band.
- calibration інтерв'юерів через географії, де in-person impractical.
- rollout structured interviews after hiring-manager change.
- competencies cap 4-6 з вагами, що сумуються до 100%.

## Applies If (ALL must hold)

- standing up an interview process from scratch for a new role family.
- auditing an existing process whose interview-to-offer rate falls outside the 15-25% band.
- calibrating interviewers across geographies where in-person calibration is impractical.
- rolling out structured interviews after a hiring-manager change.

## Skip If (ANY kills it)

- single-hire one-off (founder hiring a co-founder, exec search).
- roles where the only valid signal is portfolio review (illustrators, cinematographers).
- volume retail or hourly hiring at scale — use realistic job previews.
- statutorily-fixed questionnaires (clinical, legal regulated roles).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-methods.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-interview-methods.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[30-60-90-day-plan]]
- [[employee-value-proposition]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
