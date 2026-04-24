# LLM Prompts for Reliability Architecture

Effective prompts for using LLMs (Claude, GPT-4, Gemini) to assist with reliability architecture design, analysis, and implementation.

---

## Table of Contents

1. [SLO Definition](#slo-definition)
2. [Fault Tolerance Design](#fault-tolerance-design)
3. [Circuit Breaker Configuration](#circuit-breaker-configuration)
4. [Retry Policy Design](#retry-policy-design)
5. [Health Check Design](#health-check-design)
6. [Graceful Degradation](#graceful-degradation)
7. [Chaos Engineering](#chaos-engineering)
8. [Disaster Recovery](#disaster-recovery)
9. [Reliability Review](#reliability-review)
10. [Incident Analysis](#incident-analysis)

---

## SLO Definition

### Define SLOs for a Service

```
I need to define SLOs for a [service type] with the following characteristics:
- User base: [number of users, geographic distribution]
- Traffic pattern: [steady/spiky, peak times, seasonal variations]
- Business criticality: [revenue impact, user impact]
- Current performance: [if known, include current metrics]

Please help me:
1. Identify appropriate SLIs (availability, latency, error rate, throughput)
2. Recommend SLO targets with rationale
3. Calculate error budget
4. Define alerting thresholds (50%, 75%, 90% budget consumption)
5. Suggest measurement approach (synthetic vs real user monitoring)

Consider industry benchmarks and our constraints: [list constraints like cost, team size, existing infrastructure].
```

### Error Budget Policy

```
Help me create an error budget policy for our team with these constraints:
- SLO: [99.9% availability, <500ms p99 latency]
- Team size: [X engineers]
- Release frequency: [daily/weekly/monthly]
- Current error budget consumption rate: [if known]

I need:
1. Error budget calculation methodology
2. Decision framework when budget is consumed
3. Trade-offs between velocity and reliability
4. Escalation procedures
5. Exception handling process
```

---

## Fault Tolerance Design

### Identify Single Points of Failure

```
Analyze the following architecture for single points of failure:

[Paste architecture diagram or description, including:
- Components (services, databases, caches)
- Dependencies (internal and external)
- Network topology
- Data flow]

For each SPOF identified:
1. Describe the failure mode
2. Assess impact (blast radius, data loss risk, recovery time)
3. Propose mitigation strategies with cost/complexity trade-offs
4. Prioritize fixes based on risk and effort
```

### Design Redundancy

```
I need to design redundancy for [component type: database/cache/service/etc.] with:
- Availability target: [99.9%, 99.99%, etc.]
- RPO requirement: [data loss tolerance]
- RTO requirement: [downtime tolerance]
- Budget constraints: [approximate budget]
- Geographic requirements: [single region/multi-region]

Please recommend:
1. Redundancy pattern (active-passive, active-active, N+1)
2. Failover mechanism (automatic/manual, DNS/load balancer)
3. Data replication strategy (sync/async)
4. Testing approach for failover
5. Estimated cost breakdown
```

---

## Circuit Breaker Configuration

### Configure Circuit Breaker

```
I need to configure a circuit breaker for calls to [service name] with these characteristics:
- Average latency: [X ms]
- P99 latency: [Y ms]
- Current error rate: [Z%]
- Traffic volume: [requests per second]
- Downstream dependency: [critical/non-critical]
- Fallback available: [yes/no, describe fallback]

Help me determine:
1. Failure threshold (number of failures to trip)
2. Success threshold (successes to close)
3. Timeout duration (time in open state)
4. Half-open behavior (how many test requests)
5. Failure window (sliding window size)
6. Which errors should count as failures (5xx only? timeouts? specific codes?)
7. Monitoring metrics to track

Explain the trade-offs for each recommendation.
```

### Circuit Breaker for Microservices

```
I have a microservices architecture with the following call graph:

[Describe or diagram service dependencies, e.g.:
API Gateway -> Service A -> Service B -> Database
API Gateway -> Service A -> Service C -> External API
Service B -> Cache]

Design a circuit breaker strategy that:
1. Prevents cascading failures
2. Handles different failure characteristics per dependency
3. Coordinates circuit states across services
4. Provides appropriate fallbacks at each layer

Include specific configuration recommendations for each circuit breaker.
```

---

## Retry Policy Design

### Design Retry Policy

```
I need a retry policy for [operation type] with these characteristics:
- Operation: [API call/database query/message publish/etc.]
- Typical success latency: [X ms]
- Timeout: [Y seconds]
- Idempotent: [yes/no]
- User-facing: [yes/no]
- Downstream capacity: [can it handle retry traffic?]

Help me design:
1. Retry strategy (immediate/exponential backoff/linear)
2. Maximum attempts
3. Base delay and cap
4. Jitter approach (full/equal/decorrelated)
5. Which errors to retry (transient only)
6. Circuit breaker integration
7. Logging and metrics

Consider the risk of retry storms and downstream overload.
```

### Retry vs Circuit Breaker Decision

```
For the following failure scenarios, help me decide whether to use retry, circuit breaker, or both:

Scenario 1: [External payment API with occasional 503 errors]
Scenario 2: [Database connection pool exhaustion during traffic spikes]
Scenario 3: [Downstream service with gradual degradation under load]
Scenario 4: [Third-party API with rate limiting (429 responses)]

For each scenario:
1. Recommend the appropriate pattern(s)
2. Explain the reasoning
3. Provide configuration suggestions
4. Describe the expected behavior during failure
```

---

## Health Check Design

### Design Health Endpoints

```
I'm implementing health checks for a [service type] with these dependencies:
- Primary database: [PostgreSQL/MySQL/etc.]
- Cache: [Redis/Memcached/etc.]
- External APIs: [list critical external dependencies]
- Message queue: [Kafka/RabbitMQ/etc., if applicable]

The service runs on Kubernetes with:
- Startup time: [typical startup duration]
- Memory-intensive initialization: [yes/no]
- Graceful shutdown requirements: [yes/no]

Design health check endpoints for:
1. Liveness probe (what should it check?)
2. Readiness probe (which dependencies to verify?)
3. Startup probe (is it needed? configuration?)

Include:
- HTTP response format (what data to include)
- Timeout recommendations for each probe
- Kubernetes probe configuration (initialDelaySeconds, periodSeconds, etc.)
- Security considerations (what NOT to expose)
```

### Health Check Implementation Review

```
Review this health check implementation for potential issues:

[Paste health check code]

Analyze:
1. Is the liveness check simple enough? (Should not check external deps)
2. Is the readiness check comprehensive enough?
3. Are timeouts appropriate?
4. Is there risk of cascading health check failures?
5. Is sensitive information exposed?
6. Are the checks performant enough for frequent polling?

Suggest improvements with code examples.
```

---

## Graceful Degradation

### Design Degradation Strategy

```
I need a graceful degradation strategy for [application type] with these features:
- P0 (Critical): [list critical features, e.g., checkout, login]
- P1 (Important): [list important features]
- P2 (Standard): [list standard features]
- P3 (Optional): [list optional features]

Current failure scenarios:
- Database overload
- Cache failure
- External recommendation API down
- High latency from payment provider

Design a degradation strategy that:
1. Defines degradation behavior for each priority level
2. Specifies triggers for each degradation level
3. Provides fallback implementations
4. Maintains user experience during partial failures
5. Includes recovery criteria

Include feature flag recommendations and code patterns.
```

### Load Shedding Strategy

```
Our system experiences traffic spikes of [X times] normal load during [peak events].
Current capacity: [Y requests/second]
Peak capacity needed: [Z requests/second]

We cannot scale infinitely due to [database limits/external API limits/cost].

Design a load shedding strategy that:
1. Prioritizes request types (critical vs optional)
2. Implements admission control at the right layer
3. Provides clear signals to clients (429 vs 503)
4. Maintains fairness across customers
5. Allows for priority/premium traffic

Include queue depth recommendations and client retry guidance.
```

---

## Chaos Engineering

### Design Chaos Experiment

```
I want to run a chaos experiment to test [specific resilience concern]:

System context:
- Architecture: [describe components]
- Current failure handling: [describe existing patterns]
- SLOs: [list relevant SLOs]
- Environment: [production/staging, traffic level]

Design a chaos experiment that:
1. Defines the steady-state hypothesis
2. Specifies the fault to inject (type, magnitude, duration)
3. Identifies observability requirements
4. Sets blast radius limits
5. Defines abort criteria
6. Outlines expected vs actual outcome comparison

Include rollback procedures and safety mechanisms.
```

### Chaos Experiment Suite

```
I want to build a comprehensive chaos engineering practice for [system description].

Current maturity: [none/basic/intermediate/advanced]
Team experience: [describe team's chaos engineering experience]
Tools available: [Gremlin/LitmusChaos/custom/none]

Design a chaos engineering roadmap with:
1. Phase 1: Basic experiments (low risk, high learning)
2. Phase 2: Intermediate experiments (moderate risk)
3. Phase 3: Advanced experiments (complex failure scenarios)
4. Phase 4: Continuous chaos (automated, production)

For each phase, specify:
- Experiment types
- Target systems
- Success criteria
- Learning objectives
- Prerequisites
```

---

## Disaster Recovery

### Design DR Strategy

```
Design a disaster recovery strategy for [system type] with:
- RPO requirement: [X hours/minutes]
- RTO requirement: [Y hours/minutes]
- Data volume: [approximate size]
- Geographic requirements: [region constraints]
- Compliance requirements: [GDPR/HIPAA/SOC2/etc.]
- Budget constraints: [approximate budget]

Current infrastructure:
- Cloud provider: [AWS/GCP/Azure/on-prem]
- Database: [type and size]
- Storage: [types and volumes]
- Compute: [service types]

Recommend:
1. DR strategy (backup/restore, pilot light, warm standby, hot standby)
2. Data replication approach
3. Infrastructure provisioning (IaC templates)
4. Failover procedure (automatic vs manual)
5. Testing schedule and procedures
6. Cost estimate

Include trade-off analysis for different RTO/RPO levels.
```

### DR Runbook Creation

```
Create a disaster recovery runbook for [failure scenario]:

System: [describe system]
DR infrastructure: [describe DR setup]
Team structure: [on-call rotation, escalation path]

The runbook should include:
1. Incident detection criteria (how do we know DR is needed?)
2. Assessment phase checklist (5 minutes)
3. Decision tree (when to failover vs wait)
4. Failover steps with commands (10 minutes)
5. Verification checklist (5 minutes)
6. Communication templates (internal and external)
7. Failback procedure
8. Post-incident tasks

Format for easy use during incident (clear, numbered steps, copy-paste commands).
```

---

## Reliability Review

### Architecture Reliability Review

```
Review this architecture for reliability concerns:

[Paste architecture diagram or description]

Analyze:
1. Single points of failure
2. Fault tolerance gaps
3. Timeout and retry configuration appropriateness
4. Health check adequacy
5. Graceful degradation capabilities
6. Disaster recovery readiness
7. Monitoring and alerting coverage

For each issue found:
- Severity (critical/high/medium/low)
- Potential impact
- Recommended fix
- Implementation effort

Prioritize recommendations based on risk and effort.
```

### Production Readiness Review

```
We're launching [new service/feature] to production. Review readiness:

Service details:
- Description: [what it does]
- Dependencies: [list internal and external dependencies]
- Traffic expectation: [requests per second]
- SLO targets: [availability, latency]

Current implementation:
- [List implemented reliability features]

Checklist for production readiness:
1. Fault tolerance (circuit breakers, retries, timeouts)
2. Health checks (liveness, readiness)
3. Graceful degradation (fallbacks, load shedding)
4. Observability (metrics, logs, traces, alerts)
5. Disaster recovery (backups, failover)
6. Runbooks (incident response procedures)
7. Capacity planning (scaling, limits)

Identify gaps and recommend priorities for launch.
```

---

## Incident Analysis

### Post-Incident Analysis

```
Analyze this incident for reliability improvements:

Incident summary:
- What happened: [description]
- Duration: [X minutes/hours]
- Impact: [users affected, revenue impact]
- Root cause: [if known]

Timeline:
[Paste incident timeline]

Metrics during incident:
[Paste relevant metrics]

Analyze:
1. What reliability patterns could have prevented this?
2. What patterns could have reduced impact?
3. What patterns could have sped up recovery?
4. What monitoring gaps existed?
5. What runbook improvements are needed?

Provide actionable recommendations with implementation priority.
```

### Failure Mode Analysis

```
Analyze failure modes for [component/service]:

Component details:
- Type: [database/cache/API/queue/etc.]
- Dependencies: [list dependencies]
- Consumers: [list consumers]
- Traffic patterns: [describe patterns]

For each potential failure mode:
1. Describe the failure (what breaks, how it manifests)
2. Assess likelihood (rare/occasional/common)
3. Assess impact (minor/moderate/severe/critical)
4. Identify detection mechanisms
5. Propose mitigation strategies
6. Define recovery procedures

Create a failure mode matrix with risk scores.
```

---

## Prompt Engineering Tips

### For Best Results

1. **Provide context**: Include system characteristics, constraints, and requirements
2. **Be specific**: Mention exact numbers (latency, traffic, budget) when possible
3. **Include existing setup**: Describe what's already implemented
4. **State constraints**: Budget, team size, timeline, compliance requirements
5. **Ask for trade-offs**: Request pros/cons for recommendations

### Follow-up Prompts

After receiving initial recommendations:

```
For recommendation [X], explain:
1. Why is this threshold/configuration recommended?
2. What happens if I make it more/less aggressive?
3. How do I monitor if it's working correctly?
4. When should I revisit this configuration?
```

```
Provide implementation guidance for [recommendation]:
1. Code examples in [language]
2. Configuration for [framework/tool]
3. Testing approach
4. Rollout strategy
```

```
Compare alternatives:
- Option A: [first approach]
- Option B: [second approach]

Which is better for our context: [describe context]?
```

---

## Quick Reference: Prompt Templates

| Task | Key Information to Include |
|------|---------------------------|
| SLO Definition | User base, traffic, business criticality, current metrics |
| Circuit Breaker | Latency, error rate, traffic volume, fallback availability |
| Retry Policy | Operation type, idempotency, timeout, downstream capacity |
| Health Checks | Dependencies, startup time, Kubernetes context |
| Degradation | Feature priorities, failure scenarios, user impact |
| Chaos Experiment | Architecture, SLOs, environment, safety requirements |
| DR Strategy | RPO/RTO, data volume, compliance, budget |
| Reliability Review | Full architecture description, current implementation |
