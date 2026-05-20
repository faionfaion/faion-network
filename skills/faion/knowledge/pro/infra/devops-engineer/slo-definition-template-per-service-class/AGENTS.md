---
slug: slo-definition-template-per-service-class
tier: pro
group: devops-engineer
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "f1dd1f4a398e61a6"
summary: SLI/SLO definition templates keyed by service class (API, async worker, batch, static asset, scheduled job) so SLO authoring stops being dashboard-driven and starts being service-shape-driven, with explicit SLI selection rules and budget calibration.
tags: [slo, sli, service-class, devops-engineer, observability, prometheus]
---

# SLO Definition Template Per Service Class

## Summary

**One-sentence:** SLI / SLO templates keyed by service class — API, async worker, batch job, static asset, scheduled job — so SLO authoring is driven by service shape, not by what the dashboard already shows.

**One-paragraph:** Most teams already have Prometheus + DORA metrics but no methodology for translating a service's shape into its SLI selection. The result is dashboard-driven SLO authoring: pick metrics that look good on Grafana, set the threshold to where the line happens to be, call it an SLO. This methodology pins per-class SLI selection rules: a user-facing API gets request-success + latency SLIs, an async worker gets queue-age + processing-success SLIs, a batch job gets completion-on-time + correctness SLIs, a static asset gets freshness + delivery-success SLIs, a scheduled job gets execution-success + on-time SLIs. Each class has a window (rolling 30 days standard), a target derived from user-acceptable error (not from current performance), and a budget-policy doc. Mechanism: identify service class → pick template → calibrate target with product → publish. Primary output: a `slo-defs.yaml` per service + a one-page rationale per SLO.

## Applies If (ALL must hold)

- service catalog with at least 3 services AND a service-class taxonomy in place
- observability stack capable of computing the chosen SLIs (Prometheus + Grafana or equivalent)
- product / business owner available to set user-acceptable thresholds
- team accepts SLOs as ship gates, not just dashboards

## Skip If (ANY kills it)

- single-service shop — adapt the template directly rather than build a class system
- no observability for the chosen SLIs — instrument first
- product refuses to set acceptable-error targets — SLO becomes engineering wishful thinking
- team uses platform SLOs (e.g. inherited from cloud provider) without authority to adjust — use the inherited targets

## Prerequisites

- service catalog with class labels
- Prometheus or equivalent that can compute success rate and latency percentile
- DORA metrics in place (`pro/infra/devops-engineer/dora-metrics`)
- one-page SLO rationale template

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/dora-metrics` | Vocabulary and tooling overlap |
| `pro/infra/devops-engineer/prometheus-monitoring` | Underlying metric source |
| `pro/infra/devops-engineer/slo-burn-decision-matrix` | What the SLOs feed into |
| `geek/dev/software-developer/slo-burn-rate-review-protocol` | Weekly review consumer |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: service-class first, SLI from class template, product-set target, budget-policy doc, 30-day window default | ~1100 |
| `content/02-output-contract.xml` | essential | slo-defs.yaml schema per class, rationale template, SLI / SLO / SLA distinction | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: dashboard-driven SLOs, missing budget policy, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `service_class_assignment` | sonnet | Classify a service from its shape (endpoints, traffic pattern, dependencies) |
| `sli_template_application` | haiku | Apply class-specific template |
| `target_calibration_interview` | sonnet | Draft questions for product to set acceptable error |
| `rationale_doc_drafter` | sonnet | Produce the one-page rationale |

## Templates

| File | Purpose |
|------|---------|
| `templates/slo-defs.schema.yaml` | Schema for slo-defs.yaml |
| `templates/sli-api.yaml` | API class SLIs |
| `templates/sli-async-worker.yaml` | Worker class SLIs |
| `templates/sli-batch.yaml` | Batch class SLIs |
| `templates/sli-static.yaml` | Static asset class SLIs |
| `templates/sli-scheduled.yaml` | Scheduled job SLIs |
| `templates/rationale-one-pager.md` | Rationale doc shape |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/scaffold-slo.py` | Given service + class, produce slo-defs.yaml from template | Service onboarding |
| `scripts/lint-slo-defs.py` | Validate slo-defs.yaml against schema | Pre-commit |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodologies: `dora-metrics`, `prometheus-monitoring`, `slo-burn-decision-matrix`, `slo-burn-rate-review-protocol`
- external: [Google SRE Workbook — SLO chapter](https://sre.google/workbook/implementing-slos/) · [Honeycomb on SLO design](https://www.honeycomb.io/) · [Nobl9 SLO guide](https://www.nobl9.com/resources)
