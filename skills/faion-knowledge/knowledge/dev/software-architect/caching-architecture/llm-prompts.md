# LLM Prompts for Caching Architecture

Effective prompts for LLM-assisted caching design, implementation, and optimization.

## Discovery and Requirements

### Workload Analysis Prompt

```
Analyze my application's caching needs:

**Application Type:** [e-commerce / SaaS / social media / API / etc.]
**Tech Stack:** [Python/Django, Node.js, Go, etc.]
**Database:** [PostgreSQL, MongoDB, etc.]
**Current Scale:** [DAU, requests/sec, data size]
**Pain Points:** [slow queries, high DB load, etc.]

Please help me:
1. Identify what data should be cached
2. Recommend caching layers (browser, CDN, application, DB)
3. Suggest caching patterns for each data type
4. Estimate expected improvements
```

### Cache Strategy Selection Prompt

```
Help me choose the right caching pattern for these data types:

| Data Type | Read/Write Ratio | Consistency Need | Change Frequency |
|-----------|------------------|------------------|------------------|
| User profiles | 100:1 | Eventual OK | Daily |
| Product catalog | 1000:1 | 5-min delay OK | Hourly |
| Shopping cart | 10:1 | Strong | Per-minute |
| Inventory | 50:1 | Real-time | Per-second |

For each data type, recommend:
1. Caching pattern (cache-aside, write-through, etc.)
2. TTL strategy
3. Invalidation approach
4. Redis data structure (if applicable)
```

### Consistency Requirements Prompt

```
I need to design caching for a [type of system] where:

- Users expect to see their own updates within [X seconds]
- Different users can tolerate [Y seconds] of stale data
- Critical operations are: [list operations]
- We're using [database] and considering [cache tech]

Help me design a caching strategy that balances consistency and performance:
1. Which data needs strong consistency?
2. Which data can use eventual consistency?
3. How to implement read-your-writes consistency?
4. Recommended invalidation strategy
```

---

## Architecture Design

### Multi-Layer Cache Architecture Prompt

```
Design a multi-layer caching architecture for my application:

**Requirements:**
- Global users (US, EU, Asia)
- 50K requests/second at peak
- Mix of static and dynamic content
- API responses need personalization

**Current Stack:**
- Frontend: [React/Next.js/Gatsby]
- Backend: [Django/FastAPI/Express/Go]
- Database: [PostgreSQL/MongoDB]
- Cloud: [AWS/GCP/Cloudflare]

Please design:
1. Cache layer diagram with data flow
2. Technology selection for each layer
3. TTL strategy per layer
4. Cache key design patterns
5. Invalidation flow across layers
```

### Redis Cluster Architecture Prompt

```
Help me design a Redis cluster for caching:

**Requirements:**
- Data size: [X GB]
- Operations: [reads/sec], [writes/sec]
- Availability: [99.9% / 99.99%]
- Budget constraints: [if any]
- Cloud provider: [AWS/GCP/self-hosted]

Please recommend:
1. Cluster topology (standalone, sentinel, cluster)
2. Number of nodes and memory per node
3. Sharding strategy
4. Replication configuration
5. Backup and persistence settings
6. Failover behavior
```

### CDN Caching Strategy Prompt

```
Design a CDN caching strategy for my website:

**Site Type:** [static site / dynamic app / hybrid]
**Content Types:** [HTML, CSS/JS, images, API responses]
**Personalization:** [none / by region / by user]
**CDN Provider:** [Cloudflare / CloudFront / Fastly]

For each content type, specify:
1. Edge caching rules (what to cache, what to bypass)
2. TTL settings (edge vs browser)
3. Cache key configuration (vary headers, query strings)
4. Purge/invalidation strategy
5. Cache-Control header templates
```

---

## Implementation

### Cache-Aside Implementation Prompt

```
Implement cache-aside pattern for [language/framework]:

**Requirements:**
- Entity: [User / Product / Order]
- Cache: Redis
- Database: [PostgreSQL / MongoDB]
- TTL: [X minutes]
- Handle cache stampede

Provide:
1. Complete implementation with error handling
2. Cache key design
3. Serialization approach
4. Stampede prevention (locking or probabilistic)
5. Metrics/logging for cache hits/misses
6. Unit tests
```

