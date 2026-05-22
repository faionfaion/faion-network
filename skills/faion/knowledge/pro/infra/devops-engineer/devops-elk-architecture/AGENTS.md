---
slug: devops-elk-architecture
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The ELK Stack (Elasticsearch, Logstash, Kibana) and its variants (EFK with Fluentd, Elastic Stack with Beats) provide centralized log management, search, and visualization.
content_id: "3c387da992be521b"
tags: [elk, elasticsearch, logging, observability, devops]
---
# ELK Stack Architecture and Deployment

## Summary

**One-sentence:** The ELK Stack (Elasticsearch, Logstash, Kibana) and its variants (EFK with Fluentd, Elastic Stack with Beats) provide centralized log management, search, and visualization.

**One-paragraph:** The ELK Stack (Elasticsearch, Logstash, Kibana) and its variants (EFK with Fluentd, Elastic Stack with Beats) provide centralized log management, search, and visualization. Architect node roles, hot-warm-cold tiers, and deploy via Docker Compose or Elastic Cloud on Kubernetes (ECK) for production workloads.

## Applies If (ALL must hold)

- Centralizing logs from multiple applications and services into one searchable store.
- Building operational dashboards for troubleshooting across microservices.
- Implementing compliance logging (GDPR, HIPAA, SOC2) requiring long retention with audit trails.
- Setting up alerting based on log patterns or error rates.
- Security analytics (SIEM) requiring full-text search across log events.
- Business intelligence derived from structured application log data.

## Skip If (ANY kills it)

- Single small application with low log volume — Loki+Grafana or a managed service (Datadog, CloudWatch) has lower operational overhead.
- Cost-sensitive environments where Loki's label-based model provides sufficient query capability at a fraction of the storage cost.
- Purely metrics-only observability — Prometheus+Grafana covers this without the ELK operational burden.
- OpenSearch preference — use the AWS-native fork rather than Elastic when AWS-native integration and open licensing is a hard requirement.

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
