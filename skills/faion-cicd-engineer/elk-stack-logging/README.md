# ELK Stack Logging

## Overview

The ELK Stack (Elasticsearch, Logstash, Kibana) with Beats is the industry-standard solution for centralized log management, search, and visualization. This methodology covers architecture design, deployment patterns, and operational best practices for production environments.

## Components

| Component | Role | Description |
|-----------|------|-------------|
| **Elasticsearch** | Storage & Search | Distributed search and analytics engine |
| **Logstash** | Processing | Data ingestion pipeline with parsing/transformation |
| **Kibana** | Visualization | Dashboards, charts, and interactive queries |
| **Beats** | Collection | Lightweight shippers (Filebeat, Metricbeat, etc.) |

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
- Security analytics (SIEM use cases)
- Real-time monitoring and observability

## Architecture

```
Applications/Servers/Containers
          │
          ▼
    ┌─────────────┐
    │   Beats     │  (Filebeat, Metricbeat)
    │ Lightweight │
    └─────┬───────┘
          │
          ▼
    ┌─────────────┐
    │  Logstash   │  (Optional: parsing, enrichment)
    │ Processing  │
    └─────┬───────┘
          │
          ▼
    ┌─────────────┐
    │Elasticsearch│  (Storage, indexing, search)
    │  Cluster    │
    └─────┬───────┘
          │
          ▼
    ┌─────────────┐
    │   Kibana    │  (Visualization, dashboards)
    │    UI       │
    └─────────────┘
```

## Best Practices (2025-2026)

### Cluster Design
- Separate node roles: master, data, ingest, coordinating
- Right-size shards: 20-40GB per shard optimal
- Replica planning: at least 1 replica for HA
- Hot-warm-cold architecture for cost-effective retention

### Index Management
- Use ILM policies for automated lifecycle management
- Time-based indices with daily or weekly rollover
- Index templates for consistent mappings
- Alias strategy to abstract index names

### Performance
- Bulk indexing with batched requests
- Increase refresh interval for write-heavy workloads
- Balance shard sizing between search and indexing
- Heap sizing: 50% of RAM, max 32GB

### Security
- Enable TLS for node-to-node and client communication
- Implement RBAC (Role-Based Access Control)
- Enable audit logging for compliance
- Network isolation with private cluster network

### Observability Integration
- Correlate metrics and logs for root cause analysis
- Combine with Prometheus/Grafana for full observability
- Use structured logging with consistent schemas
- Implement distributed tracing with trace_id/span_id

## Folder Contents

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Pre-deployment and operational checklists |
| [examples.md](examples.md) | Configuration examples and code samples |
| [templates.md](templates.md) | Ready-to-use templates for common scenarios |
| [llm-prompts.md](llm-prompts.md) | AI-assisted prompts for ELK tasks |

## Key Decisions

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Beats vs Logstash | Direct to ES vs via Logstash | Use Beats direct for simple cases; Logstash for complex parsing |
| Managed vs Self-hosted | Elastic Cloud vs DIY | Managed for reduced ops; self-hosted for full control |
| Data retention | Days vs months | Use ILM with hot-warm-cold tiers |
| Kubernetes | ECK vs Helm | ECK (Elastic Cloud on Kubernetes) preferred |

## References

- [Elastic Stack Documentation](https://www.elastic.co/guide/index.html)
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Logstash Reference](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Guide](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Filebeat Documentation](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
- [Elastic Cloud on Kubernetes](https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [Elk Stack: A Comprehensive Guide for 2025](https://www.shadecoder.com/topics/elk-stack-a-comprehensive-guide-for-2025)
- [The Complete Guide to the ELK Stack](https://logz.io/learn/complete-guide-elk-stack/)
- [Kubernetes Logging Best Practices with ELK Stack](https://logit.io/blog/post/kubernetes-logging-best-practices-elk-stack/)
- [What Is ELK Stack: Tutorial on How to Use It](https://sematext.com/guides/elk-stack/)
- [Real-time monitoring with ELK Stack](https://medium.com/@jeromedecinco/real-time-monitoring-with-elk-stack-solutions-and-best-practices-cc7b85ef0469)

---

*ELK Stack Logging Methodology | faion-cicd-engineer*
