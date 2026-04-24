# Observability Architecture Checklist

Step-by-step checklist for designing and implementing a comprehensive observability system.

## Phase 1: Requirements Gathering

### 1.1 Business Requirements

- [ ] Identify critical user journeys
- [ ] Define acceptable latency thresholds
- [ ] Determine uptime requirements (99.9%, 99.99%, etc.)
- [ ] Document compliance requirements (GDPR, HIPAA, SOC2)
- [ ] Establish data retention policies
- [ ] Define budget constraints

### 1.2 Technical Requirements

- [ ] Inventory all services and dependencies
- [ ] Map service communication patterns
- [ ] Identify data volume estimates (metrics/sec, logs/day, traces/day)
- [ ] Document existing monitoring tools
- [ ] Assess team observability expertise
- [ ] Determine multi-cloud/hybrid requirements

### 1.3 Stakeholder Alignment

- [ ] Define on-call rotation structure
- [ ] Establish escalation policies
- [ ] Identify dashboard consumers (dev, ops, business)
- [ ] Document runbook ownership
- [ ] Set alert notification channels

## Phase 2: SLO Definition

### 2.1 SLI Selection

- [ ] Identify 2-3 key SLIs per critical service
- [ ] Choose SLIs that reflect user experience
- [ ] Ensure SLIs are measurable and actionable

**Common SLIs:**
| Category | SLI | Measurement |
|----------|-----|-------------|
| Availability | Success rate | Successful requests / Total requests |
| Latency | Response time | Requests < threshold / Total requests |
| Throughput | Request rate | Requests per second |
| Error rate | Failure percentage | Failed requests / Total requests |
| Saturation | Resource utilization | Current usage / Capacity |

### 2.2 SLO Targets

- [ ] Set SLO slightly stricter than SLA
- [ ] Use rolling windows (28-30 days recommended)
- [ ] Document SLO rationale and approvers
- [ ] Schedule quarterly SLO reviews

**SLO Template:**
```
Service: [service-name]
SLI: [measurement description]
SLO: [target]% over [window]
Error Budget: [100 - SLO]%
Owner: [team/person]
Review Date: [date]
```

### 2.3 Error Budget Policies

- [ ] Define error budget thresholds (50%, 75%, 100%)
- [ ] Document actions at each threshold
- [ ] Establish feature freeze criteria
- [ ] Create reliability sprint triggers

**Error Budget Actions:**
| Budget Consumed | Action |
|-----------------|--------|
| < 50% | Normal development |
| 50-75% | Prioritize reliability tickets |
| 75-100% | Reliability-focused sprint |
| 100%+ | Feature freeze, reliability-only work |

## Phase 3: Metrics Implementation

### 3.1 Infrastructure Metrics

- [ ] CPU utilization (per pod/container/host)
- [ ] Memory usage and limits
- [ ] Disk I/O and capacity
- [ ] Network throughput and errors
- [ ] Container restart counts
- [ ] Node availability

### 3.2 Application Metrics (RED)

- [ ] Request rate (total, by endpoint, by status)
- [ ] Error rate (4xx, 5xx, by type)
- [ ] Duration/latency (p50, p90, p95, p99)
- [ ] In-flight requests
- [ ] Queue depths

### 3.3 Resource Metrics (USE)

- [ ] Database connection pool utilization
- [ ] Cache hit/miss ratios
- [ ] Message queue saturation
- [ ] Thread pool utilization
- [ ] File descriptor usage

### 3.4 Business Metrics

- [ ] Orders processed per minute
- [ ] User signups/logins
- [ ] Payment success rate
- [ ] Feature usage counts
- [ ] Revenue-impacting metrics

### 3.5 Metric Best Practices

- [ ] Use consistent naming conventions
- [ ] Limit cardinality (< 10 label values per dimension)
- [ ] Add unit suffixes (_seconds, _bytes, _total)
- [ ] Include help text in metric definitions
- [ ] Set appropriate scrape intervals (15-30s typical)

## Phase 4: Logging Implementation

### 4.1 Log Structure

- [ ] Use structured logging (JSON)
- [ ] Include timestamp in ISO 8601 format
- [ ] Add service name and version
- [ ] Include trace_id and span_id
- [ ] Add correlation IDs for request tracking
- [ ] Include user/tenant context (anonymized if needed)

### 4.2 Log Levels

- [ ] Define log level guidelines per environment
- [ ] Set production default to INFO
- [ ] Enable DEBUG dynamically when needed
- [ ] Ensure ERROR logs are actionable

