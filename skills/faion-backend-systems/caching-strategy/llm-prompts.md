# LLM Prompts for Caching Strategy

Effective prompts for AI-assisted caching design, implementation, and optimization.

## Architecture Design Prompts

### Initial Caching Strategy

```
I need to design a caching strategy for my application.

**System Context:**
- Application type: [web app / API / microservices / mobile backend]
- Traffic: [X requests/sec average, Y peak]
- Database: [PostgreSQL / MongoDB / DynamoDB]
- Current latency: p95 = [X]ms
- Infrastructure: [AWS / GCP / on-premise / Kubernetes]

**Data Characteristics:**
- Read/write ratio: [X:Y]
- Most accessed entities: [users, products, etc.]
- Update frequency: [real-time / hourly / daily]
- Data size: [total X GB, average record Y KB]

**Requirements:**
- Target latency: p95 < [X]ms
- Acceptable staleness: [seconds / minutes / hours]
- Budget constraints: [open source only / managed services OK]

**Please provide:**
1. Recommended cache layers (L1/L2/L3)
2. Caching pattern (cache-aside/write-through/write-behind)
3. Technology recommendations (Redis/Memcached/local)
4. TTL strategy per entity type
5. Invalidation approach
6. Key risks and mitigations
```

### Technology Selection

```
Help me choose a caching technology for my use case.

**Requirements:**
- Scale: [X GB data, Y requests/sec]
- Features needed:
  - [ ] Key-value store
  - [ ] Pub/sub
  - [ ] Geospatial queries
  - [ ] Sorted sets
  - [ ] Transactions
  - [ ] Clustering
  - [ ] Persistence

**Constraints:**
- Deployment: [Kubernetes / AWS / GCP / bare metal]
- Team expertise: [languages/tools familiar with]
- Availability target: [99.9% / 99.99%]
- Budget: [self-hosted / managed / hybrid]

**Compare:**
- Redis
- Memcached
- Hazelcast
- Apache Ignite
- In-process cache (e.g., Caffeine, node-cache)

Provide comparison matrix and recommendation with reasoning.
```

---

## Implementation Prompts

### Cache-Aside Pattern

```
Generate cache-aside implementation for [Python/Node.js/Go/Java].

**Requirements:**
- Entity: [User/Product/Order]
- Data source: [MongoDB/PostgreSQL/REST API]
- Cache: Redis
- Features:
  - Automatic key generation
  - TTL: [seconds]
  - Serialization: [JSON/MessagePack/Pickle]
  - Error handling (graceful degradation)
  - Invalidation helper

**Include:**
1. Cache decorator/wrapper
2. Key generation logic
3. Error handling
4. Invalidation function
5. Usage examples
6. Unit tests
```

### Write-Through Implementation

```
Implement write-through caching for [entity type] with strong consistency.

**Context:**
- Database: [PostgreSQL/MongoDB]
- Cache: Redis
- Language: [Python/Node.js/Go]
- Entity: [name]
- Write frequency: [X writes/sec]

**Requirements:**
- Atomic write (DB + cache)
- Rollback on failure
- TTL: [seconds]
- Monitoring (log writes)

Generate production-ready code with error handling.
```

### Rate Limiting

```
Generate rate limiting implementation using Redis.

**Requirements:**
| Tier | Requests/min | Requests/day |
|------|-------------|--------------|
| Free | 60 | 1,000 |
| Pro | 600 | 100,000 |
| Enterprise | 6,000 | Unlimited |

**Features:**
- Sliding window algorithm
- Per-API-key limits
- Response headers (X-RateLimit-*)
- Graceful handling (429 response)
- Storage: Redis

**Framework:** [Express/Flask/FastAPI/Go Gin]

Include:
1. Middleware implementation
2. Redis operations
3. Response format
4. Retry-After header
```

---

## Optimization Prompts

### Performance Analysis

```
Analyze my caching implementation for performance issues.

**Current Metrics:**
- Hit rate: [X]%
- p95 latency: [X]ms (cache hit), [Y]ms (cache miss)
- Memory usage: [X]GB / [Y]GB available
- Evictions: [X] per hour
- Miss rate: [X]%

**Code:**
[paste caching code]

**Please analyze:**
1. Is hit rate acceptable? (Target: >80%)
2. Are TTL values optimal?
3. Is key structure efficient?
4. Are there stampede risks?
5. Is serialization efficient?
6. Suggest improvements with code examples
```

