# AIOps: ML-Powered Incident Detection and Auto-Remediation

## Summary

**One-sentence:** Produces an AIOps platform config (anomaly detection params, RCA pipeline, auto-remediation risk policy with approval matrix) wired through OpenTelemetry.

**One-paragraph:** AIOps applies ML and LLM-powered analysis to IT operations to automate anomaly detection, root cause analysis, and incident remediation. Five capabilities: anomaly detection, RCA, predictive alerts, auto-remediation, capacity planning. Every auto-remediation action is classified by risk level and gated by a human-approval policy for P1/P2 incidents. Anomaly detection requires >=2 weeks of baseline data and dynamic thresholds tied to SLO error-budget burn rates, not static CPU > 80% thresholds.

**Ефективно для:**

- reducing MTTR by automating triage and RCA across metrics, logs, traces.
- alert noise reduction — raw event stream too high for manual triage.
- building self-healing systems with human-approval gates for risky actions.
- establishing SLO-aware alerting based on error-budget burn rates.

## Applies If (ALL must hold)

- Service has >= 2 weeks of metrics + logs + traces collected through OpenTelemetry or equivalent.
- SLOs are defined with explicit error budgets per service.
- Auto-remediation actions can be classified by risk level (low / medium / high).
- Human-approval workflow exists for medium and high-risk actions (chatops, ticket, paging).

## Skip If (ANY kills it)

- Teams without an observability foundation (Prometheus + structured logs + traces) — collect data first.
- Organizations that have not defined SLOs — anomaly detection without SLOs produces meaningless alerts.
- Small services with predictable failure modes — static runbooks and on-call rotation are sufficient.
- When explainability / audit requirements are strict and ML model decisions cannot be logged with reasoning.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OpenTelemetry Collector config | YAML | platform |
| SLO definitions per service | YAML / doc | product + platform |
| Auto-remediation risk classification | table | platform + security |
| Human-approval channel | chatops / ticket / paging | team norms |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/prometheus-monitoring` | metric collection assumed |
| `pro/infra/devops-engineer/sli-slo-definition` | SLO definitions feed dynamic thresholds |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-anomaly-detector` | sonnet | Choose Isolation Forest / Prophet / LSTM per signal |
| `wire-rca-pipeline` | sonnet | Bind change events + topology + traces into RCA output |
| `risk-classify-actions` | opus | Map remediation actions to low/medium/high with approval policy |

## Templates

| File | Purpose |
|------|---------|
| `templates/aiops-policy.yaml` | Risk-tier + approval-matrix policy |
| `templates/auto-remediation-action.json` | Single auto-remediation action record |
| `templates/rca-output.json` | RCA structured output skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aiops.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[prometheus-monitoring]]
- [[alert-deduplication-playbook]]
- [[sli-slo-definition]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the AIOps: ML-Powered Incident Detection and Auto-Remediation methodology when in doubt about scope or fit.
