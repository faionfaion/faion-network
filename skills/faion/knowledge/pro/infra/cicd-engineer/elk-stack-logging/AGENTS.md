---
slug: elk-stack-logging
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The ELK Stack (Elasticsearch, Logstash, Kibana) with Beats is the industry-standard solution for centralized log management, search, and visualization.
content_id: "bd221f94e8f46524"
tags: [elasticsearch, logstash, kibana, logging, observability]
---
# ELK Stack Logging

## Summary

**One-sentence:** The ELK Stack (Elasticsearch, Logstash, Kibana) with Beats is the industry-standard solution for centralized log management, search, and visualization.

**One-paragraph:** The ELK Stack (Elasticsearch, Logstash, Kibana) with Beats is the industry-standard solution for centralized log management, search, and visualization. This methodology covers architecture design, deployment patterns, and operational best practices for production environments.

## Applies If (ALL must hold)

- Centralizing logs from multiple applications/services
- Building searchable log archives
- Creating operational dashboards for troubleshooting
- Implementing compliance logging requirements
- Setting up alerting based on log patterns
- Security analytics (SIEM use cases)
- Real-time monitoring and observability
- Centralizing logs from a heterogeneous fleet (apps, hosts, containers, network gear) into a searchable store with dashboards
- Building compliance / audit log archives with retention tiers (hot-warm-cold or frozen)
- Setting up SIEM-lite use cases — alerting on log patterns, correlating security signals
- Kubernetes log aggregation with Filebeat or Fluent Bit → Logstash/Elastic
- Replacing brittle grep-on-prod workflows for SREs

## Skip If (ANY kills it)

- Pure metrics workloads — use Prometheus/Mimir/Datadog metrics, not Elasticsearch
- Distributed tracing — use Tempo/Jaeger; Elastic APM is fine but a different methodology
- Tiny single-node apps — journalctl + lnav or Loki is cheaper
- Cost-sensitive cloud-native shops — Loki + Grafana is dramatically cheaper at petabyte scale
- Hard-real-time queries (sub-100ms log lookup) — Elasticsearch refresh interval and shard cost make this expensive

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

- parent skill: `pro/infra/cicd-engineer/`
