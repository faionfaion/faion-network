# Process Mining & Automation

## Summary

**One-sentence:** Produces an automation-assessment report ranking discovered process variants by frequency × variance × cost and naming candidate automations with feasibility scores.

**One-paragraph:** Produces an automation-assessment report ranking discovered process variants by frequency × variance × cost and naming candidate automations with feasibility scores. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Транзакційна система (ERP/CRM/ticketing) ≥6 місяців даних — є що mine'ити.
- Automation programme з обмеженим бюджетом — треба ranked candidate list з feasibility.
- Compliance audit, де треба показати actual-vs-documented process flow.
- Discovery про прихований process variance, який stakeholder'и заперечують.

## Applies If (ALL must hold)

- Existing transactional system with event logs (ERP, CRM, ticketing) ≥ 6 months of data.
- Stakeholder believes process is standard but data may reveal high variance.
- Automation programme needs prioritised candidate list with feasibility evidence.
- Compliance audit requires actual-vs-documented process comparison.

## Skip If (ANY kills it)

- No event log exists or logs lack case-id / activity / timestamp triple.
- Process is genuinely new and lacks operational history.
- Stakeholders refuse to act on findings — analysis becomes shelfware.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event log export (case_id, activity, timestamp, resource) | CSV / XES | data engineering |
| Process mining tool access (Celonis / Disco / pm4py) | license / pip | BA / data team |
| Cost data per activity | CSV | finance |
| Stakeholder hypothesis log | Markdown | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[data-driven-requirements]] | process-mining evidence feeds requirement derivation |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ingest-and-clean` | haiku | Mechanical CSV cleanup + case-id normalisation. |
| `discover-variants` | sonnet | Apply pm4py / Disco discovery; rank variants by frequency × cost. |
| `score-automation` | opus | Synthesise feasibility scores with rationale per candidate. |
| `write-report` | sonnet | Assemble final report with rankings + evidence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/automation-assessment.md` | Report skeleton: variants ranked, candidate automations, feasibility. |
| `templates/pm-feasibility-audit.py` | Stdlib audit checking event-log integrity before mining. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-process-mining-automation.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[data-driven-requirements]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
