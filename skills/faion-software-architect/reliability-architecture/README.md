# Reliability Architecture

Designing systems that stay available, recover from failures, and degrade gracefully under stress.

## Overview

Reliability architecture ensures systems can withstand failures, maintain service quality under load, and recover quickly when problems occur. This guide covers fault tolerance patterns, SRE principles, chaos engineering, and disaster recovery strategies based on industry best practices for 2025-2026.

## Core Concepts

| Concept | Definition | Key Metric |
|---------|------------|------------|
| **Availability** | % of time system is operational | Uptime percentage (99.9%, 99.99%) |
| **Durability** | Data survives failures | Data loss probability |
| **Fault Tolerance** | System continues despite failures | Error budget consumption |
| **Resilience** | System recovers from failures | MTTR (Mean Time To Recovery) |
| **Reliability** | System performs correctly over time | MTBF (Mean Time Between Failures) |

## Availability Targets

| Level | Availability | Downtime/Year | Downtime/Month | Use Case |
|-------|--------------|---------------|----------------|----------|
| 2 nines | 99% | 3.65 days | 7.3 hours | Internal tools, dev environments |
| 3 nines | 99.9% | 8.76 hours | 43.8 minutes | Business applications |
| 4 nines | 99.99% | 52.6 minutes | 4.4 minutes | Critical services, e-commerce |
| 5 nines | 99.999% | 5.26 minutes | 26 seconds | Financial, healthcare, safety-critical |

**Decision Guide:**
- Startups/MVPs: Start with 99.9% (achievable with basic redundancy)
- Growth stage: Target 99.95% (requires proper failover)
- Enterprise: Target 99.99% (multi-region, active-active)
- Critical infrastructure: 99.999% (significant investment, operational excellence)

---

## SLIs, SLOs, and SLAs

### Definitions

```
SLI (Service Level Indicator) --> SLO (Service Level Objective) --> SLA (Service Level Agreement)
      "What we measure"               "Our internal target"           "Contract with customers"
```

### Common SLIs by Service Type

| Service Type | Primary SLIs |
|--------------|--------------|
| **API** | Latency (p50, p95, p99), Error rate, Throughput |
| **Database** | Query latency, Availability, Replication lag |
| **Storage** | Durability, Read/write latency, Availability |
| **Streaming** | End-to-end latency, Message loss rate, Throughput |
| **Batch Jobs** | Success rate, Processing time, Data freshness |

### SLO Best Practices

1. **Start Conservative**: Begin with achievable targets, tighten over time
2. **Use Error Budgets**: SLO of 99.9% = 0.1% error budget for experimentation
3. **Measure from User Perspective**: Synthetic monitoring + real user monitoring
4. **Tiered SLOs**: Different targets for different customer tiers
5. **Review Quarterly**: Adjust based on actual performance and business needs

### Example SLO Document

```yaml
service: payment-api
slos:
  - name: availability
    sli: "successful_requests / total_requests"
    target: 99.95
    window: 30d

  - name: latency
    sli: "request_latency_p99"
    target: "<500ms"
    window: 30d

  - name: error_rate
    sli: "error_requests / total_requests"
    target: "<0.1%"
    window: 30d

error_budget:
  monthly_budget_minutes: 21.6  # 0.05% of 43,200 minutes
  escalation_threshold: 50%     # Alert when 50% consumed
```

---

## Fault Tolerance Patterns

### 1. Circuit Breaker

Prevents cascading failures by stopping requests to a failing service.

**States:**
- **Closed**: Normal operation, requests flow through
- **Open**: Failures exceeded threshold, requests fail fast
- **Half-Open**: Test period, limited requests allowed

```
     Closed ----[failures > threshold]----> Open
        ^                                     |
        |                                     |
        +--[success in half-open]----> Half-Open
                                             |
                                             |
        Open <---[failure in half-open]------+
```

**Configuration Guidelines:**
| Parameter | Typical Value | Notes |
|-----------|---------------|-------|
| Failure threshold | 5-10 failures | Depends on traffic volume |
| Success threshold | 3-5 successes | Required to close circuit |
| Timeout (open state) | 30-60 seconds | Time before half-open |
| Failure window | 10-60 seconds | Rolling window for counting |

**When to Use:**
- External API calls
- Database connections
- Microservice-to-microservice calls
- Any I/O operation that can fail

### 2. Retry with Exponential Backoff and Jitter

