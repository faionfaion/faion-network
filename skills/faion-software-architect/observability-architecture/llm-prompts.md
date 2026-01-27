# Observability Architecture LLM Prompts

Effective prompts for LLM-assisted observability design, implementation, and troubleshooting.

## Table of Contents

1. [Stack Selection](#stack-selection)
2. [SLO Design](#slo-design)
3. [Alerting](#alerting)
4. [Instrumentation](#instrumentation)
5. [Troubleshooting](#troubleshooting)
6. [Cost Optimization](#cost-optimization)
7. [Migration](#migration)

---

## Stack Selection

### Prompt: Compare Observability Stacks

```
I need help selecting an observability stack for my application.

**Context:**
- Architecture: [monolith/microservices/serverless]
- Scale: [services count, requests/sec, data volume/day]
- Cloud: [AWS/GCP/Azure/multi-cloud/on-prem]
- Team size: [number] engineers
- Budget: [specific amount or range per month]
- Existing tools: [list current monitoring/logging tools]

**Requirements:**
- Metrics: [specific needs]
- Logs: [retention, compliance requirements]
- Traces: [distributed tracing needs]
- Alerting: [on-call, PagerDuty integration, etc.]

**Constraints:**
- [vendor lock-in concerns]
- [compliance requirements: HIPAA, SOC2, GDPR]
- [team expertise level]

Please compare suitable options and recommend a stack with rationale.
```

### Prompt: LGTM vs Commercial Stack

```
Compare the Grafana LGTM stack (Loki, Grafana, Tempo, Mimir) against [Datadog/New Relic/Dynatrace] for our use case:

**Workload:**
- [X] microservices in Kubernetes
- [X] million metrics/day
- [X] GB logs/day
- [X] traces/day

**Team:**
- [X] engineers
- DevOps expertise: [beginner/intermediate/expert]
- Time for self-management: [hours/week]

**Priorities (rank 1-5):**
- Cost optimization: [1-5]
- Ease of use: [1-5]
- Customization: [1-5]
- Vendor independence: [1-5]
- Enterprise support: [1-5]

Provide TCO analysis for 1 year and 3 years.
```

### Prompt: Kubernetes Observability Architecture

```
Design a Kubernetes-native observability architecture for our cluster.

**Cluster Details:**
- Kubernetes version: [X.X]
- Node count: [X] nodes
- Namespaces: [X] (list critical ones)
- Service mesh: [Istio/Linkerd/none]
- Ingress: [nginx/traefik/AWS ALB]

**Requirements:**
1. Cluster-level metrics (nodes, pods, control plane)
2. Application metrics (RED method)
3. Centralized logging with [X] days retention
4. Distributed tracing for [list critical paths]
5. Alerting integrated with [PagerDuty/Opsgenie/Slack]

**Constraints:**
- Resource budget for observability: [X] vCPU, [X] GB memory
- Storage budget: [X] GB

Design the architecture with component placement and data flow.
```

---

## SLO Design

### Prompt: Define SLOs for a Service

```
Help me define SLOs for my service.

**Service:**
- Name: [service name]
- Type: [API/web app/background worker/data pipeline]
- Criticality: [tier 1/2/3]
- Users: [internal/external, count]
- Dependencies: [list upstream/downstream services]

**Current Performance:**
- Availability: [current %]
- Latency p50/p95/p99: [current values]
- Error rate: [current %]
- Traffic pattern: [steady/bursty/seasonal]

**Business Context:**
- What happens when service is down: [impact description]
- Acceptable degradation: [partial failure modes]
- Existing SLA commitments: [if any]

Define:
1. Primary SLIs (2-3 metrics)
2. SLO targets with rationale
3. Error budget calculations
4. Error budget policies
```

### Prompt: Multi-Window Multi-Burn-Rate Alerts

```
Create multi-window, multi-burn-rate SLO alerts for my service.

**SLO:**
- Metric: [availability/latency/throughput]
- Target: [X]%
- Window: [30 days]
- Error budget: [X]%

**Alert Requirements:**
- Page for critical issues (fast burn)
- Warn for concerning trends (slow burn)
- Minimize false positives
- Integration: [PagerDuty/Opsgenie/Slack]

Generate:
1. Prometheus alerting rules with proper burn rates
2. Explanation of each alert's purpose
3. Suggested `for` durations to avoid flapping
4. Alert annotations including runbook placeholders
```

### Prompt: Error Budget Tracking Dashboard

```
Design a Grafana dashboard for error budget tracking.

**SLOs:**
1. [Service A]: [X]% availability over 30 days
2. [Service B]: [X]% latency < [X]ms over 30 days
3. [Service C]: [X]% success rate over 30 days

**Dashboard Requirements:**
- Current error budget remaining (%)
- Error budget burn rate (current vs sustainable)
- Time until budget exhaustion at current rate
- Historical SLO compliance
- Deployment markers correlation

Provide:
1. Dashboard JSON or Terraform
2. PromQL queries for each panel
3. Recommended thresholds and colors
```

---

## Alerting

### Prompt: Design Alert Hierarchy

```
Design an alerting hierarchy for my observability system.

**Services:**
[List services with their criticality tiers]

**Teams:**
[List teams and their responsibilities]

**On-Call:**
- Primary: [rotation schedule]
- Escalation: [escalation policy]
- Hours: [24/7 or business hours]

**Channels:**
- Critical: [PagerDuty/phone]
- Warning: [Slack channel]
- Info: [email/dashboard]

Design:
1. Severity levels with response expectations
2. Routing rules (which alerts go where)
3. Grouping and deduplication strategy
4. Inhibition rules (suppress related alerts)
5. Escalation policies
```

### Prompt: Create Runbook for Alert

```
Create a runbook for the following alert.

**Alert:**
- Name: [alert name]
- Expression: [PromQL/LogQL query]
- Severity: [critical/warning]
- Service: [affected service]
- Typical trigger conditions: [describe when it fires]

**Context:**
- Service architecture: [brief description]
- Dependencies: [list]
- Common causes: [if known]
- Previous incidents: [if any]

Generate runbook with:
1. Alert summary and impact
2. Diagnostic steps (commands, queries)
3. Mitigation procedures (step-by-step)
4. Escalation contacts
5. Post-incident actions
6. Related dashboards and logs queries
```

### Prompt: Reduce Alert Fatigue

```
Help me reduce alert fatigue in my observability system.

**Current State:**
- Alerts/week: [X]
- False positive rate: [X]%
- Most frequent alerts: [list top 5]
- Current on-call burden: [description]

**Symptoms:**
- [Describe alert fatigue symptoms]

**Existing Rules:**
[Paste current alerting rules or describe them]

Analyze and provide:
1. Which alerts should be removed/consolidated
2. Threshold adjustments to reduce noise
3. Missing inhibition rules
4. Recording rules to improve alert quality
5. SLO-based alert recommendations
```

---

## Instrumentation

### Prompt: Instrument Application with OpenTelemetry

```
Help me instrument my application with OpenTelemetry.

**Application:**
- Language: [Python/Go/Java/Node.js/etc.]
- Framework: [FastAPI/Django/Gin/Spring/Express/etc.]
- Type: [API/worker/CLI]

**Dependencies:**
- Database: [PostgreSQL/MySQL/MongoDB/etc.]
- Cache: [Redis/Memcached]
- Message queue: [Kafka/RabbitMQ/SQS]
- HTTP clients: [requests/httpx/net/http]

**Requirements:**
- Auto-instrumentation where possible
- Custom spans for business operations: [list operations]
- Custom metrics: [list metrics needed]
- Structured logging with trace correlation
- Sampling strategy: [all/errors-only/percentage]

Provide:
1. Dependencies to install
2. Initialization code
3. Custom instrumentation examples
4. Configuration for OTEL Collector
5. Environment variables
```

### Prompt: Define Custom Metrics

```
Help me define custom metrics for my application.

**Business Domain:**
[Describe what the application does]

**Key Operations:**
1. [Operation A]: [description]
2. [Operation B]: [description]
3. [Operation C]: [description]

**Questions to Answer:**
- [List questions the metrics should answer]

**Existing Metrics:**
[List any existing metrics]

Design:
1. Metric names following conventions
2. Metric types (counter/gauge/histogram)
3. Labels/dimensions (with cardinality analysis)
4. PromQL queries for common use cases
5. Dashboard panel suggestions
```

### Prompt: Structured Logging Schema

```
Design a structured logging schema for my application.

**Application Type:** [web service/microservice/CLI]
**Log Aggregator:** [Loki/Elasticsearch/CloudWatch]

**Log Categories:**
1. HTTP requests/responses
2. Database operations
3. External API calls
4. Business events: [list]
5. Errors and exceptions

**Compliance Requirements:**
- PII handling: [mask/exclude/hash]
- Retention: [days]
- Audit requirements: [if any]

Design:
1. Base log schema (common fields)
2. Category-specific schemas
3. Log level guidelines
4. PII masking strategy
5. Example log entries
6. LogQL/ES queries for common searches
```

---

## Troubleshooting

### Prompt: Debug High Latency

```
Help me debug high latency in my service.

**Symptoms:**
- Service: [service name]
- Latency increase: from [X]ms to [Y]ms (p[percentile])
- Started: [when]
- Affected endpoints: [list or all]

**Environment:**
- Infrastructure: [K8s/EC2/Lambda]
- Dependencies: [database, cache, external APIs]
- Recent changes: [deployments, config changes]

**Available Data:**
- Metrics: [Prometheus/CloudWatch/etc.]
- Logs: [Loki/ES/CloudWatch]
- Traces: [Tempo/Jaeger/X-Ray]

Provide:
1. Diagnostic queries (PromQL, LogQL)
2. Trace analysis approach
3. Common causes checklist
4. Correlation analysis steps
5. Mitigation options
```

### Prompt: Investigate Memory Leak

```
Help me investigate a potential memory leak.

**Symptoms:**
- Service: [service name]
- Memory pattern: [steadily increasing/sudden spikes]
- OOM events: [yes/no, frequency]
- Restart behavior: [does restart help temporarily]

**Application:**
- Language: [runtime]
- Memory limit: [X] GB
- Normal memory usage: [X] GB

**Available Metrics:**
[List memory-related metrics available]

Provide:
1. Metrics to analyze (with queries)
2. Profiling approach
3. Common leak patterns for [language]
4. Diagnostic steps
5. Short-term mitigation
```

### Prompt: Trace Analysis for Distributed Issue

```
Help me analyze traces for a distributed system issue.

**Problem:**
[Describe the issue - errors, timeouts, inconsistencies]

**System:**
- Services involved: [list]
- Communication: [HTTP/gRPC/async]
- Data flow: [describe the flow]

**Observations:**
- Error type: [timeout/5xx/validation]
- Affected trace pattern: [describe]
- Frequency: [X]% of requests

**Tracing Backend:** [Tempo/Jaeger/Zipkin/X-Ray]

Provide:
1. Trace query strategy
2. Span attributes to examine
3. Service graph analysis approach
4. Root cause identification steps
5. Fix verification approach
```

---

## Cost Optimization

### Prompt: Reduce Observability Costs

```
Help me optimize observability costs.

**Current Costs:**
- Metrics: $[X]/month ([Y] active series)
- Logs: $[X]/month ([Y] GB/day)
- Traces: $[X]/month ([Y] traces/day)
- Total: $[X]/month

**Platform:** [Datadog/Grafana Cloud/self-hosted/etc.]

**Pain Points:**
- [High cardinality metrics]
- [Verbose logging]
- [Low-value data retention]

**Constraints:**
- Cannot reduce retention below [X] days
- Must keep [specific data] for compliance
- Cannot lose [specific capability]

Provide:
1. Quick wins (immediate savings)
2. Medium-term optimizations
3. Architectural changes for long-term savings
4. Sampling strategies
5. Data lifecycle policies
6. Estimated savings per recommendation
```

### Prompt: Cardinality Optimization

```
Help me reduce metric cardinality.

**Current State:**
- Total series: [X] million
- Top high-cardinality metrics: [list with series counts]
- Cardinality growth rate: [X]% per month

**Labels Causing Issues:**
[List labels with high cardinality]

**Retention:** [X] days

Provide:
1. Labels to remove or aggregate
2. Recording rules to pre-aggregate
3. Relabeling configurations
4. Cardinality monitoring queries
5. Alerting for cardinality growth
```

### Prompt: Sampling Strategy Design

```
Design a sampling strategy for my observability data.

**Data Volumes:**
- Traces: [X]/second
- Logs: [X] GB/day
- Metrics series: [X] million

**Requirements:**
- Must capture all errors
- Must capture slow requests (> [X]ms)
- Must sample [X]% of normal traffic
- Critical paths: [list] must have higher sampling

**Cost Target:** Reduce to [X]% of current cost

Design:
1. Head vs tail sampling decision
2. Sampling rules by criteria
3. Log filtering/aggregation rules
4. OTEL Collector configuration
5. Validation approach (ensure nothing critical is lost)
```

---

## Migration

### Prompt: Migrate to OpenTelemetry

```
Help me plan a migration to OpenTelemetry.

**Current Stack:**
- Metrics: [Prometheus client libraries/StatsD/etc.]
- Logs: [current logging setup]
- Traces: [Jaeger client/Zipkin/none]

**Applications:**
- Languages: [list languages]
- Frameworks: [list frameworks]
- Services count: [X]

**Target State:**
- Collection: OpenTelemetry Collector
- Backends: [Prometheus/Mimir, Loki, Tempo/Jaeger]

**Constraints:**
- Zero downtime requirement
- Team bandwidth: [X] engineer-weeks
- Timeline: [X] months

Create:
1. Migration phases
2. Per-service migration checklist
3. Dual-write period strategy
4. Validation tests
5. Rollback plan
6. Risk mitigation
```

### Prompt: Migrate from Datadog/New Relic

```
Help me migrate from [Datadog/New Relic] to open-source observability.

**Current Usage:**
- APM: [features used]
- Infrastructure monitoring: [features used]
- Logs: [features used]
- Custom dashboards: [count]
- Alerts: [count]
- Integrations: [list]

**Current Cost:** $[X]/month

**Target Stack:**
[Describe target: LGTM, self-hosted, etc.]

**Requirements:**
- Feature parity for: [list critical features]
- Nice to have: [list]
- Can drop: [list]

Create:
1. Feature mapping (current to target)
2. Migration phases
3. Dashboard recreation approach
4. Alert migration
5. Integration alternatives
6. Timeline and resource estimate
7. Risk assessment
```

### Prompt: Kubernetes Observability Migration

```
Help me migrate Kubernetes observability to a new stack.

**Current:**
- Metrics: [Prometheus Operator/kube-prometheus-stack/custom]
- Logs: [EFK/Fluentd/current setup]
- Version: [current versions]

**Target:**
- Metrics: [target solution]
- Logs: [target solution]
- Traces: [target solution]

**Cluster:**
- Size: [nodes, pods]
- Critical workloads: [list]
- Change windows: [when maintenance allowed]

Create:
1. Pre-migration checklist
2. Parallel deployment strategy
3. Traffic migration steps
4. Validation queries
5. Cleanup steps
6. Rollback triggers and process
```

---

## Prompt Engineering Tips

### Best Practices for Observability Prompts

1. **Provide Context**: Include current stack, scale, constraints
2. **Be Specific**: Exact numbers, service names, metrics
3. **State Goals**: What you want to achieve
4. **Mention Constraints**: Budget, compliance, team skills
5. **Request Formats**: Ask for specific outputs (YAML, JSON, queries)

### Example Context Block

```
**Environment:**
- Cloud: AWS (us-east-1, eu-west-1)
- Kubernetes: EKS 1.28, 50 nodes
- Services: 120 microservices
- Traffic: 10K RPS peak
- Data: 500GB logs/day, 1M active metric series, 100K traces/day

**Stack:**
- Metrics: Prometheus + Thanos
- Logs: Loki 2.9
- Traces: Tempo 2.3
- Visualization: Grafana 10.2
- Alerting: Alertmanager + PagerDuty

**Team:**
- 4 SREs, 20 developers
- On-call rotation: weekly
- Observability expertise: intermediate
```

### Iterative Refinement

```
[After initial response]

This is helpful. Can you also:
1. Add [specific detail]
2. Provide alternative for [constraint]
3. Include [specific format/output]
4. Explain trade-offs for [decision point]
```

---

## Quick Reference Prompts

### One-Liners

```
# Quick PromQL help
"Write PromQL for [metric description] with [aggregation/filtering needs]"

# Alert design
"Create Prometheus alert for [condition] with severity [level] and runbook placeholder"

# Dashboard panel
"Create Grafana panel JSON for [visualization] showing [metric] by [dimensions]"

# OTEL config
"Configure OTEL Collector to [receive/process/export] [data type] to [backend]"

# Log query
"Write LogQL query to find [condition] in [service] logs"

# Cost estimate
"Estimate observability costs for [X] services with [Y] traffic at [Z] retention"
```
