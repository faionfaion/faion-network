# AIOps

## Summary

AIOps applies ML and LLM-powered analysis to IT operations to automate anomaly detection, root cause analysis, and incident remediation. The five capabilities are: anomaly detection, root cause analysis, predictive alerts, auto-remediation, and capacity planning. Every auto-remediation action must be classified by risk level and gated by a human-approval policy for P1/P2 incidents.

## Why

Alert fatigue causes teams to miss critical signals; AIOps platforms correlate raw events (reducing noise 80%+) and surface ranked probable causes. LLM integration enables natural-language incident summaries and AI-generated runbooks. Change-aware correlation (linking RCA to recent deployments/config changes) dramatically improves diagnosis accuracy. Gartner projects 60%+ of large enterprises will adopt self-healing systems by 2026.

## When To Use

- Reducing MTTR by automating triage and RCA across metrics, logs, and traces.
- Alert noise reduction — raw event stream too high for manual triage.
- Building self-healing systems with human-approval gates for risky actions.
- Establishing SLO-aware alerting based on error-budget burn rates.

## When NOT To Use

- Teams without an observability foundation (Prometheus + structured logs + traces) — collect data first.
- Organizations that have not defined SLOs — anomaly detection without SLOs produces meaningless alerts.
- Small services with predictable failure modes — static runbooks and on-call rotation are sufficient.
- When explainability/audit requirements are strict and ML model decisions cannot be logged with reasoning.

## Content

| File | What's inside |
|------|---------------|
| `content/01-capabilities.xml` | Five core capabilities, architecture data-flow, tool landscape, 2025-2026 evolution trends, success metrics |
| `content/02-checklists.xml` | Anomaly detection, RCA, incident management, auto-remediation, platform selection, quarterly audit checklists |

## Templates

none
