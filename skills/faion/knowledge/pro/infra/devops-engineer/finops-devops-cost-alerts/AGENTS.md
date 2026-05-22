---
slug: finops-devops-cost-alerts
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Budget alerts at 50/75/90/100% thresholds prevent surprise overspend by notifying teams before the billing period closes.
content_id: "d84d51ede3f33047"
tags: [finops, budget-alerts, anomaly-detection, cost-reporting, llm-prompts]
---
# FinOps Budget Alerts, Anomaly Investigation, and Cost Reporting

## Summary

**One-sentence:** Budget alerts at 50/75/90/100% thresholds prevent surprise overspend by notifying teams before the billing period closes.

**One-paragraph:** Budget alerts at 50/75/90/100% thresholds prevent surprise overspend by notifying teams before the billing period closes. Anomaly detection catches intra-period spikes (new deployment, configuration error, traffic event) within hours. Structured LLM prompts accelerate cost analysis, rightsizing review, commitment planning, and executive reporting — reducing FinOps analyst time per cycle from days to hours.

## Applies If (ALL must hold)

- Setting up any cloud account — budget alerts at all four thresholds should be Day 1 infrastructure, not an afterthought.
- Monthly billing review — use LLM prompts to generate the initial analysis, then verify the top recommendations manually.
- A cost spike appears in anomaly detection — use the investigation prompt to structure the root-cause analysis.
- Preparing quarterly commitment reviews (Savings Plans / RIs) — use the commitment prompt to structure the analysis.
- Generating executive or team-level cost reports — prompts produce consistent format across reporting periods.

## Skip If (ANY kills it)

- Replacing human judgment for commitment purchases — LLM prompts surface candidates and trade-offs; a human must approve multi-thousand-dollar commitments.
- Auto-remediating anomalies without an approval step — auto-termination of a resource identified by anomaly detection can cause an incident if misclassified.

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