### Stampede Prevention

```
I'm experiencing cache stampede on key: [key_name].

**Context:**
- Traffic spike: [X] concurrent requests
- Cache TTL: [seconds]
- Miss latency: [X] seconds (slow query)
- Current behavior: All requests hit DB simultaneously

**Requirements:**
- Language: [Python/Node.js/Go]
- Cache: Redis
- Pattern preference: [distributed lock / probabilistic refresh / coalescing]

Generate stampede prevention code with:
1. Lock acquisition logic
2. Timeout handling
3. Fallback strategy
4. Metrics/logging
```

### Memory Optimization

```
My Redis instance is running out of memory.

**Current State:**
- Used memory: [X]GB / [Y]GB
- Evictions: [X] per hour
- Key count: [X]
- Top key prefixes by memory:
  [paste output of MEMORY DOCTOR or similar]

**Questions:**
1. Which eviction policy should I use? (currently: [policy])
2. Should I compress values? (average value size: [X]KB)
3. Should I adjust TTL? (current: [values])
4. Do I need to scale up or partition?
5. Provide Redis config recommendations
```

---

## Troubleshooting Prompts

### Low Hit Rate

```
My cache hit rate is only [X]% (target: >80%).

**Details:**
- Entity: [type]
- TTL: [seconds]
- Invalidation: [strategy]
- Access pattern: [description]
- Cache size: [X]GB
- Eviction policy: [policy]

**Metrics:**
- Requests: [X]/sec
- Hits: [X]/sec
- Misses: [X]/sec
- Evictions: [X]/hour

**Possible causes:**
- TTL too short?
- Invalidation too aggressive?
- Working set > cache size?
- Non-cacheable queries?

Please diagnose and suggest fixes.
```

### Stale Data Issues

```
Users are seeing stale data in [feature].

**Context:**
- Entity: [type]
- TTL: [seconds]
- Update frequency: [X] per hour
- Invalidation: [event-based/time-based]
- Cache: Redis

**Problem:**
- User updates [entity]
- Other users see old data for [X] seconds/minutes

**Questions:**
1. Is invalidation strategy correct?
2. Should I use write-through instead?
3. Are there race conditions?
4. How to invalidate related entities?
5. Generate improved invalidation code
```

### Connection Issues

```
I'm getting Redis connection errors intermittently.

**Error:**
[paste error message]

**Context:**
- Redis: [version, deployment type]
- Client library: [name and version]
- Error frequency: [X] per hour
- Traffic: [X] requests/sec
- Connection pool: [current config]

**Please help:**
1. Diagnose likely cause
2. Recommend connection pool settings
3. Implement retry logic
4. Add circuit breaker
5. Improve error handling
```

---

## Monitoring & Alerting Prompts

### Metrics Dashboard

```
Generate monitoring queries for my caching layer.

**Stack:**
- Cache: Redis
- Monitoring: [Prometheus/Datadog/CloudWatch]
- Application: [language/framework]

**Required metrics:**
1. Hit rate (%)
2. Miss rate (%)
3. Latency histogram (p50, p95, p99)
4. Memory usage
5. Eviction count
6. Key count by namespace
7. Connection pool stats

**Output format:**
- PromQL queries (if Prometheus)
- Grafana dashboard JSON
- Alert rules (hit rate < 60%, memory > 90%)
```

### Cache Health Check

```
Implement comprehensive cache health check endpoint.

**Requirements:**
- Framework: [Express/Flask/FastAPI]
- Cache: Redis
- Health indicators:
  - [ ] Connectivity
  - [ ] Response time (<50ms)
  - [ ] Memory usage (<80%)
  - [ ] Hit rate (>60%)
  - [ ] Eviction rate (<X per hour)

**Output format:**
- HTTP 200 if healthy
- HTTP 503 if unhealthy
- JSON response with detailed status

Generate code for health check route.
```

---

## Migration Prompts

### Add Caching to Existing Code