Handles transient failures without overwhelming the system.

**Formula:**
```
wait_time = min(cap, base * 2^attempt) + random(0, jitter_range)
```

**Jitter Strategies:**
| Strategy | Formula | Use Case |
|----------|---------|----------|
| Full Jitter | `random(0, base * 2^attempt)` | General purpose |
| Equal Jitter | `base * 2^attempt / 2 + random(0, base * 2^attempt / 2)` | Moderate spread |
| Decorrelated Jitter | `min(cap, random(base, prev_sleep * 3))` | Best for high contention (Netflix/AWS recommended) |

**Best Practices:**
1. **Cap maximum delay**: 30-60 seconds typical
2. **Limit retry attempts**: 3-5 attempts maximum
3. **Only retry idempotent operations**: Or ensure idempotency
4. **Retry only transient errors**: 5xx, timeouts, network errors
5. **Don't retry**: 4xx client errors (except 429)

### 3. Bulkhead Pattern

Isolates failures to prevent cascading across the system.

**Types:**
| Type | Description | Implementation |
|------|-------------|----------------|
| Thread Pool | Separate thread pools per service | Java ExecutorService, Python ThreadPoolExecutor |
| Semaphore | Limit concurrent calls | Counting semaphore, rate limiter |
| Process | Separate processes per component | Containers, VMs |
| Connection Pool | Dedicated connection pools | Database-specific pools |

**Example Architecture:**
```
Application
  |
  +-- Pool A (10 connections) --> Service A
  |       [Failure here doesn't affect B]
  |
  +-- Pool B (10 connections) --> Service B
  |
  +-- Pool C (5 connections) --> Service C (less critical)
```

### 4. Timeout Management

Prevents indefinite waiting and resource exhaustion.

**Timeout Types:**
| Type | Description | Typical Value |
|------|-------------|---------------|
| Connection timeout | Time to establish connection | 3-5 seconds |
| Read timeout | Time to receive response | 5-30 seconds |
| Request timeout | Total time for entire request | 10-60 seconds |
| Idle timeout | Time before closing idle connection | 60-300 seconds |

**Best Practices:**
1. **Set explicit timeouts everywhere**: Never use infinite timeouts
2. **Timeout budget**: Distribute timeout across call chain
3. **Deadline propagation**: Pass remaining time to downstream services
4. **Circuit breaker integration**: Count timeouts as failures

---

## Graceful Degradation

### Principles

1. **Feature Ranking**: Classify features by criticality
2. **Fallback Strategies**: Define alternatives for each failure mode
3. **Progressive Degradation**: Degrade in stages, not all at once
4. **User Communication**: Inform users about reduced functionality

### Feature Criticality Matrix

| Priority | Category | Example | Degradation Strategy |
|----------|----------|---------|---------------------|
| P0 | Critical | Checkout, Login | Never degrade, maximum resources |
| P1 | Important | Search, Product pages | Cached results, simplified view |
| P2 | Standard | Recommendations, Reviews | Disable or show generic |
| P3 | Optional | Analytics, Personalization | Silently disable |

### Degradation Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Static Fallback** | Return cached/default data | Show cached product catalog |
| **Simplified Response** | Omit non-essential data | Return basic user profile |
| **Feature Toggle** | Disable features dynamically | Turn off recommendations |
| **Load Shedding** | Reject low-priority requests | Queue non-urgent requests |
| **Read-Only Mode** | Disable writes, allow reads | View but not modify data |

### Load Shedding Priority Levels

```
Normal load    --> Accept all requests
High load      --> Reject P3 (optional) requests
Critical load  --> Accept only P0 (critical) requests
Overload       --> Accept only health checks

Priority assignment:
1. Health checks (always)
2. Critical operations (payments, auth)
3. Standard requests (product pages)
4. Optional features (recommendations)
5. Background tasks (analytics)
```

---

## Redundancy Patterns

### Active-Passive (Failover)

```
Traffic --> Primary (Active)
              |
              | Replication
              v
            Secondary (Standby)

On failure: Traffic --> Secondary (becomes Active)
```

**Characteristics:**
- Lower cost (standby resources underutilized)
- Failover time: seconds to minutes
- Potential data loss during failover
- Good for: Databases, stateful services

### Active-Active

```
Traffic
   |
   +-----> Instance A <--sync--> Instance B
   |           |                     |
   +-----------|---------------------+
               |
           Shared State
```

