# Observability Architecture

Comprehensive guide to designing and implementing observability systems using the three pillars: logs, metrics, and traces.

## Overview

Observability is the ability to understand the internal state of a system by examining its outputs. Unlike monitoring (which tells you when something is wrong), observability helps you understand why.

| Aspect | Monitoring | Observability |
|--------|-----------|---------------|
| Focus | Known unknowns | Unknown unknowns |
| Approach | Predefined dashboards | Ad-hoc exploration |
| Questions | "Is service X down?" | "Why is latency increasing for users in region Y?" |
| Data | Metrics, logs | Metrics, logs, traces (correlated) |

## Three Pillars of Observability

| Pillar | Purpose | Question Answered | Tools |
|--------|---------|-------------------|-------|
| **Metrics** | Aggregate numerical data | What happened? | Prometheus, Mimir, InfluxDB |
| **Logs** | Event details with context | Why did it happen? | Loki, Elasticsearch, Splunk |
| **Traces** | Request flow across services | Where did it happen? | Tempo, Jaeger, Zipkin |

### Metrics

Numerical measurements collected over time intervals.

**Types:**
| Type | Use Case | Example |
|------|----------|---------|
| Counter | Cumulative totals | Total HTTP requests |
| Gauge | Current value | Active connections |
| Histogram | Value distribution | Request latency buckets |
| Summary | Pre-calculated quantiles | p95 latency |

**Key Methodologies:**

**RED Method** (for services):
- **R**ate: Requests per second
- **E**rrors: Failed requests per second
- **D**uration: Response time distribution

**USE Method** (for resources):
- **U**tilization: % time resource is busy
- **S**aturation: Queue depth / backlog
- **E**rrors: Error count

**Golden Signals** (Google SRE):
- Latency: Response time
- Traffic: Request rate
- Errors: Error rate
- Saturation: Resource utilization

### Logs

Discrete events with timestamps and context.

**Structured Logging Best Practices:**
```json
{
  "timestamp": "2025-01-15T10:30:00.000Z",
  "level": "INFO",
  "service": "order-service",
  "trace_id": "abc123def456",
  "span_id": "span-001",
  "user_id": "user-789",
  "action": "order_created",
  "order_id": "order-456",
  "amount": 99.99,
  "currency": "USD",
  "message": "Order created successfully"
}
```

**Log Levels:**
| Level | Use | Alert? |
|-------|-----|--------|
| ERROR | Failures requiring attention | Yes |
| WARN | Potential issues, degraded state | Maybe |
| INFO | Normal business operations | No |
| DEBUG | Detailed debugging info | No |

### Traces

End-to-end request paths through distributed systems.

**Trace Structure:**
```
Trace (unique ID: abc123)
|
+-- Span A (API Gateway) [0-150ms]
|   +-- Span B (Auth Service) [10-30ms]
|   +-- Span C (User Service) [40-100ms]
|       +-- Span D (Database) [50-90ms]
|
+-- Span E (Order Service) [160-350ms]
    +-- Span F (Inventory Check) [170-220ms]
    +-- Span G (Payment) [230-340ms]
```

**Context Propagation:**
- W3C Trace Context (standard)
- B3 (Zipkin format)
- Jaeger format

## Modern Observability Stack (2025)

### LGTM Stack (Grafana Labs)

| Component | Purpose | Storage |
|-----------|---------|---------|
| **L**oki | Log aggregation | Object storage (S3/GCS) |
| **G**rafana | Visualization | - |
| **T**empo | Distributed tracing | Object storage |
| **M**imir | Metrics (Prometheus compatible) | Object storage |

### OpenTelemetry (OTEL)

OpenTelemetry is the CNCF standard for observability instrumentation.

**Benefits:**
- Vendor-neutral instrumentation
- Single SDK for metrics, logs, traces
- Auto-instrumentation for many languages
- Prevents vendor lock-in

**Architecture:**
```
Applications          Collection           Storage            Visualization
+-----------+        +----------+        +---------+        +---------+
| App + SDK |------->| OTel     |------->| Metrics |------->|         |
|           |        | Collector|        | (Mimir) |        |         |
| Auto-     |------->|          |------->| Logs    |------->| Grafana |
| instrument|        | (Gateway)|        | (Loki)  |        |         |
|           |------->|          |------->| Traces  |------->|         |
+-----------+        +----------+        | (Tempo) |        +---------+
                                         +---------+
```

**Key Stats (2025):**
- 76% of companies use open source for observability
- 71% use both Prometheus and OpenTelemetry
- 57% of organizations reduced costs with OpenTelemetry

