---
slug: devops-elk-logstash-pipeline
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Logstash processes log streams through input → filter → output pipelines.
content_id: "767f1079999dc715"
tags: [logstash, elk, pipeline, logging, devops]
---
# Logstash Pipeline Configuration and Tuning

## Summary

**One-sentence:** Logstash processes log streams through input → filter → output pipelines.

**One-paragraph:** Logstash processes log streams through input → filter → output pipelines. Filters parse raw text into structured fields (grok, json, date, geoip, useragent), mask sensitive data (mutate gsub), and normalize field names. Multi-pipeline configurations isolate heavy processing from lightweight routing. Dead letter queues capture failed events for later replay.

## Applies If (ALL must hold)

- Log sources produce multiple formats requiring different parsing rules (nginx access logs, application JSON logs, syslog, custom formats).
- PII masking, field normalization, or GeoIP enrichment is required before indexing.
- Heavy processing (grok pattern matching, useragent parsing) needs to be isolated from the write path.
- Multiple log streams need routing to different Elasticsearch indices with different retention policies.
- A dead letter queue is needed to capture and replay events that fail parsing.

## Skip If (ANY kills it)

- Simple JSON logs from a single application — Filebeat with JSON parsing and direct Elasticsearch output avoids the Logstash overhead entirely.
- Kubernetes-native deployments where Fluentd or Fluent Bit provide sufficient routing and transformation with lower memory footprint.
- Throughput requirements exceed what a single Logstash node can handle and horizontal scaling is constrained — consider Kafka as a buffer upstream.

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