**Characteristics:**
- Higher cost (all instances active)
- Instant failover (no switchover needed)
- Complexity in state synchronization
- Good for: Stateless services, global distribution

### Multi-Region Architecture

| Strategy | Recovery Time | Data Loss | Cost | Complexity |
|----------|--------------|-----------|------|------------|
| Backup/Restore | Hours | Hours of data | $ | Low |
| Pilot Light | 10-30 minutes | Minutes | $$ | Medium |
| Warm Standby | Minutes | Seconds | $$$ | High |
| Multi-Active | Near zero | Near zero | $$$$ | Very High |

---

## Health Checks and Probes

### Kubernetes Probe Types

| Probe | Purpose | On Failure | Check Frequency |
|-------|---------|------------|-----------------|
| **Liveness** | Is the process alive? | Restart container | Every 10-30s |
| **Readiness** | Can it serve traffic? | Remove from load balancer | Every 5-10s |
| **Startup** | Has it finished starting? | Blocks other probes | Until success |

### Health Check Best Practices

1. **Liveness Probe**:
   - Keep simple and lightweight
   - Don't check external dependencies
   - Use for detecting deadlocks, infinite loops
   - Set appropriate initialDelaySeconds

2. **Readiness Probe**:
   - Check all critical dependencies
   - Include database, cache, external services
   - More comprehensive than liveness
   - Use higher successThreshold (2-3)

3. **Startup Probe**:
   - Use for slow-starting applications
   - Set failureThreshold * periodSeconds > max startup time
   - Prevents liveness killing slow starts

### Health Endpoint Design

```
/health          # Basic liveness (is process running?)
/health/live     # Liveness probe endpoint
/health/ready    # Readiness probe endpoint
/health/startup  # Startup probe endpoint
/health/detailed # Full health with dependency status (internal only)
```

**Response Format:**
```json
{
  "status": "healthy",
  "checks": {
    "database": {"status": "healthy", "latency_ms": 5},
    "cache": {"status": "healthy", "latency_ms": 1},
    "external_api": {"status": "degraded", "latency_ms": 250}
  },
  "version": "1.2.3",
  "uptime_seconds": 86400
}
```

---

## Chaos Engineering

### Principles

1. **Define steady state**: What does "normal" look like? (SLIs, SLOs)
2. **Hypothesize impact**: Predict what will happen during failure
3. **Introduce failures**: Inject faults in controlled manner
4. **Observe and learn**: Compare actual vs expected behavior
5. **Minimize blast radius**: Start small, expand gradually

### Common Chaos Experiments

| Experiment | What It Tests | Tools |
|------------|---------------|-------|
| Instance termination | Auto-scaling, failover | Chaos Monkey, Gremlin |
| Network latency | Timeout handling | Toxiproxy, tc |
| Network partition | Split-brain handling | iptables, Gremlin |
| DNS failure | Service discovery | Gremlin |
| CPU/Memory stress | Autoscaling, throttling | stress-ng |
| Disk failure | Data durability | dd, fault injection |
| Zone/Region failure | Multi-zone resilience | Cloud provider tools |

### Chaos Maturity Model

| Level | Description | Practices |
|-------|-------------|-----------|
| 1 | Manual testing | Manual failovers, game days |
| 2 | Automated tests | Scheduled chaos in staging |
| 3 | Production chaos | Chaos in production (low traffic) |
| 4 | Continuous chaos | Always-on chaos, automatic remediation |
| 5 | Advanced chaos | Multi-fault injection, AI-driven chaos |

### Chaos Engineering Tools

