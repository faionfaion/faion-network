# System Design Process

End-to-end workflow for designing software systems.

## Process Steps

```
1. UNDERSTAND REQUIREMENTS
   ├─ Functional requirements (what it does)
   ├─ Non-functional requirements (quality attributes)
   ├─ Constraints (budget, timeline, team skills)
   └─ Scale estimates (users, data, requests)

2. DEFINE SCOPE
   ├─ In scope / Out of scope
   ├─ MVP vs full solution
   └─ Phased approach if needed

3. HIGH-LEVEL DESIGN
   ├─ Major components
   ├─ Data flow
   ├─ User interactions
   └─ External integrations

4. DEEP DIVE
   ├─ Database schema
   ├─ API design
   ├─ Caching strategy
   └─ Critical algorithms

5. IDENTIFY BOTTLENECKS
   ├─ Single points of failure
   ├─ Scalability limits
   └─ Performance hotspots

6. SCALE & OPTIMIZE
   ├─ Horizontal vs vertical scaling
   ├─ Caching layers
   ├─ Database optimization
   └─ CDN, load balancing
```

## Requirements Gathering

### Functional Requirements
- What does the system do?
- User stories, use cases
- Core features vs nice-to-have

### Non-Functional Requirements (Quality Attributes)

| Attribute | Question | Metric |
|-----------|----------|--------|
| Scalability | How many users/requests? | RPS, concurrent users |
| Availability | What uptime needed? | 99.9%, 99.99% |
| Latency | How fast must it respond? | p50, p95, p99 |
| Durability | Can we lose data? | RPO, RTO |
| Consistency | Strong or eventual? | CAP trade-off |
| Security | What threats? | Threat model |

### Scale Estimates

```
Users: _____ (daily active)
Requests: _____ RPS (peak)
Data: _____ GB/day (storage growth)
Bandwidth: _____ MB/s (network)
```

## Back-of-Envelope Calculations

### Traffic Estimates
```
DAU = Daily Active Users
RPS = DAU × requests_per_user / 86400
Peak RPS = RPS × peak_multiplier (usually 2-3x)
```

### Storage Estimates
```
Storage/day = objects_per_day × object_size
Storage/year = Storage/day × 365
With replication = Storage × replication_factor
```

### Memory/Cache Estimates
```
Cache size = hot_data_percentage × total_data
Cache hit rate target = 80-95%
```

## Design Document Template

```markdown
# System Design: [Name]

## 1. Requirements
### Functional
### Non-Functional
### Constraints

## 2. High-Level Design
[Diagram]

## 3. Component Design
### Component A
### Component B

## 4. Data Model
### Schema
### Indexes

## 5. API Design
### Endpoints
### Contracts

## 6. Scalability
### Current capacity
### Scaling strategy

## 7. Trade-offs & Alternatives
### Option A vs B

## 8. Open Questions
```

## Common System Design Patterns

| Pattern | Use Case |
|---------|----------|
| Load Balancer | Distribute traffic |
| CDN | Static content, reduce latency |
| Cache | Reduce DB load, improve latency |
| Message Queue | Async processing, decoupling |
| Database Replication | Read scaling, availability |
| Sharding | Write scaling, large datasets |
| Rate Limiting | Protect from abuse |
| Circuit Breaker | Handle downstream failures |

## Related

- [c4-model.md](c4-model.md) - Diagramming
- [quality-attributes-analysis.md](quality-attributes-analysis.md) - Deep dive on NFRs
- [trade-off-analysis.md](trade-off-analysis.md) - Decision making
