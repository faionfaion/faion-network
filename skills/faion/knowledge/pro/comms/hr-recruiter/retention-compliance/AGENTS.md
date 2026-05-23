---
slug: retention-compliance
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Retention diagnostic and compliance audit report with prioritized fix list per regulation domain.
content_id: "b116a66893514663"
complexity: medium
produces: report
est_tokens: 5400
tags: [retention, compliance, attrition, gdpr, eeoc]
---

# Retention and HR Compliance

## Summary

**One-sentence:** Retention diagnostic and compliance audit report with prioritized fix list per regulation domain.

**One-paragraph:** Retention diagnostic and compliance audit report with prioritized fix list per regulation domain. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Діагностика підвищеної voluntary attrition для population з достатнім розміром.
- Підготовка до compliance аудиту (SOX, GDPR, EEOC, EU AI Act) у HR/recruiting процесах.
- Пріоритезований план виправлень для leadership з обґрунтуванням ROI.

## Applies If (ALL must hold)

- Voluntary attrition for a population has been above target for ≥2 quarters.
- A compliance audit (SOX, GDPR, EEOC, EU AI Act) is scheduled or recently flagged a recruiting/HR control.
- Leadership has approved retention or compliance investment beyond business-as-usual.

## Skip If (ANY kills it)

- Attrition spike is single-quarter noise (<2 quarters).
- Compliance audit owned by external counsel — they own the artefact, not us.
- Population <30 employees — privacy and statistical power both fail.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 12-month attrition dataset | csv / sheet | HRIS |
| Exit interview themes | doc / sheet | people ops |
| Regulatory scope list | markdown | legal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[recruiting-process]] | Some attrition drivers begin at hiring stage and require recruiting-side fixes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + rationale + source | 1200 |
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
| `templates/retention-compliance-report.md` | Diagnostic report skeleton with attrition + compliance findings sections |
| `templates/_smoke-test.md` | Worked example for engineering org with GDPR + attrition findings |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retention-compliance.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[recruiting-process]]
- [[onboarding-60-90-day]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