**Level Guidelines:**
| Level | When to Use | Example |
|-------|-------------|---------|
| ERROR | Action required, service degraded | Database connection failed |
| WARN | Unexpected but handled | Retry succeeded after failure |
| INFO | Normal business events | Order created |
| DEBUG | Detailed technical info | Cache lookup result |

### 4.3 Log Aggregation

- [ ] Deploy log collectors (Fluentd, Fluent Bit, Vector)
- [ ] Configure log parsing and enrichment
- [ ] Set up log storage (Loki, Elasticsearch)
- [ ] Implement log retention policies
- [ ] Create log-based alerts for critical patterns

### 4.4 Log Security

- [ ] Mask PII and sensitive data
- [ ] Encrypt logs in transit and at rest
- [ ] Implement access controls
- [ ] Set up audit logging for log access

## Phase 5: Distributed Tracing

### 5.1 Instrumentation

- [ ] Add OpenTelemetry SDK to all services
- [ ] Enable auto-instrumentation where possible
- [ ] Add manual spans for business operations
- [ ] Include relevant attributes on spans
- [ ] Propagate context across service boundaries

### 5.2 Context Propagation

- [ ] Choose propagation format (W3C Trace Context recommended)
- [ ] Verify propagation across HTTP calls
- [ ] Verify propagation across message queues
- [ ] Test propagation through async operations

### 5.3 Sampling Strategy

- [ ] Implement tail-based sampling
- [ ] Configure baseline sampling rate (1-5%)
- [ ] Always sample errors (100%)
- [ ] Always sample slow requests (100% > threshold)
- [ ] Define critical path sampling rules

**Sampling Configuration:**
| Condition | Sample Rate |
|-----------|-------------|
| Default | 1-5% |
| Error status | 100% |
| Latency > p99 | 100% |
| Critical path | 100% |
| Health checks | 0% |

### 5.4 Trace Storage

- [ ] Deploy trace backend (Tempo, Jaeger)
- [ ] Configure retention period
- [ ] Set up trace-to-logs correlation
- [ ] Enable trace-to-metrics exemplars

## Phase 6: Alerting

### 6.1 Alert Design

- [ ] Base alerts on SLOs, not raw metrics
- [ ] Use multi-window, multi-burn-rate alerts
- [ ] Set appropriate `for` durations (avoid flapping)
- [ ] Include runbook URLs in annotations
- [ ] Add context in alert descriptions

### 6.2 Alert Severity

| Severity | Response | Example |
|----------|----------|---------|
| Critical | Page immediately (any time) | Service down, SLO breached |
| Warning | Review within hours | Elevated error rate |
| Info | Check during business hours | Unusual pattern detected |

### 6.3 Alert Routing

- [ ] Route critical alerts to PagerDuty/Opsgenie
- [ ] Route warnings to Slack/Teams
- [ ] Configure on-call schedules
- [ ] Set up escalation policies
- [ ] Implement alert grouping and deduplication

### 6.4 Runbooks

- [ ] Create runbook for every alerting rule
- [ ] Include diagnostic steps
- [ ] Document mitigation procedures
- [ ] Add escalation contacts
- [ ] Review and update runbooks quarterly

**Runbook Template:**
```markdown
# Alert: [AlertName]

## Summary
[What this alert means]

## Impact
[User/business impact]

## Diagnosis
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Mitigation
1. [Immediate action]
2. [Follow-up action]

## Escalation
- L1: [team/person]
- L2: [team/person]

## Related
- Dashboard: [link]
- Logs: [query]
- Traces: [link]
```

## Phase 7: Dashboards

### 7.1 Dashboard Hierarchy

- [ ] Create executive overview dashboard
- [ ] Build service-level dashboards (RED metrics)
- [ ] Design infrastructure dashboards (USE metrics)
- [ ] Add debugging/drill-down dashboards

### 7.2 Dashboard Best Practices

- [ ] Use consistent layouts across services
- [ ] Include SLO status prominently
- [ ] Add deployment markers
- [ ] Link to related dashboards
- [ ] Include time range presets
- [ ] Add documentation panels

### 7.3 Dashboard Content

**Service Dashboard (per service):**
- SLO status (current burn rate)
- Request rate
- Error rate
- Latency (p50, p95, p99)
- Top endpoints by latency/errors
- Resource utilization
- Recent deployments

## Phase 8: OpenTelemetry Collector

### 8.1 Collector Deployment

- [ ] Choose deployment mode (DaemonSet vs Deployment vs Sidecar)
- [ ] Configure resource limits
- [ ] Set up health checks
- [ ] Enable internal metrics

