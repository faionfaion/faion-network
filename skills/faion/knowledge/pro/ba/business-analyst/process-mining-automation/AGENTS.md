---
slug: process-mining-automation
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Event-log driven process discovery + automation candidate scoring (volume × frequency × variance × rule-density) producing a ranked automation pipeline with RPA/IDP/orchestration verdict per candidate.
content_id: "59b4220324dc8b5c"
complexity: deep
produces: report
est_tokens: 5400
tags: [process-mining, automation-assessment, rpa, event-logs, data-driven]
---
# Process Mining and Intelligent Automation Analysis

## Summary

**One-sentence:** Event-log driven process discovery + automation candidate scoring (volume × frequency × variance × rule-density) producing a ranked automation pipeline with RPA/IDP/orchestration verdict per candidate.

**One-paragraph:** A data-driven methodology for discovering actual process execution from IT event logs (Celonis, Disco, PM4Py, ProM) and identifying automation candidates using objective scoring criteria. Replaces interview-based process models (the ideal) with conformance-checked event-log models (the actual). Output: ranked automation candidate list with verdict (RPA, IDP, orchestration, none) and ROI estimate per candidate.

**Ефективно для:**

- RPA programme prioritisation з reality-based event log evidence.
- Conformance audit: де actual process розходиться з documented.
- ERP migration: витягти as-is з legacy event logs замість stakeholder interviews.
- Continuous improvement з monthly mining cadence + drift detection.

## Applies If (ALL must hold)

- Existing IT systems emit event logs (timestamp, case_id, activity) suitable for mining.
- RPA programme prioritisation across N candidate processes.
- Conformance audit: where does actual process diverge from documented?
- ERP rollout: extract as-is process from legacy logs.
- Continuous improvement programme with monthly mining cadence.

## Skip If (ANY kills it)

- Manual / paper-based process with no event logs.
- Pure ad-hoc work where case_id is undefined.
- Single-process automation already justified — skip mining; do POC.
- Privacy / regulatory restriction prevents log access.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Event log access | CSV / Celonis / DB | data platform |
| Case ID + activity + timestamp present | schema check | data engineering |
| Process scope list | Markdown | BA / sponsor |
| Mining tool credentials | env | infra |
| Scoring matrix template | YAML | this methodology |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/business-process-analysis` | Provides BPMN convention guide for to-be. |
| `pro/ba/business-analyst/frontline-validation-protocol` | Validates discovered model with operators. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `event-log-profiling` | haiku | Mechanical schema + completeness check. |
| `process-discovery` | sonnet | Run alpha/heuristic miner; emit as-is BPMN. |
| `conformance-check` | sonnet | Token-replay; identify deviations. |
| `automation-scoring` | sonnet | Score candidates against the scoring matrix. |
| `roi-estimation` | opus | Cross-system cost/benefit with risk. |

## Templates

| File | Purpose |
|------|---------|
| `templates/automation-assessment.md` | Per-candidate automation assessment template. |
| `templates/conformance-report.md` | Per-process conformance report. |
| `templates/scoring-matrix.yaml` | Volume/frequency/variance/rule-density scoring matrix. |
| `templates/_smoke-test.md` | Minimum filled-in report. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-process-mining-automation.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[business-process-analysis]]
- [[frontline-validation-protocol]]
- [[data-analysis]]
- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
