---
slug: recruiting-process
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Full-cycle hiring playbook step covering sourcing, JD, screening, interview, offer, with metric-anchored gates.
content_id: "f3c1f1eb8740c561"
complexity: deep
produces: playbook-step
est_tokens: 4500
tags: [recruiting, full-cycle, talent-acquisition, sourcing, hiring-process]
---

# Recruiting Process (Full-Cycle)

## Summary

**One-sentence:** Full-cycle hiring playbook step covering sourcing, JD, screening, interview, offer, with metric-anchored gates.

**One-paragraph:** Full-cycle hiring playbook step covering sourcing, JD, screening, interview, offer, with metric-anchored gates. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Запуск нової ролі або вакансії з потребою побудувати воронку з нуля.
- Аудит JD, ATS workflow або outreach-послідовності для існуючої ролі.
- Впровадження тижневих / місячних метрик recruiting-функції.

## Applies If (ALL must hold)

- Building a sourcing strategy for a new role type or market.
- Diagnosing why a specific stage is underperforming (after funnel diagnosis).
- Designing or auditing a JD, ATS workflow, or candidate outreach sequence.
- Implementing metric reporting for the recruiting function.

## Skip If (ANY kills it)

- Executive search where a retained firm is running the process — overlap creates confusion.
- Single-hire, one-time role where building pipelines and personas is overhead.
- Compliance-audit context — use retention-compliance methodology instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Open requisition | ATS record | hiring manager |
| Role scorecard with 5-7 must-haves | markdown | hiring manager |
| Sourcing channel list | list | recruiting ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[recruitment-funnel-optimization]] | Funnel metrics define which stage needs intervention before applying full-cycle changes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 7-step procedure with input/action/output per step | 1000 |
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
| `templates/recruiting-playbook-step.md` | Full-cycle step skeleton with inputs/outputs/exit-criteria per stage |
| `templates/_smoke-test.md` | Filled-in example for a single Senior Engineer requisition |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-recruiting-process.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[recruitment-funnel-optimization]]
- [[structured-interview-design]]
- [[star-interview-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
