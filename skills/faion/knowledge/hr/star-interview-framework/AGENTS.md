# STAR Interview Framework

## Summary

**One-sentence:** Calibrated STAR rubric: per-competency anchors, scoring scale, debrief contract — produces a usable interview scorecard.

**One-paragraph:** Calibrated STAR rubric: per-competency anchors, scoring scale, debrief contract — produces a usable interview scorecard. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Підняття inter-rater agreement через явні behavior anchors і debrief contract.
- Defensible hire/no-hire рішення з посиланням на калібрований scorecard.
- Onboarding нових інтервюерів з прив'язкою до того ж самого rubric.

## Applies If (ALL must hold)

- Team needs a calibrated rubric, not just questions.
- Inter-rater agreement on the current kit is below target.
- Hiring manager wants behavior anchors to argue hire/no-hire decisions defensibly.

## Skip If (ANY kills it)

- Single-interviewer role where calibration is moot.
- Role uses work-sample tests as primary signal — rubric duplicates effort.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Role scorecard with 4-6 competencies | markdown | hiring manager |
| STAR question bank | markdown | star-interview-examples |
| Calibration session attendees | list | interview lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[star-interview-method]] | Method definitions ground the rubric vocabulary |
| [[star-interview-examples]] | Question bank feeds the rubric anchors |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure with input/action/output per step | 1000 |
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
| `templates/star-scorecard.md` | Scorecard skeleton: competency × scale × behavior anchor + evidence slot |
| `templates/interviewer-guide.md` | Guide explaining how to use the rubric live in an interview |
| `templates/_smoke-test.md` | Filled-in scorecard for a single candidate × competency |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-star-interview-framework.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[star-interview-method]]
- [[star-interview-examples]]
- [[structured-interview-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