### 8.2 Collector Security

- [ ] Run as non-root user
- [ ] Use TLS for all receivers
- [ ] Bind to specific interfaces (not 0.0.0.0)
- [ ] Store secrets securely (env vars or secret store)
- [ ] Apply RBAC policies (Kubernetes)

### 8.3 Collector Pipelines

- [ ] Configure separate pipelines for logs, metrics, traces
- [ ] Add batch processor
- [ ] Add memory limiter processor
- [ ] Configure retry and timeout limits
- [ ] Enable compression for exporters

### 8.4 Collector Operations

- [ ] Monitor collector metrics
- [ ] Set up alerts for collector health
- [ ] Plan for collector scaling
- [ ] Document collector configuration

## Phase 9: Kubernetes Observability

### 9.1 Cluster-Level Metrics

- [ ] Node metrics (kubelet, node-exporter)
- [ ] API server metrics
- [ ] etcd metrics
- [ ] Controller manager metrics
- [ ] Scheduler metrics

### 9.2 Workload Metrics

- [ ] Pod resource metrics (cAdvisor)
- [ ] Container restart counts
- [ ] Pod scheduling latency
- [ ] PVC usage
- [ ] Network policies

### 9.3 Kubernetes Events

- [ ] Collect and store Kubernetes events
- [ ] Alert on critical events (OOMKilled, CrashLoopBackOff)
- [ ] Correlate events with metrics and traces

### 9.4 Service Mesh Observability

- [ ] Enable Istio/Linkerd metrics
- [ ] Configure distributed tracing
- [ ] Monitor mTLS certificate expiry
- [ ] Track service-to-service latency

## Phase 10: Cost Optimization

### 10.1 Data Volume Management

- [ ] Implement sampling strategies
- [ ] Set cardinality limits
- [ ] Drop unnecessary labels
- [ ] Aggregate high-volume metrics
- [ ] Filter health check logs

### 10.2 Storage Optimization

- [ ] Use tiered storage (hot/warm/cold)
- [ ] Configure appropriate retention per tier
- [ ] Enable compression
- [ ] Use object storage for long-term retention

### 10.3 Cost Monitoring

- [ ] Track data ingestion volume
- [ ] Monitor storage costs
- [ ] Review unused dashboards/alerts
- [ ] Audit metric cardinality regularly

### 10.4 Vendor Optimization

- [ ] Negotiate committed use discounts
- [ ] Review license utilization
- [ ] Consider open source alternatives
- [ ] Evaluate multi-tenant configurations

## Phase 11: Testing and Validation

### 11.1 Observability Testing

- [ ] Verify all services emit metrics
- [ ] Confirm log aggregation working
- [ ] Test trace propagation end-to-end
- [ ] Validate alert routing

### 11.2 Chaos Engineering

- [ ] Test observability during failures
- [ ] Verify alerts fire correctly
- [ ] Confirm runbooks are accurate
- [ ] Measure time to detection

### 11.3 Load Testing

- [ ] Test observability at peak load
- [ ] Verify collector scaling
- [ ] Check storage performance
- [ ] Validate query performance

## Phase 12: Operations

### 12.1 Documentation

- [ ] Document architecture decisions (ADRs)
- [ ] Create onboarding guides
- [ ] Maintain runbook index
- [ ] Document on-call procedures

### 12.2 Training

- [ ] Train team on observability tools
- [ ] Practice incident response
- [ ] Review post-mortems
- [ ] Share learnings across teams

### 12.3 Continuous Improvement

- [ ] Review SLOs quarterly
- [ ] Update alerts based on incidents
- [ ] Refine runbooks post-incident
- [ ] Track MTTR improvements
- [ ] Gather feedback from on-call engineers

## Quick Reference: Implementation Order

**Phase 1-2 (Foundation):** Requirements, SLOs
**Phase 3-5 (Data Collection):** Metrics, Logs, Traces
**Phase 6-7 (Actionability):** Alerting, Dashboards
**Phase 8-9 (Infrastructure):** Collector, Kubernetes
**Phase 10-12 (Optimization):** Cost, Testing, Operations

## Validation Checklist

Before going to production:

- [ ] All critical services have SLOs defined
- [ ] All SLOs have corresponding alerts
- [ ] All alerts have runbooks
- [ ] Dashboards exist for all services
- [ ] Traces correlate with logs
- [ ] On-call rotation is configured
- [ ] Cost projections are validated
- [ ] Team is trained on tools
