# STAR Interview — Example Question Bank

## Summary

**One-sentence:** Per-competency STAR question bank with calibration anchors — a vetted reusable interviewer checklist.

**One-paragraph:** Per-competency STAR question bank with calibration anchors — a vetted reusable interviewer checklist. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Старт нового interview kit з question bank, прив'язаним до competencies, а не до загальних 'tell me about'.
- Onboarding нового інтервюера: ready-made калібрувальні приклади.
- Заміна питань у kit з низькою inter-rater agreement.

## Applies If (ALL must hold)

- Interview kit needs question seeds tied to specific competencies.
- New interviewer onboarding needs calibration examples.
- Existing kit has shown low inter-rater agreement and needs replacement questions.

## Skip If (ANY kills it)

- Kit already passes ≥0.6 inter-rater agreement — do not change tools that work.
- Role is so specialized that off-the-shelf questions do not map (research science, founding-engineer).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Role scorecard with named competencies | markdown | hiring manager |
| Calibration anchors per competency | markdown | interview lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[star-interview-method]] | Need the underlying STAR scoring rubric to interpret each question |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
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
| `templates/star-question-bank.md` | Question bank skeleton: competency → question → calibration anchor |
| `templates/interviewer-training-agenda.md` | Agenda for the 60-minute interviewer-onboarding session |
| `templates/scorecard-qa-checklist.md` | Pre-debrief QA checklist for completed scorecards |
| `templates/_smoke-test.md` | Filled-in question bank for 'communication' competency |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-star-interview-examples.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[star-interview-method]]
- [[star-interview-framework]]
- [[structured-interview-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
