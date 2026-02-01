# Performance Architecture

Designing systems for speed, efficiency, and scalability. This methodology covers performance requirements definition, optimization strategies, and continuous performance engineering.

## Overview

Performance architecture ensures systems meet latency, throughput, and resource efficiency requirements under expected and peak loads. It spans the entire stack from client-side rendering to database query optimization.

## Performance Goals (SLOs)

Define measurable targets using Service Level Objectives:

| Metric | Startup/MVP | Growth | Enterprise |
|--------|-------------|--------|------------|
| Response time (p50) | < 200ms | < 100ms | < 50ms |
| Response time (p95) | < 500ms | < 300ms | < 150ms |
| Response time (p99) | < 2s | < 1s | < 500ms |
| Throughput | > 1,000 RPS | > 10,000 RPS | > 100,000 RPS |
| Error rate | < 1% | < 0.1% | < 0.01% |
| Availability | 99.9% | 99.95% | 99.99% |

**Error Budget Calculation:**
- 99.9% availability = 43.8 minutes downtime/month
- 99.95% availability = 21.9 minutes downtime/month
- 99.99% availability = 4.4 minutes downtime/month

## Performance Layers

Performance optimization targets different layers:

```
Layer 1: CLIENT
  Browser rendering, JS execution, network latency
  Target: First Contentful Paint < 1.5s, Time to Interactive < 3s

Layer 2: EDGE/CDN
  Static assets, edge caching, compression, edge functions
  Target: Cache hit ratio > 95%, Edge latency < 50ms globally

Layer 3: LOAD BALANCER
  Request distribution, health checks, SSL termination
  Target: Connection overhead < 5ms

Layer 4: APPLICATION
  Code efficiency, concurrency, algorithms, async processing
  Target: Request processing < 100ms (excluding I/O)

Layer 5: DATA
  Query optimization, indexing, caching, connection pooling
  Target: DB query p95 < 50ms, Cache hit ratio > 85%
```

## Scalability Patterns

### Horizontal Scaling (Scale Out)

Add more instances to handle increased load:

```
Load Balancer
      |
  +---+---+---+
  |   |   |   |
 S1  S2  S3  S4  (stateless, identical instances)
  |   |   |   |
  +---+---+---+
        |
   Shared State (Redis/DB)
```

**Requirements:**
- Stateless application design (externalize sessions)
- Shared state management (Redis, distributed cache)
- Database connection pooling
- Service discovery

**Kubernetes HPA (2025):**
- Auto-scales pods based on CPU, memory, or custom metrics
- New in K8s 1.33: Configurable tolerance for scale up/down
- Combine with Cluster Autoscaler for infrastructure scaling
- Cost savings: 50-70% with proper autoscaling

### Vertical Scaling (Scale Up)

Increase resources (CPU, RAM) on existing instances:

| Aspect | Horizontal | Vertical |
|--------|------------|----------|
| Limit | Near-infinite | Hardware limits |
| Downtime | Zero | Usually required |
| Complexity | Higher | Lower |
| Cost | Linear | Exponential |
| Best for | Web apps, APIs | Databases, legacy |

### Data Partitioning

**Horizontal (Sharding):**
```
Users A-M  --> Shard 1 (DB instance 1)
Users N-Z  --> Shard 2 (DB instance 2)
```

**Vertical:**
```
User profiles --> Users DB
Order history --> Orders DB
Analytics     --> Analytics DB (ClickHouse)
```

## Caching Strategies

### Cache Hierarchy

```
Request --> Browser Cache --> CDN Cache --> App Cache --> DB Query Cache --> Database
             (0ms)           (10-50ms)     (1-5ms)       (5-20ms)          (50-200ms)
```

### Caching Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Cache-Aside | App manages cache; load on miss | General purpose |
| Read-Through | Cache loads from DB on miss | Simplified app logic |
| Write-Through | Sync write to cache and DB | Strong consistency |
| Write-Behind | Async write to DB from cache | High write throughput |
| Cache Prefetching | Preload cache before requests | Predictable access |

**Cache Invalidation Strategies:**
- TTL (Time-To-Live): Simple, eventual consistency
- Event-driven: Invalidate on writes, stronger consistency
- Version tags: ETags, cache busting

**Performance Targets:**
- L1 Cache (in-memory): Hit rate > 95%, latency < 1ms
- L2 Cache (Redis): Hit rate > 85%, latency < 5ms

### Redis Best Practices (2025)

- Use Redis Cluster for horizontal scaling
- Implement request coalescing to prevent cache stampedes
- Set appropriate eviction policies (LRU for general, LFU for hot data)
- Monitor with `INFO stats`, `SLOWLOG`
- Consider Redis 7.x features: Functions, multi-part AOF

## Database Performance

### Query Optimization