| Tool | Type | Best For |
|------|------|----------|
| [Chaos Monkey](https://netflix.github.io/chaosmonkey/) | Instance termination | AWS, basic chaos |
| [Gremlin](https://www.gremlin.com/) | Full platform | Enterprise, comprehensive |
| [LitmusChaos](https://litmuschaos.io/) | Kubernetes-native | K8s environments |
| [Chaos Mesh](https://chaos-mesh.org/) | Kubernetes-native | K8s, cloud-native |
| [Toxiproxy](https://github.com/Shopify/toxiproxy) | Network failures | Network testing |
| [Pumba](https://github.com/alexei-led/pumba) | Docker chaos | Container environments |

---

## Disaster Recovery

### RPO and RTO

```
         <---------- RPO ---------->
         |                         |
---------+-------------------------+---------------------------> time
      Last backup              Disaster                    Recovery
                                  |                           |
                                  <---------- RTO ------------>
```

- **RPO** (Recovery Point Objective): Maximum acceptable data loss
- **RTO** (Recovery Time Objective): Maximum acceptable downtime

### DR Strategies Comparison

| Strategy | RTO | RPO | Cost | Description |
|----------|-----|-----|------|-------------|
| **Backup/Restore** | Hours | Hours | $ | Periodic backups, restore on failure |
| **Pilot Light** | 10-30 min | Minutes | $$ | Core services running, scale on failure |
| **Warm Standby** | Minutes | Seconds | $$$ | Scaled-down copy always running |
| **Hot Standby** | Seconds | Near-zero | $$$$ | Full copy running, instant failover |
| **Multi-Active** | Zero | Zero | $$$$$ | Multiple active sites, no failover needed |

### Backup Strategy: 3-2-1 Rule

- **3** copies of data
- **2** different storage types
- **1** offsite location

**Backup Types:**
| Type | Description | Frequency | Retention |
|------|-------------|-----------|-----------|
| Full | Complete backup | Weekly | 4-12 weeks |
| Differential | Changes since last full | Daily | 2 weeks |
| Incremental | Changes since last backup | Hourly | 1 week |

### DR Testing Schedule

| Test Type | Frequency | Duration | Scope |
|-----------|-----------|----------|-------|
| Backup verification | Weekly | Minutes | Data integrity |
| Failover testing | Monthly | Hours | Single component |
| DR drill | Quarterly | Half day | Full system |
| Full DR exercise | Annually | Full day | Complete failover |

---

## Data Reliability

### Replication Strategies

| Strategy | Consistency | Latency | Durability | Use Case |
|----------|-------------|---------|------------|----------|
| Synchronous | Strong | Higher | Highest | Financial transactions |
| Asynchronous | Eventual | Lower | High | Read replicas, analytics |
| Semi-synchronous | Tunable | Medium | High | Balanced workloads |
| Quorum-based | Tunable | Medium | High | Distributed databases |

### CAP Theorem Trade-offs

| Focus | Sacrifice | Examples |
|-------|-----------|----------|
| CP (Consistency + Partition) | Availability | HBase, MongoDB (strong mode) |
| AP (Availability + Partition) | Consistency | Cassandra, DynamoDB |
| CA (Consistency + Availability) | Partition tolerance | Traditional RDBMS (single node) |

---

## LLM Usage Tips

When using LLMs for reliability architecture design:

1. **Provide Context**: Share your SLO targets, traffic patterns, and constraints
2. **Request Trade-off Analysis**: Ask for pros/cons of different approaches
3. **Use Decision Frameworks**: Ask LLM to apply decision trees
4. **Validate Configurations**: Have LLM review your retry/timeout configs
5. **Generate Runbooks**: LLMs can help create incident response procedures

See [llm-prompts.md](llm-prompts.md) for ready-to-use prompts.

---

## External Resources

### Documentation
- [AWS Builders Library: Timeouts, retries and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Google Cloud: Design for graceful degradation](https://docs.cloud.google.com/architecture/framework/reliability/graceful-degradation)
- [Microsoft Azure: Circuit Breaker Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
- [Kubernetes: Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

### Tools and Libraries
- [Resilience4j](https://resilience4j.readme.io/) - Java resilience library
- [Polly](https://github.com/App-vNext/Polly) - .NET resilience library
- [Gremlin](https://www.gremlin.com/) - Chaos engineering platform
- [LitmusChaos](https://litmuschaos.io/) - Kubernetes chaos engineering

### Books
- "Release It!" by Michael Nygard - Foundational patterns
- "Site Reliability Engineering" by Google - SRE practices
- "Chaos Engineering" by Casey Rosenthal - Chaos principles

---

## Related Methodologies

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step reliability design checklist |
| [examples.md](examples.md) | Real-world implementation examples |
| [templates.md](templates.md) | Copy-paste configurations and code |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted design |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [performance-architecture](../performance-architecture/) | Performance optimization |
| [observability-architecture](../observability-architecture/) | Monitoring and alerting |
| [security-architecture](../security-architecture/) | Security considerations |
| [faion-devops-engineer](../../faion-devops-engineer/CLAUDE.md) | Infrastructure implementation |
| [faion-infrastructure-engineer](../../faion-infrastructure-engineer/CLAUDE.md) | K8s, cloud infrastructure |
