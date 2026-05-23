---
slug: dora-metrics
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a DORA metrics report (Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR + Reliability) with deploy-event ingestion, Prometheus rules, schema, and Grafana wiring.
content_id: "3d1db3c3785be582"
complexity: medium
produces: report
est_tokens: 4400
tags: ["dora", "metrics", "devops", "ci-cd", "observability"]
---
# DORA + Reliability Metrics Report

## Summary

**One-sentence:** Generates a DORA metrics report (Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR + Reliability) with deploy-event ingestion, Prometheus rules, schema, and Grafana wiring.

**One-paragraph:** DORA + Reliability Metrics Report — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a report that the downstream agent can verify with the included validator.

**Ефективно для:**

- Team wants to measure delivery performance objectively against the 2024+ DORA bands (Elite/High/Medium/Low).
- CI/CD pipeline + incident management produce machine-readable events (deploy timestamp, lead time, MTTR signal).
- Audience is engineering leadership or board-level KPIs.

## Applies If (ALL must hold)

- Team wants to measure delivery performance objectively against the 2024+ DORA bands (Elite/High/Medium/Low).
- CI/CD pipeline + incident management produce machine-readable events (deploy timestamp, lead time, MTTR signal).
- Audience is engineering leadership or board-level KPIs.

## Skip If (ANY kills it)

- Pre-product team with no production deploys.
- Single-developer side project where metrics overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[docker-optimization]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (ingest-deploy-event-cdevents, lead-time-from-commit-to-prod, deploy-frequency-rolling-7-day, change-failure-rate-from-incidents, mttr-includes-detection-time, reliability-as-fifth-metric, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the report + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-dora-metrics` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/deploy-event.yml` | CDEvents-style deploy event schema |
| `templates/prometheus-rules.yml` | Prometheus recording + alerting rules for DORA metrics |
| `templates/schema.sql` | SQL schema for deploys + incidents join |
| `templates/backup-config.example.json` | Filled report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dora-metrics.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[docker-optimization]]
- [[elk-stack-logging]]
- [[cicd-tls-validation-gate]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