```sql
-- Bad: Function on column prevents index use
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- Good: Range query uses index
SELECT * FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';

-- Bad: SELECT * fetches unnecessary data
SELECT * FROM users WHERE id = 1;

-- Good: Select only needed columns
SELECT id, name, email FROM users WHERE id = 1;
```

### Indexing Strategy

| Index Type | Use Case | PostgreSQL |
|------------|----------|------------|
| B-tree (default) | Equality, range queries | `CREATE INDEX` |
| Hash | Equality only | `CREATE INDEX USING hash` |
| GIN | Arrays, JSONB, full-text | `CREATE INDEX USING gin` |
| GiST | Geometric, range types | `CREATE INDEX USING gist` |
| BRIN | Large sorted tables | `CREATE INDEX USING brin` |

**Indexing Rules:**
1. Index columns in WHERE clauses
2. Index foreign keys
3. Create composite indexes matching query order
4. Consider partial indexes for filtered queries
5. Use covering indexes to avoid table lookups

### Connection Pooling

```
Application (100 requests) --> Connection Pool (20 connections) --> Database
```

**Tools:**
- PostgreSQL: PgBouncer, Pgpool-II
- MySQL: ProxySQL
- Application-level: HikariCP (Java), SQLAlchemy pools (Python)

**Sizing Formula:**
```
pool_size = (core_count * 2) + effective_spindle_count
```
For SSDs: `pool_size = core_count * 2` (typically 10-50 connections)

## Async Processing

### Message Queue Selection

| Broker | Throughput | Latency | Best For |
|--------|------------|---------|----------|
| Kafka | 500K/s | 2-8ms | Event streaming, log aggregation |
| RabbitMQ | 25K/s | 1-5ms | Complex routing, RPC |
| Redis Streams | 100K/s | <1ms | Simple queues, real-time |
| SQS/Service Bus | Variable | 10-50ms | Serverless, cloud-native |

**Decision Matrix:**
- Need event replay/time-travel --> Kafka
- Need complex routing --> RabbitMQ
- Need simplicity + low latency --> Redis Streams
- Need serverless integration --> Cloud queues

### Async Patterns

**Background Jobs:**
```
HTTP Request --> API --> Quick Response (202 Accepted)
                  |
                  v
               Queue --> Worker --> Heavy Processing --> Notify
```

**Batch Processing:**
```python
# Bad: N database calls
for item in items:
    db.insert(item)  # 1000 items = 1000 queries

# Good: Single batch call
db.bulk_insert(items)  # 1000 items = 1 query
```

## Load Balancing

### Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Round Robin | Rotate through servers | Equal capacity servers |
| Least Connections | Route to least busy | Variable request duration |
| IP Hash | Same client same server | Session affinity |
| Weighted | Distribute by capacity | Mixed hardware |
| Random | Random selection | Simple, surprisingly effective |

### Health Checks

- **Liveness**: Is the process running?
- **Readiness**: Can it handle traffic?
- **Custom**: Application-specific checks (DB connection, etc.)

## CDN and Edge Computing

### CDN Architecture

```
User (Europe) --> CDN Edge (Frankfurt) --[cache miss]--> Origin (US-East)
                        |
                  [cache hit]
                        |
                        v
                  Fast Response (<50ms)
```

### Edge Functions (2025)

| Platform | Cold Start | Global Locations | Best For |
|----------|------------|------------------|----------|
| Cloudflare Workers | <1ms | 330+ cities | Edge logic, personalization |
| Vercel Edge | <5ms | 100+ regions | Next.js, React |
| AWS Lambda@Edge | 50-200ms | CloudFront POPs | AWS ecosystem |
| Fastly Compute | <10ms | 90+ POPs | High-throughput APIs |

**Edge Function Use Cases:**
- A/B testing at the edge
- Geolocation-based routing
- Authentication/authorization
- Request/response transformation
- Rate limiting

**Avoid Edge For:**
- Database-heavy operations (5+ queries)
- CPU-intensive tasks (image processing, ML)
- Complex orchestration workflows

### Asset Optimization

| Technique | Benefit | Implementation |
|-----------|---------|----------------|
| Minification | 30-50% size reduction | Build tools (esbuild, Terser) |
| Compression | 70-90% smaller (Brotli) | CDN/server config |
| Image optimization | WebP: 25-35% smaller | Cloudinary, imgproxy |
| Bundle splitting | Load on demand | Code splitting, lazy imports |
| Tree shaking | Remove dead code | Modern bundlers |

## Performance Testing

### Test Types

| Type | Purpose | When |
|------|---------|------|
| Smoke | Basic functionality | Every deploy |
| Load | Expected traffic | Weekly, before release |
| Stress | Beyond capacity | Monthly |
| Spike | Sudden traffic bursts | Before events |
| Soak | Memory leaks, degradation | Monthly |