```
Add caching to my existing function without breaking it.

**Current Code:**
[paste function code]

**Requirements:**
- Cache: Redis
- TTL: [seconds]
- Invalidation triggers: [on update/delete]
- Backward compatible (gradual rollout)
- Feature flag: CACHE_ENABLED

**Please:**
1. Wrap function with caching
2. Add cache invalidation
3. Add feature flag
4. Preserve error handling
5. Add logging (cache hit/miss)
6. Provide A/B test code
```

### Cache Warming

```
Generate cache warming strategy for [entity type].

**Context:**
- Entity: [User/Product/etc.]
- Count: [X] total
- Hot entities: Top [Y]% by access
- Cache: Redis
- Load time: Acceptable: <[X] minutes

**Strategy preferences:**
- [ ] Warm on startup
- [ ] Warm on deployment
- [ ] Background warming
- [ ] On-demand + prediction

**Please provide:**
1. Warming script
2. Priority algorithm (which to warm first)
3. Concurrency control (don't overload DB)
4. Progress tracking
5. Monitoring
```

---

## Best Practices for LLM Prompts

### Do's

1. **Provide context** - System scale, traffic patterns, constraints
2. **Specify metrics** - Current performance, target performance
3. **Include data characteristics** - Read/write ratio, update frequency
4. **Show existing code** - Makes suggestions more relevant
5. **Ask for trade-offs** - Compare different approaches

### Don'ts

1. **Don't be vague** - "Make it faster" vs "Reduce p95 latency from 200ms to 50ms"
2. **Don't omit scale** - Caching for 100 RPS vs 10k RPS is very different
3. **Don't forget monitoring** - Always ask for metrics/observability
4. **Don't ignore errors** - Request proper error handling

### Iterative Refinement

Start broad, then refine:

```
1. "Design caching strategy for e-commerce catalog"
   -> Get high-level architecture

2. "Generate cache-aside implementation for products with Redis"
   -> Get specific pattern code

3. "Add stampede prevention to the cache-aside code"
   -> Enhance implementation

4. "Add Prometheus metrics for hit rate and latency"
   -> Add observability

5. "Review for production readiness (error handling, scaling)"
   -> Final review
```

---

## Prompt Templates for Common Tasks

### Quick Implementation

```
Generate [pattern] caching for [entity] in [language]:
- Cache: [Redis/Memcached/local]
- TTL: [seconds]
- Invalidation: [strategy]
- Include: error handling, logging, tests

Output: production-ready code with comments.
```

### Performance Review

```
Review this caching code for:
1. Performance bottlenecks
2. Race conditions
3. Memory leaks
4. Stampede risks
5. Missing error handling

Code:
[paste code]

Provide specific fixes with line numbers.
```

### Configuration Optimization

```
Optimize my Redis configuration for:
- Use case: [description]
- Data size: [X]GB
- Traffic: [Y] RPS
- Availability: [99.9% / 99.99%]

Current config:
[paste redis.conf relevant sections]

Suggest optimizations for:
- Memory management
- Persistence
- Replication
- Performance
```

---

## Example Conversation Flow

**User:** I need caching for my product catalog API.

**Prompt:**
```
Design caching strategy for product catalog API.

Context:
- 50k products, 5k RPS reads, 10 writes/min
- PostgreSQL database
- Current p95 latency: 300ms
- Target: <50ms

Recommend: layers, pattern, TTL, tech stack
```

**LLM:** Recommends multi-layer (local + Redis), cache-aside, 1hr TTL

**User:** Generate the cache-aside implementation.

**Prompt:**
```
Generate Python cache-aside for products:
- Redis cache
- TTL: 3600s
- PostgreSQL source
- Include: decorator, error handling, invalidation
```

**LLM:** Provides code

**User:** Add stampede prevention.

**Prompt:**
```
Add distributed lock to prevent stampede:
- Current code: [paste]
- Use Redis SETNX
- Timeout: 10s
- Return stale data if lock fails
```

**LLM:** Enhances code with locking

**User:** How do I monitor this?

**Prompt:**
```
Add Prometheus metrics to cache code:
- Hit rate
- Latency (hit/miss)
- Lock acquisition rate

Include: metric definitions, dashboard JSON
```

**LLM:** Adds monitoring
