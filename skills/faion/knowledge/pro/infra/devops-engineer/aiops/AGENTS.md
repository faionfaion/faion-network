---
slug: aiops
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AIOps applies ML and LLM-powered analysis to IT operations to automate anomaly detection, root cause analysis, and incident remediation.
content_id: "fa4838d8ad1a0cbb"
tags: [aiops, observability, incident-response, machine-learning, self-healing]
---
# AIOps: ML-Powered Incident Detection and Auto-Remediation

## Summary

**One-sentence:** AIOps applies ML and LLM-powered analysis to IT operations to automate anomaly detection, root cause analysis, and incident remediation.

**One-paragraph:** AIOps applies ML and LLM-powered analysis to IT operations to automate anomaly detection, root cause analysis, and incident remediation. The five capabilities are: anomaly detection, root cause analysis, predictive alerts, auto-remediation, and capacity planning. Every auto-remediation action must be classified by risk level and gated by a human-approval policy for P1/P2 incidents.

## Applies If (ALL must hold)

- Reducing MTTR by automating triage and RCA across metrics, logs, and traces.
- Alert noise reduction — raw event stream too high for manual triage.
- Building self-healing systems with human-approval gates for risky actions.
- Establishing SLO-aware alerting based on error-budget burn rates.

## Skip If (ANY kills it)

- Teams without an observability foundation (Prometheus + structured logs + traces) — collect data first.
- Organizations that have not defined SLOs — anomaly detection without SLOs produces meaningless alerts.
- Small services with predictable failure modes — static runbooks and on-call rotation are sufficient.
- When explainability/audit requirements are strict and ML model decisions cannot be logged with reasoning.

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
