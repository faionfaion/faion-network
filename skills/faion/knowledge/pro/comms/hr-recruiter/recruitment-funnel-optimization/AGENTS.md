---
slug: recruitment-funnel-optimization
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a funnel report identifying the single bottleneck stage and an experiment plan to lift its conversion.
content_id: "6a881d8b779e5105"
complexity: medium
produces: report
est_tokens: 5400
tags: [recruiting, funnel, conversion, metrics, diagnosis]
---

# Recruitment Funnel Optimization

## Summary

**One-sentence:** Produces a funnel report identifying the single bottleneck stage and an experiment plan to lift its conversion.

**One-paragraph:** Produces a funnel report identifying the single bottleneck stage and an experiment plan to lift its conversion. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Діагностика, чому конкретна стадія воронки не конвертить (drop-off на screening, interview, offer).
- Побудова експерименту з підняття конверсії одного етапу.
- Звіт для leadership з єдиним bottleneck + планом дій.

## Applies If (ALL must hold)

- ≥90 days of funnel data exist for the role / role family being optimized.
- Hiring manager and recruiting agree on a target metric to improve (time-to-fill, offer accept, quality of hire).
- Conversion data is segmented by stage (applied → screen → interview → offer → accept).

## Skip If (ANY kills it)

- Funnel has <50 candidates total — sample too small for any conclusion.
- Same role has had ≥3 different hiring managers in the period — confound dominates the signal.
- Recruiting team is mid-tool migration — measurement is unreliable until migration settles.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stage-level conversion data | csv / sheet | ATS export |
| Time-in-stage data | csv / sheet | ATS export |
| Loss-reason tags | csv / sheet | ATS / recruiter notes |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[recruiting-process]] | Need to know the canonical full-cycle stages to attribute losses correctly |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
| `content/05-examples.xml` | reference | One full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/funnel-report.md` | Funnel diagnosis report skeleton with bottleneck section + experiment plan |
| `templates/_smoke-test.md` | Filled-in report for a worked example (Senior Engineer role, screen→interview drop) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-recruitment-funnel-optimization.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[recruiting-process]]
- [[structured-interview-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
