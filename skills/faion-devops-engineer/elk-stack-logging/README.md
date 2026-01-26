# ELK Stack Logging

## Overview

The ELK Stack (Elasticsearch, Logstash, Kibana) is a powerful logging and observability solution for centralized log management, search, and visualization. This methodology covers architecture design, deployment patterns, and operational best practices for production environments.

## Components

| Component | Role | Version (2025) |
|-----------|------|----------------|
| Elasticsearch | Storage & search engine | 8.x |
| Logstash | Data processing pipeline | 8.x |
| Kibana | Visualization & dashboards | 8.x |
| Beats | Lightweight data shippers | 8.x |

## Stack Variants

| Stack | Components | Use Case |
|-------|------------|----------|
| ELK | Elasticsearch, Logstash, Kibana | Traditional, heavy processing |
| EFK | Elasticsearch, Fluentd, Kibana | Kubernetes-native |
| Elastic Stack | Elasticsearch, Beats, Kibana | Lightweight collection |

## When to Use

- Centralizing logs from multiple applications/services
- Building searchable log archives
- Creating operational dashboards for troubleshooting
- Implementing compliance logging requirements
- Setting up alerting based on log patterns
- Security analytics (SIEM)
- Business intelligence from log data

## Architecture

```
Applications → Beats/Fluentd → Logstash → Elasticsearch → Kibana
                    ↓              ↓            ↓
              (Collection)   (Processing)  (Storage)    (Viz)
```

**Data Flow:**
1. **Collection**: Beats (Filebeat, Metricbeat) or Fluentd collect logs
2. **Processing**: Logstash parses, enriches, transforms data
3. **Storage**: Elasticsearch indexes and stores data
4. **Visualization**: Kibana provides dashboards and queries

## Key Concepts

### Index Management

| Concept | Description |
|---------|-------------|
| Index Template | Pre-defined settings and mappings for indices |
| ILM (Index Lifecycle Management) | Automated index lifecycle (hot/warm/cold/delete) |
| Rollover | Create new index when size/age threshold reached |
| Alias | Abstract index name for seamless rollover |

### Node Roles

| Role | Purpose |
|------|---------|
| Master | Cluster state management |
| Data | Store and search data |
| Ingest | Pre-process documents |
| Coordinating | Route requests, reduce results |
| ML | Machine learning jobs |

### Shard Strategy

| Guideline | Recommendation |
|-----------|----------------|
| Shard size | 20-40 GB optimal |
| Shards per node | Max 20 shards per GB heap |
| Replicas | At least 1 for HA |

## Best Practices (2025-2026)

### Architecture

1. **Separate node roles** - Master, data, ingest, coordinating
2. **Hot-warm-cold architecture** - Cost-effective retention
3. **Right-size shards** - 20-40GB per shard optimal
4. **Plan capacity** - Monitor and scale proactively

### Index Management

1. **Use ILM policies** - Automate index lifecycle
2. **Time-based indices** - Daily or weekly rollover
3. **Index templates** - Consistent mappings
4. **Alias strategy** - Abstract index names

### Performance

1. **Bulk indexing** - Batch requests (500-5000 docs)
2. **Refresh interval** - Increase to 30s for write-heavy workloads
3. **Heap sizing** - 50% of RAM, max 32GB
4. **Disable replicas during initial load** - Re-enable after

### Security

1. **Enable TLS** - Node-to-node and client
2. **RBAC** - Role-based access control
3. **Audit logging** - Track access and changes
4. **Network isolation** - Private network for cluster

### Kubernetes Logging

1. **Use Fluent Bit or Filebeat DaemonSet** - Node-level collection
2. **Structured logging** - JSON format from applications
3. **Autodiscover** - Dynamic pod discovery
4. **Resource limits** - Prevent collector from starving nodes

## Alternatives to Consider

| Alternative | When to Consider |
|-------------|------------------|
| Loki + Grafana | Cost-sensitive, Grafana ecosystem |
| OpenSearch | Open-source fork, AWS-native |
| Datadog Logs | Managed, unified observability |
| Splunk | Enterprise, compliance-heavy |

## Files in This Methodology

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation and operational checklists |
| [examples.md](examples.md) | Configuration and query examples |
| [templates.md](templates.md) | Ready-to-use configuration templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for ELK-related tasks |

## Related Methodologies

- [Prometheus Monitoring](../prometheus-monitoring/README.md)
- [Grafana Dashboards](../grafana-dashboards/README.md)
- [Kubernetes Observability](../kubernetes-observability/README.md)

## References

- [Elastic Stack Documentation](https://www.elastic.co/guide/index.html)
- [Elasticsearch Reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash Reference](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Guide](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Filebeat Documentation](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
- [Elastic Cloud on Kubernetes](https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html)

## Sources

- [Elk Stack: A Comprehensive Guide for 2025 - Shadecoder](https://www.shadecoder.com/topics/elk-stack-a-comprehensive-guide-for-2025)
- [The Complete Guide to the ELK Stack - Logz.io](https://logz.io/learn/complete-guide-elk-stack/)
- [Monitoring & Logging with Prometheus, Grafana, ELK, and Loki - Refonte Learning](https://www.refontelearning.com/blog/monitoring-logging-prometheus-grafana-elk-stack-loki)
- [Kubernetes Logging Best Practices with ELK Stack - Logit.io](https://logit.io/blog/post/kubernetes-logging-best-practices-elk-stack/)
- [What Is ELK Stack - Sematext](https://sematext.com/guides/elk-stack/)
- [Real-time monitoring with ELK Stack - Medium](https://medium.com/@jeromedecinco/real-time-monitoring-with-elk-stack-solutions-and-best-practices-cc7b85ef0469)
