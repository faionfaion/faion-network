---
slug: devops-elk-beats-collection
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Filebeat is a lightweight log shipper deployed as an agent on each host or as a Kubernetes DaemonSet.
content_id: "a15dd343418d387d"
tags: [filebeat, beats, elk, kubernetes, logging]
---
# Log Collection with Filebeat and Elastic Beats

## Summary

**One-sentence:** Filebeat is a lightweight log shipper deployed as an agent on each host or as a Kubernetes DaemonSet.

**One-paragraph:** Filebeat is a lightweight log shipper deployed as an agent on each host or as a Kubernetes DaemonSet. It reads log files, handles multiline events (Java stack traces, Python tracebacks), parses JSON, enriches with host/cloud/Kubernetes metadata, and ships to Elasticsearch or Logstash. Autodiscover providers dynamically configure inputs as containers start and stop.

## Applies If (ALL must hold)

- Collecting logs from files on Linux/Windows hosts where application code cannot be modified to ship directly.
- Kubernetes environments where all container stdout/stderr must be centralized without modifying application deployments.
- Lightweight collection without the Logstash JVM overhead — Filebeat ships pre-parsed JSON directly to Elasticsearch.
- Dynamic environments where new services are deployed frequently and Autodiscover handles configuration automatically.

## Skip If (ANY kills it)

- Complex parsing that requires grok, translate, or conditional routing — Logstash or Fluentd are more capable processors.
- Kubernetes clusters where Fluentd is already installed and maintained — adding Filebeat creates duplicate collection overhead.
- Very high event rates (above 100k events/second per node) where Filebeat's single-goroutine harvester per file becomes a bottleneck — Fluent Bit has lower per-event overhead.

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
