# Structured Interview Design

## Summary

**One-sentence:** Produces a structured interview spec: round map, competency-to-round assignment, scorecard, debrief contract.

**One-paragraph:** Produces a structured interview spec: round map, competency-to-round assignment, scorecard, debrief contract. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Дизайн нового interview process з нуля для нової role family.
- Заміна kit з низькою correlation hire-success.
- Defensible structure для diversity audit і pay-equity review.

## Applies If (ALL must hold)

- Designing the interview process for a new role family.
- Existing interview kit shows low hire-success correlation.
- Leadership wants a defensible structure for diversity audits.

## Skip If (ANY kills it)

- Single-interview hire (e.g., contractor for <60 days).
- Reuse of a working kit from an adjacent role (modify, do not rebuild).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Role scorecard | markdown | hiring manager |
| Pool of interviewers + calendars | list | recruiting |
| Time budget per round | constraint | hiring manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[star-interview-framework]] | Behavioral rounds will use the calibrated STAR rubric |
| [[recruiting-process]] | Structured interview is one stage in the full-cycle pipeline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
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
| `templates/interview-design-doc.md` | Structured interview spec skeleton with round map + competency assignment |
| `templates/scorecard.md` | Per-round scorecard template tied to the design doc competencies |
| `templates/_smoke-test.md` | Filled-in spec for a Senior Engineer role with 4 rounds |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-interview-design.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[star-interview-framework]]
- [[star-interview-method]]
- [[recruiting-process]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
