# Reliability Architecture

Designing systems that stay available and recover from failures.

## Reliability Concepts

| Concept | Definition |
|---------|------------|
| Availability | % of time system is operational |
| Durability | Data survives failures |
| Fault Tolerance | Continues despite failures |
| Resilience | Recovers from failures |

## Availability Targets

| Availability | Downtime/Year | Use Case |
|--------------|---------------|----------|
| 99% (2 nines) | 3.65 days | Internal tools |
| 99.9% (3 nines) | 8.76 hours | Business apps |
| 99.99% (4 nines) | 52.6 minutes | Critical services |
| 99.999% (5 nines) | 5.26 minutes | Financial, healthcare |

## SLIs, SLOs, SLAs

```
SLI (Indicator) ──▶ SLO (Objective) ──▶ SLA (Agreement)
   "What we measure"   "Our target"      "Contract with users"

Example:
SLI: Request latency p99
SLO: < 300ms for 99.9% of requests
SLA: Credits if SLO missed for > 1 hour
```

## Redundancy Patterns

### Active-Passive

```
         Traffic
            │
            ▼
    ┌───────────────┐
    │   Primary     │◀──Healthcheck──┐
    │  (active)     │                │
    └───────┬───────┘                │
            │ replication            │
            ▼                        │
    ┌───────────────┐                │
    │   Secondary   │────────────────┘
    │  (standby)    │
    └───────────────┘

    Failover: Switch traffic to secondary on primary failure
```

### Active-Active

```
         Traffic
            │
    ┌───────┴───────┐
    ▼               ▼
┌────────┐     ┌────────┐
│Instance│◀───▶│Instance│
│   A    │sync │   B    │
└────────┘     └────────┘

Both serve traffic, sync state
```

## Failure Handling Patterns

### Circuit Breaker

```
        ┌──────────────────────────────────┐
        │         Circuit Breaker           │
        │                                   │
Closed ─┼──▶ Failures exceed threshold ──▶ Open
   ▲    │                                   │
   │    │                                   │
   │    │         After timeout             │
   │    │                                   ▼
   │    │                              Half-Open
   │    │                                   │
   │    │◀── Success ──────────────────────┘
   │    │
   └────┼── Failure ──▶ Open (reset timeout)
        └──────────────────────────────────┘
```

### Retry with Backoff

```python
def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)  # 1s, 2s, 4s
            delay += random.uniform(0, delay * 0.1)  # Jitter
            time.sleep(delay)
```

### Bulkhead

```
┌─────────────────────────────────────────┐
│              Application                 │
│  ┌──────────┐  ┌──────────┐            │
│  │ Pool A   │  │ Pool B   │            │
│  │ (10 conn)│  │ (10 conn)│            │
│  └────┬─────┘  └────┬─────┘            │
│       │             │                   │
│       ▼             ▼                   │
│   Service A     Service B               │
│                                         │
│   Failure in A doesn't affect B         │
└─────────────────────────────────────────┘
```

### Timeout

```
Request ──▶ Service ──▶ Response
    │                      │
    │◀───────────────────▶│
         Timeout (e.g., 5s)

    If exceeded: Return error, don't wait forever
```

## Data Reliability

### Replication Strategies

| Strategy | Consistency | Latency | Durability |
|----------|-------------|---------|------------|
| Sync replication | Strong | Higher | Highest |
| Async replication | Eventual | Lower | High |
| Semi-sync | Tunable | Medium | High |

### Backup Strategy

```
Backup Types:
┌────────────────────────────────────────┐
│ Full    │■■■■■■■■■■│ All data (weekly) │
│ Diff    │■■■□□□□□□□│ Since full (daily)│
│ Incr    │■□□□□□□□□□│ Since last (hourly│
└────────────────────────────────────────┘

3-2-1 Rule:
- 3 copies of data
- 2 different storage types
- 1 offsite location
```

## Disaster Recovery

### RPO and RTO

```
       ◀────────── RPO ──────────▶
       │                         │
───────┼─────────────────────────┼─────────────────▶ time
    Last backup              Disaster           Recovery
                                │                  │
                                │◀────── RTO ─────▶│
```

**RPO** (Recovery Point Objective): Max acceptable data loss
**RTO** (Recovery Time Objective): Max acceptable downtime

### DR Strategies

| Strategy | RTO | RPO | Cost |
|----------|-----|-----|------|
| Backup/Restore | Hours | Hours | $ |
| Pilot Light | Minutes | Minutes | $$ |
| Warm Standby | Seconds | Seconds | $$$ |
| Multi-Active | ~0 | ~0 | $$$$ |

## Health Checks

### Liveness vs Readiness

```yaml
# Liveness: Is the process alive?
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5

# Readiness: Can it serve traffic?
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Health Check Endpoints

```python
# /health - Liveness
@app.get("/health")
def health():
    return {"status": "ok"}

# /ready - Readiness (check dependencies)
@app.get("/ready")
def ready():
    db_ok = check_database()
    cache_ok = check_cache()

    if db_ok and cache_ok:
        return {"status": "ready"}
    else:
        raise HTTPException(status_code=503)
```

## Graceful Degradation

### Feature Flags

```python
def get_recommendations(user_id):
    if feature_enabled("ml_recommendations"):
        try:
            return ml_service.recommend(user_id)
        except ServiceUnavailable:
            pass  # Fallback below

    # Degraded: Return popular items instead
    return get_popular_items()
```

### Load Shedding

```
Normal load: Accept all requests
High load: Reject low-priority requests
Critical load: Accept only critical requests

Priority levels:
1. Health checks (always)
2. Critical operations (payments)
3. Normal requests (list items)
4. Optional features (recommendations)
```

## Chaos Engineering

### Principles

1. Define steady state
2. Hypothesize about impact
3. Introduce failures
4. Observe and learn
5. Minimize blast radius

### Common Experiments

| Experiment | Tests |
|------------|-------|
| Kill instance | Auto-healing, failover |
| Network latency | Timeout handling |
| DNS failure | Service discovery |
| CPU stress | Autoscaling |
| Fill disk | Monitoring, alerts |

### Tools

- **Chaos Monkey** - Netflix
- **Gremlin** - Commercial
- **LitmusChaos** - Kubernetes
- **Toxiproxy** - Network failures

## Reliability Checklist

### Design
- [ ] Single points of failure identified
- [ ] Redundancy for critical components
- [ ] Failure modes documented
- [ ] SLOs defined

### Implementation
- [ ] Circuit breakers implemented
- [ ] Retries with backoff
- [ ] Timeouts configured
- [ ] Health checks added
- [ ] Graceful degradation

### Operations
- [ ] Monitoring and alerting
- [ ] Runbooks for incidents
- [ ] DR plan tested
- [ ] Regular backups verified
- [ ] Chaos experiments run

## Related

- [performance-architecture.md](performance-architecture.md) - Performance
- [observability-architecture.md](observability-architecture.md) - Monitoring
- [distributed-patterns.md](distributed-patterns.md) - Distributed systems
