---
slug: aws-monitoring-observability
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Production observability spec: CloudWatch metrics + logs + alarms + Container Insights + X-Ray tracing + OpenTelemetry collector, with SLO-derived alarms (burn-rate multi-window), structured logs, and dashboards per service."
content_id: "13f984b9687b7e25"
complexity: deep
produces: spec
est_tokens: 5000
tags: [aws, cloudwatch, x-ray, observability, slo, infra]
---
# AWS Monitoring + Observability

## Summary

**One-sentence:** Production observability spec: CloudWatch metrics + logs + alarms + Container Insights + X-Ray tracing + OpenTelemetry collector, with SLO-derived alarms (burn-rate multi-window), structured logs, and dashboards per service.

**One-paragraph:** Production observability spec: CloudWatch metrics + logs + alarms + Container Insights + X-Ray tracing + OpenTelemetry collector, with SLO-derived alarms (burn-rate multi-window), structured logs, and dashboards per service. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Production AWS workload exists with paying users or internal SLAs.
- Service has defined or definable SLOs.
- Named platform-lead can sign off on observability pattern.

## Skip If (ANY kills it)

- Prototype / pre-revenue with < 100 users — defaults are fine.
- Team already runs full OpenTelemetry + SLO discipline — audit don't redesign.
- Observability is fully outsourced to a SaaS vendor with no AWS hooks needed.

**Ефективно для:**

- Команди з production AWS workloads без unified observability.
- SLO-driven alerting на основі burn-rate (multi-window).
- Migration з CloudWatch-only до OpenTelemetry / Prometheus.
- Audit-ready dashboards per service з SLI / SLO визначеннями.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-monitoring-observability.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
