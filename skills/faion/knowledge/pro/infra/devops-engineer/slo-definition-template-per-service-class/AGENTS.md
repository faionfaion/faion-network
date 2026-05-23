---
slug: slo-definition-template-per-service-class
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "SLI/SLO definition templates keyed by service class (API, async worker, batch, static asset, scheduled job) with explicit SLI selection rules and error-budget calibration."
content_id: "8fbeda51b7d78b38"
complexity: medium
produces: spec
est_tokens: 4000
tags: [slo, sli, service-class, devops-engineer, observability, prometheus]
---

# SLO Definition Template Per Service Class

## Summary

**One-sentence:** SLI/SLO definition templates keyed by service class (API, async worker, batch, static asset, scheduled job) with explicit SLI selection rules and error-budget calibration.

**One-paragraph:** SLO authoring fails when teams reverse-engineer SLOs from existing dashboards instead of from service shape. The result: API SLOs measured by 'CPU < 80%' (not user-facing), worker SLOs missing entirely, batch SLOs treating success counts as latency. This methodology pins SLI templates per service class: API → availability + latency (RED), async worker → durability + processing-lag, batch → success-rate + completion-time, static asset → availability + freshness, scheduled job → schedule-adherence. Each template specifies the SLI query, the SLO target with rationale, and the error-budget window. Output: slo.yaml per service that ships into the alerting + matrix pipelines.

**Ефективно для:**

- SLO author не вигадує — pick template по service class.
- Уникнення CPU-based SLO для user-facing API (не вимірює customer pain).
- Узгодження SLI query format між teams (one PromQL per template).
- Calibration: target + rationale + window замість магічних 99.9%.

## Applies If (ALL must hold)

- Service catalog exists with service-shape metadata (HTTP API / async worker / batch / etc.)
- Metrics pipeline (Prometheus / Datadog / Honeycomb) measures the relevant SLIs
- Engineering org wants explicit SLOs (for paging, customer commitments, or error-budget policy)
- There is a feedback loop: SLO miss → alert → action

## Skip If (ANY kills it)

- Pre-product team — SLOs without customers are theatre; instrument first, SLO later
- Single-tenant internal tool with no SLA — overhead exceeds value
- Service-class taxonomy not yet defined — define classes first, then SLOs per class

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service catalog with service_class field | catalog YAML | platform team |
| Metrics pipeline + recording rules | Prometheus config | SRE |
| Error-budget policy | freeze-rules.yaml | engineering leader |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[prometheus-monitoring]] | PromQL + metric naming conventions |
| [[error-budget-policy-and-freeze-rules]] | How budgets become actions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | medium | Worked example end-to-end | ~500 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_service` | haiku | Pick one class from catalog metadata |
| `target_rationale` | sonnet | Bounded judgment on benchmark vs SLA |
| `template_fill` | haiku | Mechanical placeholder substitution |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-slo-definition-template-per-service-class.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[prometheus-monitoring]]
- [[error-budget-policy-and-freeze-rules]]
- [[slo-burn-decision-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