### Tools Comparison

| Tool | Language | Cloud Support | Best For |
|------|----------|---------------|----------|
| k6 | JavaScript | Grafana Cloud | Modern teams, CI/CD |
| Locust | Python | Distributed | Python teams, custom load |
| JMeter | Java | Various | Complex scenarios, GUI |
| Artillery | JavaScript | Artillery Cloud | Node.js teams |
| Gatling | Scala | Enterprise | High performance |

### k6 Best Practices

- Start small, gradually increase load
- Use realistic scenarios (login, browse, checkout)
- Set custom thresholds matching SLOs
- Integrate with CI/CD pipelines
- Combine with Grafana for visualization

## Profiling and Bottleneck Identification

### APM Tools (2025)

| Tool | Strength | Pricing |
|------|----------|---------|
| Datadog | Full-stack, 600+ integrations | Per host |
| New Relic | Transparent pricing, OTEL | Per GB |
| Dynatrace | AI-powered (Davis AI) | Per GiB |
| Grafana Cloud | Open source stack | Per metric/log |
| Uptrace | Cost-effective, OTEL-native | Per span |

### Profiling Strategy

1. **APM dashboards**: Identify slow endpoints
2. **Distributed tracing**: Find cross-service bottlenecks
3. **Flame graphs**: CPU/memory hotspots in code
4. **Database profiling**: Slow queries, missing indexes
5. **Network analysis**: Latency, packet loss

### Common Bottlenecks

| Symptom | Likely Cause | Investigation |
|---------|--------------|---------------|
| High CPU | Inefficient algorithms, GC pressure | CPU profiler, flame graphs |
| High memory | Leaks, large objects | Memory profiler, heap dumps |
| High latency | N+1 queries, sync I/O | APM traces, DB slow log |
| Low throughput | Connection limits, thread pool | Resource metrics, pool stats |
| Intermittent errors | Resource exhaustion, race conditions | Error logs, distributed traces |

## Performance Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| N+1 queries | 100 items = 101 queries | Eager loading, batch queries |
| Sync external calls | Blocking on slow services | Async/await, circuit breakers |
| No caching | Repeated expensive operations | Multi-layer caching |
| Over-fetching | Transferring unused data | Pagination, field selection |
| No connection pooling | Connection overhead | Use connection pools |
| Large payloads | Slow transfers | Compression, pagination |
| Missing indexes | Full table scans | EXPLAIN ANALYZE, add indexes |
| Premature optimization | Wasted effort | Profile first, optimize second |

## Capacity Planning

### Calculate Requirements

```
Peak concurrent users: 100,000
Requests per user per minute: 10
Peak RPS: 100,000 * 10 / 60 = 16,667 RPS

With 2x headroom: 33,334 RPS target
With 3x for growth: 50,000 RPS target
```

### Resource Sizing

```
Single instance capacity: 500 RPS
Required instances: 50,000 / 500 = 100
With N+1 redundancy: 101 instances
With 50% headroom: 150 instances
```

## LLM-Assisted Performance Analysis

Use LLMs effectively for performance work:

**Best For:**
- Analyzing slow query logs
- Reviewing caching strategies
- Suggesting indexing improvements
- Writing load test scripts
- Interpreting profiler output

**Provide Context:**
- Current metrics and SLOs
- Technology stack details
- Traffic patterns
- Resource constraints
- Budget limitations

**Example Prompt Pattern:**
```
Context: [Tech stack, current metrics]
Problem: [Specific performance issue]
Constraints: [Budget, time, compatibility]
Question: [What you need help with]
```

## External Resources

### Documentation
- [Google SRE Book - Performance](https://sre.google/sre-book/handling-overload/)
- [AWS Performance Efficiency Pillar](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/)
- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [Redis Best Practices](https://redis.io/docs/management/optimization/)

### Tools
- [k6 Load Testing](https://k6.io/docs/)
- [Grafana](https://grafana.com/docs/)
- [pganalyze](https://pganalyze.com/) - PostgreSQL performance
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) - Frontend performance

### Learning
- [High Scalability Blog](http://highscalability.com/)
- [awesome-scalability GitHub](https://github.com/binhnguyennus/awesome-scalability)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Capacity planning | opus | Complex infrastructure analysis |
| Caching strategy | sonnet | Cache invalidation patterns |
| Cache configuration | haiku | Redis/Memcached setup |
## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [caching-architecture](../caching-architecture/) | Deep dive on caching patterns |
| [observability-architecture](../observability-architecture/) | Monitoring and alerting |
| [reliability-architecture](../reliability-architecture/) | SLOs, error budgets |
| [database-selection](../database-selection/) | Choosing the right database |
| [microservices-architecture](../microservices-architecture/) | Distributed system patterns |
