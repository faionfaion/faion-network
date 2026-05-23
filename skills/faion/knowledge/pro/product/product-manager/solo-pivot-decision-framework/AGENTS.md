---
slug: solo-pivot-decision-framework
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Opinionated pivot taxonomy (segment / feature / business-model / tech / channel) with quantitative trigger signals, sunk-cost guardrails, and a hard rule for distinguishing pivot from quit for solo SaaS founders.
content_id: "23a41765dac49322"
complexity: deep
produces: decision-record
est_tokens: 6100
tags: [pivot, product-market-fit, decision-framework, solo-saas, sunk-cost]
---
# Solo Pivot Decision Framework

## Summary

**One-sentence:** Opinionated pivot taxonomy (segment / feature / business-model / tech / channel) with quantitative trigger signals, sunk-cost guardrails, and a hard rule for distinguishing pivot from quit for solo SaaS founders.

**One-paragraph:** Five pivot categories, quantitative triggers (MRR flat, activation <5%, churn >8%/mo, NPS <0), explicit sunk-cost disclosure, runway feasibility gate (>=8 weeks), 3-pivot rule (quit instead of pivot a fourth time). Output: pivot-decision-record markdown.

**Ефективно для:**

- v1 живий >=90 днів із paying/free users + >=1 failure signal.
- Operator має >=8 weeks personal runway виконати pivot.
- Попередній квартал містив >4 години customer-development розмов.
- Sunk-cost bias loomed — рамка дає quantified триггери і guardrails.

## Applies If (ALL must hold)

- v1 has been live >=90 days with paying or free users.
- >=1 of the failure signals is true: MRR flat/down, activation <5%, churn >8%/mo, NPS <0.
- Operator has >=8 weeks of personal runway to execute the pivot.
- Previous quarter included >4 hours of customer development conversation.
- Sunk-cost continuation pressure is building.

## Skip If (ANY kills it)

- Pre-launch product with no users (use customer-development).
- Engagement < 90 days live (give it time).
- >=2-founder team (use co-founder pivot methodology).
- Profitable product seeking optimization not pivot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trailing 30/60/90d metrics | table | product-analytics |
| Customer-development log | list | interview notes |
| Personal runway | weeks remaining | founder |
| Sunk-cost ledger | list | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[product-lifecycle]] | Stage classification informs whether the metrics are pivot-warranting. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: pivot taxonomy, quantitative triggers, sunk-cost disclosed, runway gate, 3-pivot quit rule | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for pivot-decision-record | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: vibe-pivot, sunk-cost continuation, runway-less pivot, serial pivot | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: evaluate triggers -> classify type -> disclose sunk -> check runway -> author DR | 900 |
| `content/05-examples.xml` | medium | Worked DR pivoting on segment trigger after 3 months | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on age + triggers + runway | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `trigger-evaluate` | sonnet | Match observed metrics to quantitative triggers. |
| `pivot-type-classify` | sonnet | Map proposed change to one of 5 categories. |
| `decision-record-author` | opus | Write the DR with sunk-cost disclosure + runway gate + kill rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pivot-decision-record.md` | DR skeleton with type + triggers + sunk-cost + runway. |
| `templates/pivot-trigger-check.sh` | Check quantitative triggers against metrics. |
| `templates/runway-gate.yaml` | Runway-feasibility-gate input template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-pivot-decision-framework.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[product-lifecycle]]
- [[continuous-discovery-habits]]
- [[portfolio-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
