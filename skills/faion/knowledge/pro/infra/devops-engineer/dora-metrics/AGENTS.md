---
slug: dora-metrics
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Five DORA metrics measure software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service (MTTR), and Reliability (SLO compliance).
content_id: "b0d7d14c181a3387"
tags: [dora, metrics, software-delivery, performance-measurement, deployment-frequency]
---
# DORA Metrics

## Summary

**One-sentence:** Five DORA metrics measure software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service (MTTR), and Reliability (SLO compliance).

**One-paragraph:** Five DORA metrics measure software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service (MTTR), and Reliability (SLO compliance). Elite teams deploy 973x more frequently and recover 6570x faster than low performers. Measure all five together — high frequency with high CFR signals process problems, not success.

## Applies If (ALL must hold)

- Establishing baseline software delivery performance for a team or service
- Identifying delivery bottlenecks (where does lead time accumulate?)
- Evaluating impact of process changes (did trunk-based dev improve deploy frequency?)
- Building engineering dashboards for leadership aligned to business outcomes
- Assessing AI tooling adoption impact on delivery stability (2025: AI improves throughput but increases CFR)

## Skip If (ANY kills it)

- Individual performance reviews — DORA measures team/system outcomes, not individuals
- Comparing teams without context — team size, domain complexity, and tech debt differ
- Single-metric focus — optimize one metric without watching others (e.g., deploy frequency up but CFR up too)
- Fewer than 30 days of data — baselines are meaningless without sufficient history

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/devops-engineer/`