## SLOs, SLIs, and Error Budgets

### Definitions

| Term | Definition | Example |
|------|------------|---------|
| **SLI** (Service Level Indicator) | Quantitative measure of service behavior | 99.2% of requests < 200ms |
| **SLO** (Service Level Objective) | Target value for an SLI | 99.9% of requests < 200ms |
| **SLA** (Service Level Agreement) | Contract with consequences | 99.5% uptime or credits |
| **Error Budget** | Allowable unreliability (100% - SLO) | 0.1% = 43 min/month |

### SLI Calculation

```
SLI = (Good Events) / (Total Events) * 100%

Example:
Good requests: 999,000
Total requests: 1,000,000
SLI = 999,000 / 1,000,000 = 99.9%
```

### Error Budget Examples

| SLO | Error Budget | Downtime/Month | Downtime/Year |
|-----|--------------|----------------|---------------|
| 99% | 1% | 7.3 hours | 3.65 days |
| 99.9% | 0.1% | 43 minutes | 8.76 hours |
| 99.95% | 0.05% | 21.6 minutes | 4.38 hours |
| 99.99% | 0.01% | 4.3 minutes | 52.6 minutes |

### Error Budget Policy

When error budget is exhausted:
1. Freeze feature deployments
2. Focus engineering on reliability
3. Conduct incident reviews
4. Implement fixes before resuming features

## Cost Optimization

### Strategies

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| Tail-based sampling | 70-90% trace reduction | May miss rare issues |
| Log aggregation | 30-50% storage | Less granularity |
| Metric cardinality limits | 40-60% series reduction | Less detail |
| Tiered retention | 50-70% storage | Slower historical queries |
| Adaptive telemetry (AI) | 30-60% overall | Complexity |

### Sampling Strategies

**Head Sampling:**
- Decision at trace start
- Consistent sampling rate
- May miss errors

**Tail Sampling:**
- Decision after trace complete
- Sample based on characteristics (errors, latency)
- Higher memory usage

**Recommended Approach:**
```
- Baseline: 1-5% of all traces
- 100% of traces with errors
- 100% of traces > latency threshold
- 100% of traces for critical paths
```

### Data Retention Tiers

| Tier | Retention | Use Case |
|------|-----------|----------|
| Hot | 7-14 days | Active debugging |
| Warm | 30-90 days | Recent incident analysis |
| Cold | 1-2 years | Compliance, audits |
| Archive | 3+ years | Legal requirements |

## LLM Usage Tips

### When to Use This Methodology

- Designing new observability infrastructure
- Migrating to OpenTelemetry
- Implementing SLO-based alerting
- Optimizing observability costs
- Debugging distributed systems

### Effective LLM Prompts

1. **Stack Selection:** "Compare LGTM stack vs ELK stack for [workload type] with [scale]"
2. **SLO Definition:** "Help me define SLOs for [service] serving [user type]"
3. **Alert Design:** "Create Prometheus alerting rules for [use case] with runbook"
4. **Cost Analysis:** "Analyze observability costs for [metrics/day, logs/day, traces/day]"

### Context to Provide

- Current stack and scale
- Team size and expertise
- Budget constraints
- Compliance requirements
- Cloud provider(s)

## External Resources

### Official Documentation

- [OpenTelemetry Docs](https://opentelemetry.io/docs/)
- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
- [Loki Docs](https://grafana.com/docs/loki/)
- [Tempo Docs](https://grafana.com/docs/tempo/)
- [Jaeger Docs](https://www.jaegertracing.io/docs/)

### Best Practice Guides

- [Google SRE Workbook - Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [OpenTelemetry Best Practices](https://opentelemetry.io/docs/security/config-best-practices/)
- [Prometheus Operator Runbooks](https://runbooks.prometheus-operator.dev/)
- [Grafana LGTM Stack](https://grafana.com/oss/)

### Community Resources

- [CNCF Observability TAG](https://github.com/cncf/tag-observability)
- [OpenTelemetry Community](https://opentelemetry.io/community/)
- [Prometheus Community](https://prometheus.io/community/)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [reliability-architecture](../reliability-architecture/) | SLOs, fault tolerance |
| [microservices-architecture](../microservices-architecture/) | Distributed systems |
| [security-architecture](../security-architecture/) | Security monitoring |
| [caching-architecture](../caching-architecture/) | Cache metrics |

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step observability design checklist |
| [examples.md](examples.md) | Real-world observability stack examples |
| [templates.md](templates.md) | Copy-paste configurations |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted design |
