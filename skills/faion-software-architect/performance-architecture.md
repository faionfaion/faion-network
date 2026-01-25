# Performance Architecture

Designing systems for speed and efficiency.

## Performance Goals

Define measurable targets:

| Metric | Example Target |
|--------|----------------|
| Response time (p50) | < 100ms |
| Response time (p95) | < 300ms |
| Response time (p99) | < 1s |
| Throughput | > 10,000 RPS |
| Error rate | < 0.1% |

## Performance Layers

```
┌─────────────────────────────────────────────────────┐
│                    Client                            │
│  Browser rendering, JS execution, network           │
├─────────────────────────────────────────────────────┤
│                    CDN / Edge                        │
│  Static assets, edge caching, compression           │
├─────────────────────────────────────────────────────┤
│                    Load Balancer                     │
│  Request distribution, health checks                │
├─────────────────────────────────────────────────────┤
│                    Application                       │
│  Code efficiency, concurrency, algorithms           │
├─────────────────────────────────────────────────────┤
│                    Data                              │
│  Query optimization, indexing, caching              │
└─────────────────────────────────────────────────────┘
```

## Caching Strategy

### Cache Hierarchy

```
Request ──▶ CDN Cache ──▶ App Cache ──▶ DB Cache ──▶ Database
              │              │             │
              └──────────────┴─────────────┘
                    Cache hits (fast)
```

### Cache Placement

| Layer | Type | Latency | Use Case |
|-------|------|---------|----------|
| Browser | Local | ~0ms | Static assets |
| CDN | Edge | ~10ms | Public content |
| Redis | Memory | ~1ms | Session, hot data |
| DB Cache | Query | ~5ms | Query results |

### Caching Patterns

```
# Read-Through
Request ──▶ Cache ──miss──▶ Database
              │◀────────────load────│
              │
           hit│
              ▼
           Response

# Write-Through
Write ──▶ Cache ──▶ Database (sync)

# Write-Behind
Write ──▶ Cache ──▶ Queue ──▶ Database (async)
```

## Database Optimization

### Query Optimization

```sql
-- Bad: Full table scan
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- Good: Index-friendly
SELECT * FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at < '2025-01-01';
```

### Indexing Strategy

```
Primary key ──▶ Clustered index (one per table)
Foreign keys ──▶ Non-clustered indexes
Frequent WHERE ──▶ Covered indexes
ORDER BY ──▶ Include in index
```

### Connection Pooling

```
Application ──┬──▶ Connection Pool ──▶ Database
              │         │
              │    [10-50 connections]
              │         │
              └─────────┘
              (reuse connections)
```

## Horizontal Scaling

### Stateless Services

```
Load Balancer
      │
  ┌───┼───┬───┐
  ▼   ▼   ▼   ▼
 S1  S2  S3  S4  (stateless, identical)
  │   │   │   │
  └───┴───┴───┘
        │
   Shared State
   (Redis, DB)
```

### Data Partitioning

```
# Horizontal (Sharding)
Users A-M ──▶ Shard 1
Users N-Z ──▶ Shard 2

# Vertical
User data ──▶ Users DB
Order data ──▶ Orders DB
```

## Async Processing

### Message Queue Pattern

```
Sync request ──▶ API ──▶ Quick response
                  │
                  ▼
                Queue ──▶ Worker ──▶ Heavy processing
```

### Batch Processing

```
# Instead of:
for item in items:
    db.insert(item)  # N queries

# Do:
db.bulk_insert(items)  # 1 query
```

## Load Balancing Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Round Robin | Rotate through servers | Equal capacity |
| Least Connections | Route to least busy | Varying load |
| IP Hash | Same client → same server | Sticky sessions |
| Weighted | Distribute by capacity | Mixed hardware |

## Content Delivery

### CDN Architecture

```
User (EU) ──▶ CDN Edge (EU) ──cache miss──▶ Origin (US)
                    │
              cache hit
                    │
                    ▼
               Fast response
```

### Asset Optimization

| Technique | Benefit |
|-----------|---------|
| Minification | Reduce file size |
| Compression (gzip, brotli) | 70-90% smaller |
| Image optimization | WebP, lazy loading |
| Bundle splitting | Load on demand |
| Tree shaking | Remove unused code |

## Performance Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| N+1 queries | Too many DB calls | Batch/join queries |
| No caching | Repeated expensive ops | Add caching layer |
| Sync everything | Blocking on slow ops | Async processing |
| Over-fetching | Too much data | Pagination, fields |
| No connection pooling | Connection overhead | Use pools |
| Large payloads | Slow transfers | Compression, pagination |

## Capacity Planning

### Calculate Requirements

```
Peak users: 100,000
Requests per user: 10/min
Peak RPS: 100,000 × 10 / 60 = ~16,700 RPS

With 2x headroom: 33,400 RPS target
```

### Resource Sizing

```
Single instance: 500 RPS
Required: 33,400 / 500 = 67 instances
With redundancy: ~80 instances
```

## Performance Testing

### Types

| Type | Purpose |
|------|---------|
| Load testing | Expected load |
| Stress testing | Beyond capacity |
| Spike testing | Sudden load |
| Soak testing | Sustained load |

### Tools

- **k6** - Modern load testing
- **Apache JMeter** - Feature-rich
- **Locust** - Python-based
- **Artillery** - Node.js based

### Example (k6)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Stay
    { duration: '1m', target: 0 },    // Ramp down
  ],
};

export default function () {
  const res = http.get('https://api.example.com/');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

## Performance Monitoring

### Key Metrics

```
Latency: p50, p95, p99
Throughput: requests/second
Errors: error rate %
Saturation: CPU, memory, disk, network
```

### Alerting Thresholds

```yaml
alerts:
  - name: high_latency
    condition: p95_latency > 500ms
    for: 5m
    severity: warning

  - name: error_spike
    condition: error_rate > 1%
    for: 1m
    severity: critical
```

## Performance Optimization Checklist

- [ ] Response time SLOs defined
- [ ] Caching strategy implemented
- [ ] Database queries optimized
- [ ] Connection pooling enabled
- [ ] Async processing for heavy tasks
- [ ] CDN for static assets
- [ ] Compression enabled
- [ ] Load testing completed
- [ ] Monitoring and alerting setup

## Related

- [caching-architecture.md](caching-architecture.md) - Caching patterns
- [reliability-architecture.md](reliability-architecture.md) - SLOs
- [observability-architecture.md](observability-architecture.md) - Monitoring