### Write-Through Implementation Prompt

```
Implement write-through caching for [entity]:

**Context:**
- Language: [Python/TypeScript/Go]
- Cache: Redis
- Database: [PostgreSQL]
- Consistency: Strong required

The implementation should:
1. Update cache and DB atomically (or with proper error handling)
2. Handle partial failures gracefully
3. Include transaction rollback logic
4. Log all cache operations
5. Include retry logic for transient failures
```

### Cache Invalidation System Prompt

```
Design a cache invalidation system:

**Architecture:**
- Multiple application instances
- Redis cluster for caching
- Events from: [DB triggers / application events / message queue]
- Need to invalidate: [specific keys / patterns / tags]

Implement:
1. Event-based invalidation with pub/sub
2. Pattern-based invalidation (wildcard keys)
3. Tag-based invalidation (group keys)
4. Cross-datacenter invalidation
5. Monitoring for invalidation latency
```

### Cache Warming Script Prompt

```
Create a cache warming script for deployment:

**Cache Contents:**
- Top 1000 products
- Active user sessions
- Configuration data
- Frequently accessed [entities]

Requirements:
1. Throttled loading (don't overwhelm DB)
2. Progress reporting
3. Error handling with retries
4. Parallel loading where safe
5. Verification step
6. Integration with deployment pipeline

Language: [Python/Node.js/Go]
```

---

## Cache Stampede Prevention

### Locking Implementation Prompt

```
Implement distributed locking to prevent cache stampede:

**Scenario:**
- High-traffic endpoint (10K req/sec)
- Cache TTL: 5 minutes
- DB query time: 200ms
- Language: [Python/TypeScript/Go]

Implement:
1. Redis-based distributed lock
2. Lock timeout handling
3. Fallback for lock acquisition failure
4. Metrics for lock contention
5. Test cases for concurrent requests
```

### Probabilistic Early Expiration Prompt

```
Implement probabilistic early expiration (XFetch algorithm):

**Requirements:**
- No external locks needed
- Configurable beta parameter
- Works with existing cache-aside pattern
- Language: [Python/TypeScript]

Provide:
1. Algorithm implementation
2. Beta parameter tuning guidance
3. Integration with existing caching code
4. A/B test setup to measure effectiveness
5. Monitoring for early refresh rate
```

### Stale-While-Revalidate Prompt

```
Implement stale-while-revalidate pattern:

**Requirements:**
- Serve stale data immediately
- Refresh in background
- Maximum stale time: [X minutes]
- Language: [Python/TypeScript/Go]

Implement:
1. Background refresh mechanism
2. Stale time tracking
3. Fallback when stale limit exceeded
4. Rate limiting for background refreshes
5. Metrics for stale vs fresh responses
```

---

## Performance Optimization

### Cache Performance Audit Prompt

```
Audit my caching implementation for performance issues:

**Current Metrics:**
- Hit ratio: [X%]
- Average latency: [Xms]
- Memory usage: [X GB]
- Eviction rate: [X/sec]

**Code/Config:** [paste relevant code or describe setup]

Please analyze:
1. Why is hit ratio low/high?
2. Latency bottlenecks
3. Memory optimization opportunities
4. Key design improvements
5. Serialization efficiency
6. Connection pooling issues
```

### Hot Key Detection Prompt

```
Help me identify and handle hot keys:

**Symptoms:**
- Uneven Redis cluster load
- Specific keys getting [X requests/sec]
- [Other symptoms]

**Current Setup:**
- Redis cluster with [N] nodes
- [Application details]

Help me:
1. Identify hot keys using Redis commands
2. Implement hot key detection in application
3. Design solutions (local cache, key replication, sharding)
4. Set up monitoring alerts
```

### Memory Optimization Prompt

```
Optimize Redis memory usage:

**Current State:**
- Memory used: [X GB]
- Number of keys: [X million]
- Largest key types: [strings/hashes/lists/sorted sets]
- Eviction policy: [allkeys-lru/volatile-lru/etc.]

**Goals:**
- Reduce memory by [X%]
- Maintain hit ratio above [X%]

Recommend:
1. Key structure optimization
2. Serialization improvements (MessagePack, Protobuf)
3. TTL tuning
4. Eviction policy changes
5. Data compression options
```

