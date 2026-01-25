# Quality Attributes Analysis

Analyzing non-functional requirements (NFRs) for architecture decisions.

## Core Quality Attributes

### Performance
How fast does it respond?

| Metric | Description | Target Example |
|--------|-------------|----------------|
| Latency | Response time | p99 < 200ms |
| Throughput | Requests/second | 10,000 RPS |
| Resource usage | CPU, memory | < 70% utilization |

**Architecture tactics:**
- Caching (Redis, CDN)
- Connection pooling
- Async processing
- Database optimization

### Scalability
Can it handle growth?

| Type | Description |
|------|-------------|
| Vertical | Bigger machines |
| Horizontal | More machines |
| Elastic | Auto-scale up/down |

**Architecture tactics:**
- Stateless services
- Load balancing
- Database sharding
- Message queues

### Availability
What uptime is needed?

| Level | Downtime/year | Use Case |
|-------|---------------|----------|
| 99% | 3.65 days | Internal tools |
| 99.9% | 8.76 hours | Business apps |
| 99.99% | 52.6 minutes | Critical systems |
| 99.999% | 5.26 minutes | Life-critical |

**Architecture tactics:**
- Redundancy
- Failover
- Health checks
- Circuit breakers

### Reliability
Does it work correctly?

| Metric | Description |
|--------|-------------|
| MTBF | Mean time between failures |
| MTTR | Mean time to recovery |
| Error rate | Failed requests % |

**Architecture tactics:**
- Retries with backoff
- Idempotency
- Graceful degradation
- Chaos engineering

### Security
Is it protected?

| Aspect | Concern |
|--------|---------|
| Authentication | Who are you? |
| Authorization | What can you do? |
| Confidentiality | Data encryption |
| Integrity | Data tampering |
| Non-repudiation | Audit trails |

**Architecture tactics:**
- Zero trust
- Defense in depth
- Encryption at rest/transit
- Least privilege

### Maintainability
Can it be changed easily?

| Aspect | Metric |
|--------|--------|
| Modularity | Component independence |
| Testability | Test coverage ease |
| Deployability | Release frequency |
| Debuggability | Time to diagnose |

**Architecture tactics:**
- Clean architecture
- Dependency injection
- Feature flags
- Observability

### Consistency
Data correctness guarantees.

| Type | Description | Use Case |
|------|-------------|----------|
| Strong | Immediate consistency | Financial transactions |
| Eventual | Converges over time | Social feeds |
| Causal | Respects causality | Chat messages |

**CAP Theorem:**
- Consistency
- Availability
- Partition tolerance

Pick 2 of 3 during network partition.

## Analysis Framework

### 1. Identify Stakeholders
Who cares about which attributes?

| Stakeholder | Priority Attributes |
|-------------|---------------------|
| Users | Performance, Availability |
| Ops | Maintainability, Reliability |
| Security | Security, Compliance |
| Business | Scalability, Cost |

### 2. Define Scenarios

```
Stimulus: [What happens]
Source: [Who/what triggers]
Environment: [Normal/Overload/Attack]
Response: [System behavior]
Measure: [Success criteria]
```

**Example:**
```
Stimulus: 10x traffic spike
Source: Marketing campaign
Environment: Production
Response: Auto-scale, serve all requests
Measure: p99 latency < 500ms, 0 errors
```

### 3. Prioritize (MoSCoW)

| Priority | Attributes |
|----------|------------|
| Must have | Availability 99.9%, Security |
| Should have | p99 < 200ms |
| Could have | Multi-region |
| Won't have | Real-time sync |

### 4. Document Trade-offs

| Decision | Favors | Sacrifices |
|----------|--------|------------|
| Strong consistency | Correctness | Performance |
| Eventual consistency | Performance | Immediate accuracy |
| Microservices | Scalability | Complexity |
| Monolith | Simplicity | Independent scaling |

## Quality Attribute Worksheet

```markdown
## Attribute: [Name]

### Priority
[ ] Critical  [ ] High  [ ] Medium  [ ] Low

### Current State
[Description of current capability]

### Target State
[Desired capability with metrics]

### Gap Analysis
[What needs to change]

### Architectural Approach
[How to achieve target]

### Trade-offs
[What we sacrifice]

### Verification
[How to measure success]
```

## Related

- [trade-off-analysis.md](trade-off-analysis.md) - Decision framework
- [system-design-process.md](system-design-process.md) - Design workflow
- [reliability-architecture.md](reliability-architecture.md) - Deep dive
- [performance-architecture.md](performance-architecture.md) - Deep dive
- [security-architecture.md](security-architecture.md) - Deep dive
