---
slug: onboarding-60-90-day
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Two-phase ramp framework producing a day-60 gate + day-90 review checklist anchored to artifacts.
content_id: "480d23f42be1c31e"
complexity: medium
produces: checklist
est_tokens: 4500
tags: [onboarding, 60-90-day, new-hire-ramp, performance-review, milestones]
---

# 60-90 Day Onboarding Phases

## Summary

**One-sentence:** Two-phase ramp framework producing a day-60 gate + day-90 review checklist anchored to artifacts.

**One-paragraph:** Two-phase ramp framework producing a day-60 gate + day-90 review checklist anchored to artifacts. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Перехід нового співробітника з фази навчання у фази Contribute (31-60) і Execute (61-90).
- Документований gate на день 60 з конкретним артефактом, а не оцінкою активності.
- Skip-level check-in на день 45 для незалежного сигналу про прогрес.

## Applies If (ALL must hold)

- Hire has cleared 30-day learning criteria and needs explicit Contribute (31-60) and Execute (61-90) milestones.
- Manager wants a structured second-and-third-month plan separate from the broad 30-60-90 framework.
- Role has ramp quotas or feature ownership (sales, engineering) where deliverables land in this window.
- Preparing a defensible 90-day review with an artifact trail.

## Skip If (ANY kills it)

- Hire is still failing day-30 criteria — resolve or restart the cycle first.
- Role has multi-quarter ramp (Enterprise AE, ML researcher) — extend phases; do not compress.
- Senior autonomous hire who defines their own deliverables.
- Contract placement under 60 days.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Day-30 outcome record | markdown | manager |
| Role scorecard | markdown / sheet | hiring manager |
| Project candidate list | list | team backlog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[onboarding-30-day]] | 30-day learning phase must be closed before this phase opens |

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
| `templates/checklist-60-90.md` | Day-60 and day-90 milestone checklist with artifact slots |
| `templates/_smoke-test.md` | Minimum viable filled-in checklist for a generic engineering hire |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-onboarding-60-90-day.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[onboarding-30-day]]
- [[structured-interview-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
