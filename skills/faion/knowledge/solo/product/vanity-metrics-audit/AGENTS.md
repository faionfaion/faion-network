---
slug: vanity-metrics-audit
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Audits an exec dashboard against the 'vanity vs leading vs lagging' test, marks vanity metrics for retirement, supplies a stakeholder script for political defence, and emits a refactored KPI tree.
content_id: "1954945716760d83"
complexity: light
produces: report
est_tokens: 3500
tags: [vanity-metrics-audit, kpi, okr, exec-dashboard]
---
# Vanity Metrics Audit

## Summary

**One-sentence:** Audits an exec dashboard against the 'vanity vs leading vs lagging' test, marks vanity metrics for retirement, supplies a stakeholder script for political defence, and emits a refactored KPI tree.

**One-paragraph:** Audits an exec dashboard against the 'vanity vs leading vs lagging' test, marks vanity metrics for retirement, supplies a stakeholder script for political defence, and emits a refactored KPI tree. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Vanity Metrics Audit on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Exec dashboard has ≥10 KPIs.
- PM has been asked to defend / kill metrics in a leadership review.
- ≥1 stakeholder is emotionally attached to a likely-vanity metric.
- PM has access to underlying metric definitions + sources.

## Skip If (ANY kills it)

- Pre-PMF — no KPIs to audit.
- Compliance dashboards mandated externally.
- Single-KPI startups — nothing to audit.
- Cultural inability to retire metrics — audit will be theatre.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Exec dashboard inventory | list | BI |
| Metric definitions | doc | Analytics |
| Stakeholder map (per metric) | table | PM |
| Outcome / OKR tree | doc | Roadmap |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/solo-kpi-dashboard-template` | Reference shape for solo dashboards. |
| `solo/product/product-operations/product-analytics` | Source of metric definitions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-vanity-metrics-audit` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-vanity-metrics-audit` | haiku | Schema check + threshold checks; deterministic. |
| `review-vanity-metrics-audit` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vanity-metrics-audit.json` | JSON skeleton conforming to the output contract schema. |
| `templates/vanity-metrics-audit.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vanity-metrics-audit.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[solo-kpi-dashboard-template]]
- [[product-analytics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
