---
slug: paid-test-task-scoring-rubric
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a calibrated rubric for scoring paid test tasks with anti-bias controls and pay-on-completion contract.
content_id: "1ed516f318ee6e60"
complexity: medium
produces: rubric
est_tokens: 4500
tags: [test-task, rubric, scoring, pay-on-completion, bias]
---

# Paid Test-Task Scoring Rubric

## Summary

**One-sentence:** Produces a calibrated rubric for scoring paid test tasks with anti-bias controls and pay-on-completion contract.

**One-paragraph:** Produces a calibrated rubric for scoring paid test tasks with anti-bias controls and pay-on-completion contract. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Calibrated rubric для платної test task від кількох reviewers.
- Anti-bias controls: blind scoring, dimension-level anchors, pay-on-completion.
- Захист legal/EU AI Act exposure при автоматичному скорингу.

## Applies If (ALL must hold)

- Test task lasts ≥3 hours and is paid at market hourly rate.
- Multiple candidates will complete the same task in the same hiring window.
- At least two reviewers will score every submission.

## Skip If (ANY kills it)

- Task is <1 hour — use a take-home screener instead.
- Task is real production work — never ship a hiring task to prod.
- Single-reviewer process — rubric calibration is moot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test task brief | markdown | hiring manager |
| Pay rate + payment mechanism | policy | people ops |
| Reviewer pool | list | interview lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[structured-interview-design]] | Rubric is one component of the broader interview kit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `fill-template` | haiku | Mechanical template fill with bounded inputs |
| `apply-rubric` | sonnet | Per-instance judgment against calibrated anchors |
| `cross-check-evidence` | sonnet | Verify each claim cites an input artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-task-rubric.md` | Per-dimension rubric skeleton with 5-level anchors and evidence slots |
| `templates/payment-tracker.md` | Per-candidate payment tracker tied to completion |
| `templates/_smoke-test.md` | Filled-in rubric for a frontend take-home |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-paid-test-task-scoring-rubric.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[structured-interview-design]]
- [[star-interview-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