---

## Troubleshooting

### Cache Miss Investigation Prompt

```
Debug why cache hit ratio is low:

**Metrics:**
- Hit ratio: [X%] (target: [Y%])
- Miss patterns: [random / specific keys / time-based]
- TTL settings: [describe]
- Invalidation events: [frequency]

**Observations:**
[Describe what you've noticed]

Help me:
1. Identify root causes
2. Determine if TTL is too short
3. Check for invalidation storms
4. Analyze key distribution
5. Recommend fixes with expected impact
```

### Cache Inconsistency Debug Prompt

```
Debug data inconsistency between cache and database:

**Symptoms:**
- Users seeing stale data for [entity]
- Inconsistency window: [X seconds/minutes]
- Happens: [always / intermittently / under load]

**Architecture:**
[Describe caching setup and invalidation]

Help me:
1. Trace the data flow
2. Identify race conditions
3. Find missing invalidation paths
4. Design consistency verification
5. Recommend fixes
```

### Redis Latency Investigation Prompt

```
Investigate high Redis latency:

**Symptoms:**
- Average latency: [Xms] (normally [Yms])
- p99 latency: [Xms]
- Happens: [always / peak hours / random]

**Environment:**
- Redis version: [X]
- Deployment: [standalone/cluster/cloud managed]
- Network: [same VPC / cross-region]

Debug:
1. Redis SLOWLOG analysis
2. Network latency checks
3. Connection pool issues
4. Memory pressure indicators
5. Command analysis (expensive operations)
```

---

## Code Review Prompts

### Cache Implementation Review Prompt

```
Review this caching implementation:

```[language]
[paste code]
```

Check for:
1. Cache stampede vulnerability
2. Error handling (cache unavailable)
3. Memory leaks (unbounded growth)
4. Key collision risks
5. Serialization issues
6. TTL appropriateness
7. Logging and metrics
8. Security concerns (sensitive data)
```

### Cache Key Design Review Prompt

```
Review my cache key design:

**Keys:**
```
user:{id}
user:{id}:profile
user:{id}:preferences
product:{id}:details:{locale}
search:{query_hash}:page:{n}
```

**Questions:**
1. Is the naming convention consistent?
2. Are keys predictable for invalidation?
3. Is there risk of collision?
4. Should I version the keys?
5. Any optimization suggestions?
```

---

## Migration and Scaling

### Cache Migration Prompt

```
Plan migration from [old cache] to [new cache]:

**Current Setup:**
- Cache: [Memcached / Redis standalone / etc.]
- Data size: [X GB]
- Traffic: [X req/sec]
- Downtime tolerance: [zero / minutes / hours]

**Target:**
- New cache: [Redis Cluster / ElastiCache / etc.]
- Reasons for migration: [scalability / features / cost]

Create migration plan:
1. Preparation steps
2. Dual-write strategy
3. Traffic migration approach
4. Rollback plan
5. Validation checklist
6. Monitoring during migration
```

### Cache Scaling Prompt

```
Plan horizontal scaling for Redis cache:

**Current State:**
- Single Redis instance: [memory, CPU]
- Traffic: [X ops/sec]
- Hit ratio: [X%]

**Scaling Trigger:**
- [Expected traffic increase / memory limit / latency issues]

**Target:**
- Handle [X]x current traffic
- [Specific requirements]

Recommend:
1. Scaling approach (vertical vs horizontal)
2. Redis Cluster vs Sentinel
3. Sharding strategy
4. Data migration approach
5. Application code changes needed
6. Monitoring for new architecture
```

---

## Prompt Best Practices

### Do Include

- Specific numbers (request rates, data sizes, latencies)
- Technology stack details
- Current architecture
- Constraints (budget, downtime, consistency)
- What you've already tried
- Expected outcomes

### Do Not Include

- Sensitive credentials or keys
- Full production data
- Internal URLs or IPs
- Customer-specific details

### Follow-Up Questions

After initial response, consider asking:
- "What are the trade-offs of this approach?"
- "How would this change at 10x scale?"
- "What monitoring should I add?"
- "What are common failure modes?"
- "Show me the error handling for [specific case]"
