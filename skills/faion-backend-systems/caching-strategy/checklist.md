# Caching Strategy Checklist

Step-by-step checklist for implementing caching in backend systems.

## Phase 1: Requirements Analysis

### 1.1 Access Pattern Analysis

- [ ] Measure read vs write ratio (target: >80% reads for caching benefit)
- [ ] Identify top 10 most frequently accessed data types
- [ ] Calculate average query latency without caching
- [ ] Determine peak traffic patterns (daily/weekly)
- [ ] Analyze data update frequency per entity type

### 1.2 Cache Benefit Assessment

- [ ] Identify expensive computations (>100ms)
- [ ] Find N+1 query patterns
- [ ] Locate repeated database queries
- [ ] Calculate potential latency reduction (target: 50-90%)
- [ ] Estimate cost savings from reduced database load

### 1.3 Data Characteristics

- [ ] Categorize data by staleness tolerance
- [ ] Identify immutable data (safe to cache indefinitely)
- [ ] Document update patterns (real-time vs batch)
- [ ] Determine acceptable stale data window per entity
- [ ] List data with strict consistency requirements (no caching)

## Phase 2: Cache Layer Selection

### 2.1 L1: Application Cache

- [ ] Choose in-memory library (lru_cache, cachetools, node-cache)
- [ ] Define memory limits (recommend: <20% of total RAM)
- [ ] Set eviction policy (LRU recommended for most cases)
- [ ] Plan cache warming strategy (preload on startup if needed)
- [ ] Document process-local cache limitations (not shared)

**Decision Matrix:**

| Use Case | Recommended |
|----------|-------------|
| Static config, lookups | LRU cache, maxsize=1000 |
| Computation results | TTL cache, 5-60 min |
| User sessions | Redis (shared state) |

### 2.2 L2: Distributed Cache

- [ ] Choose distributed cache (Redis recommended)
- [ ] Plan deployment (managed vs self-hosted)
- [ ] Configure replication (1 primary + 2 replicas minimum)
- [ ] Set up eviction policy (allkeys-lru for general use)
- [ ] Plan persistence strategy (RDB + AOF for durability)

**Redis Configuration Checklist:**

- [ ] maxmemory (75% of available RAM)
- [ ] maxmemory-policy (allkeys-lru)
- [ ] save rules (900 1, 300 10, 60 10000)
- [ ] appendonly (yes for critical data)
- [ ] Enable cluster mode for >50GB data

### 2.3 L3: HTTP/CDN Cache

- [ ] Configure Cache-Control headers
- [ ] Enable CDN caching for static assets
- [ ] Set up edge caching for API responses (if applicable)
- [ ] Configure Vary headers for content negotiation
- [ ] Plan cache purge API integration

## Phase 3: Cache Key Design

### 3.1 Key Structure

- [ ] Define consistent key naming convention
- [ ] Use namespace prefixes (e.g., `user:`, `product:`)
- [ ] Include version in keys (for easy invalidation)
- [ ] Plan for parameterized queries (hash query params)
- [ ] Document key structure in codebase

**Key Naming Patterns:**

```
{entity}:{version}:{id}               # user:v1:12345
{entity}:{operation}:{params}         # search:v1:query=laptop&page=1
{entity}:tag:{tag_name}               # user:tag:premium
```

### 3.2 Key Generation

- [ ] Implement deterministic key builder
- [ ] Hash long parameters (MD5/SHA256)
- [ ] Validate key length (<250 chars for Redis)
- [ ] Plan for complex query caching
- [ ] Test key uniqueness

## Phase 4: Caching Pattern Selection

### 4.1 Cache-Aside (Lazy Loading)

**Use when:** Read-heavy, data can be stale, cache misses acceptable

- [ ] Implement read-through logic (check cache → miss → fetch → populate)
- [ ] Add TTL to all keys (prevent memory overflow)
- [ ] Handle cache miss gracefully (fallback to DB)
- [ ] Log cache hit/miss rates
- [ ] Plan for cache stampede mitigation

### 4.2 Write-Through

**Use when:** Strong consistency required, writes can tolerate latency

- [ ] Write to cache and DB in same transaction
- [ ] Implement rollback logic (if DB write fails, invalidate cache)
- [ ] Set appropriate TTL
- [ ] Log write failures
- [ ] Monitor write latency (should be <2x uncached)

### 4.3 Write-Behind (Write-Back)

**Use when:** High write throughput, eventual consistency acceptable

- [ ] Queue writes asynchronously
- [ ] Implement flush interval (5-60 seconds)
- [ ] Handle queue overflow (persist to disk)
- [ ] Plan for crash recovery (persistent queue)
- [ ] Monitor queue depth

### 4.4 Refresh-Ahead

**Use when:** Predictable access patterns, zero cache misses required

- [ ] Identify frequently accessed keys
- [ ] Implement background refresh (before TTL expires)
- [ ] Set refresh trigger (e.g., 80% of TTL)
- [ ] Monitor refresh success rate
- [ ] Plan for refresh failures (fallback to cache-aside)

## Phase 5: TTL Strategy

### 5.1 TTL Selection

- [ ] Set default TTL (recommend: 5-60 minutes)
- [ ] Define per-entity TTL based on update frequency
- [ ] Use shorter TTL for critical data (<5 min)
- [ ] Use longer TTL for static data (1-24 hours)
- [ ] Document TTL values in code

**TTL Guidelines:**

| Data Type | Recommended TTL |
|-----------|----------------|
| User profile | 30 minutes |
| Product catalog | 1 hour |
| Static config | 24 hours |
| Search results | 5 minutes |
| Analytics | 15 minutes |

### 5.2 Dynamic TTL

- [ ] Implement variable TTL based on access patterns
- [ ] Shorten TTL during deployments
- [ ] Extend TTL for rarely-changing data
- [ ] Monitor TTL effectiveness
- [ ] Plan for TTL override API (manual refresh)

## Phase 6: Cache Invalidation

### 6.1 Time-Based Invalidation

- [ ] Set TTL on all keys (mandatory)
- [ ] Use EXPIRE command for dynamic TTL
- [ ] Monitor key expiration events
- [ ] Plan for expired key cleanup
- [ ] Test TTL enforcement

### 6.2 Event-Based Invalidation

- [ ] Identify write events that invalidate cache
- [ ] Implement invalidation hooks (on update/delete)
- [ ] Use pattern-based deletion (e.g., `user:*`)
- [ ] Plan for cascading invalidation (related entities)
- [ ] Log invalidation events

### 6.3 Tag-Based Invalidation

- [ ] Define tags for related entities
- [ ] Maintain tag → keys mapping (Redis SET)
- [ ] Implement invalidate-by-tag function
- [ ] Set TTL on tag sets (same as entity TTL)
- [ ] Test tag invalidation

**Example Tags:**

```
tag:category:electronics  → [product:1, product:5, product:9]
tag:user:premium          → [user:12, user:45, user:78]
```

### 6.4 Version-Based Invalidation

- [ ] Include version in cache keys
- [ ] Increment version on schema changes
- [ ] Store version in application config
- [ ] Plan for gradual rollover (old keys expire naturally)
- [ ] Monitor version distribution

## Phase 7: Cache Stampede Prevention

### 7.1 Locking Strategy

- [ ] Implement distributed lock (Redis SETNX)
- [ ] Set lock timeout (3-10 seconds)
- [ ] Queue waiting requests (don't retry immediately)
- [ ] Return stale data while refreshing (if acceptable)
- [ ] Monitor lock acquisition failures

### 7.2 Probabilistic Early Expiration

- [ ] Refresh key before TTL expires (last 10-20% of TTL)
- [ ] Use random jitter (prevent synchronized refreshes)
- [ ] Implement background refresh worker
- [ ] Monitor refresh rate
- [ ] Test under high concurrency

### 7.3 Request Coalescing

- [ ] Group concurrent identical requests
- [ ] Use in-flight request tracking
- [ ] Share result with all waiting clients
- [ ] Set timeout for coalescing (100-500ms)
- [ ] Monitor coalescing effectiveness

## Phase 8: Monitoring and Observability

### 8.1 Metrics

- [ ] Track cache hit rate (target: >80% for cacheable data)
- [ ] Monitor cache miss rate
- [ ] Measure latency (cache hit vs miss)
- [ ] Track memory usage (stay below 80% of maxmemory)
- [ ] Monitor eviction count (should be low)
- [ ] Track key count by namespace
- [ ] Measure TTL distribution

### 8.2 Logging

- [ ] Log cache operations (hit/miss/set/delete)
- [ ] Log invalidation events with reason
- [ ] Track cache errors (connection failures, timeouts)
- [ ] Log slow cache operations (>50ms)
- [ ] Sample logs (don't log every hit)

### 8.3 Alerting

- [ ] Alert on hit rate drop (below 60%)
- [ ] Alert on high eviction rate (>10% keys/hour)
- [ ] Alert on cache service unavailability
- [ ] Alert on memory usage >90%
- [ ] Alert on latency spike (p95 >100ms)

## Phase 9: Error Handling

### 9.1 Cache Failures

- [ ] Implement graceful degradation (continue without cache)
- [ ] Add circuit breaker for repeated failures
- [ ] Set timeout for cache operations (50-200ms)
- [ ] Log failures with context
- [ ] Monitor fallback frequency

### 9.2 Connection Management

- [ ] Use connection pooling (min: 10, max: 50)
- [ ] Set connection timeout (3-5 seconds)
- [ ] Implement retry logic (max 2 retries)
- [ ] Add exponential backoff
- [ ] Monitor connection pool health

### 9.3 Data Consistency

- [ ] Validate cached data structure (before deserialization)
- [ ] Handle schema changes (version mismatch)
- [ ] Implement cache health check endpoint
- [ ] Plan for cache flush (emergency invalidation)
- [ ] Test inconsistency scenarios

## Phase 10: Performance Optimization

### 10.1 Serialization

- [ ] Choose efficient serialization (MessagePack > JSON)
- [ ] Compress large values (>1KB, use gzip/lz4)
- [ ] Benchmark serialization overhead
- [ ] Monitor value size distribution
- [ ] Test deserialization performance

### 10.2 Memory Optimization

- [ ] Set maxmemory policy (allkeys-lru recommended)
- [ ] Monitor memory fragmentation
- [ ] Use Redis MEMORY DOCTOR command
- [ ] Plan for key compaction
- [ ] Test eviction behavior under load

### 10.3 Network Optimization

- [ ] Use pipelining for batch operations
- [ ] Implement MGET for multiple keys
- [ ] Co-locate cache and application (same region)
- [ ] Use Unix socket for local Redis
- [ ] Monitor network latency

## Phase 11: Testing

### 11.1 Unit Tests

- [ ] Test cache hit scenario
- [ ] Test cache miss scenario
- [ ] Test invalidation logic
- [ ] Test TTL expiration
- [ ] Test error handling (cache unavailable)

### 11.2 Integration Tests

- [ ] Test cache-aside pattern end-to-end
- [ ] Test write-through consistency
- [ ] Test stampede prevention
- [ ] Test concurrent access
- [ ] Test cache warming

### 11.3 Load Testing

- [ ] Benchmark cache hit latency (target: <10ms)
- [ ] Test throughput (target: >10k ops/sec)
- [ ] Test under cache miss load
- [ ] Simulate stampede scenario
- [ ] Monitor resource usage under load

## Phase 12: Documentation

### 12.1 Architecture Documentation

- [ ] Document cache layers (L1, L2, L3)
- [ ] Diagram cache flow (cache-aside/write-through)
- [ ] List cached entities with TTL
- [ ] Document invalidation strategy
- [ ] Create runbook for common issues

### 12.2 Code Documentation

- [ ] Add JSDoc/docstrings for cache functions
- [ ] Document cache key structure
- [ ] Explain TTL values (why chosen)
- [ ] Document error handling
- [ ] Add examples for common use cases

## Quick Reference: Common Configurations

### Cache Hit Rate Targets

| Scenario | Target Hit Rate |
|----------|----------------|
| User profiles | 90%+ |
| Product catalog | 85%+ |
| Search results | 70%+ |
| Session data | 95%+ |
| API responses | 60-80% |

### TTL Guidelines

| Update Frequency | Recommended TTL |
|-----------------|----------------|
| Static (never) | 24 hours |
| Rare (<1/day) | 1-4 hours |
| Occasional (hourly) | 15-30 minutes |
| Frequent (every 5 min) | 1-5 minutes |
| Real-time | Don't cache or <1 min |

### Redis Memory Limits

| Data Size | Recommended Instance |
|-----------|---------------------|
| <5GB | 8GB RAM instance |
| 5-20GB | 32GB RAM instance |
| 20-100GB | Cluster (3+ nodes) |
| >100GB | Cluster + partitioning |

## Checklist Summary

| Phase | Items | Critical |
|-------|-------|----------|
| Requirements | 13 | 8 |
| Layer Selection | 15 | 10 |
| Key Design | 10 | 8 |
| Pattern Selection | 18 | 12 |
| TTL Strategy | 10 | 8 |
| Invalidation | 19 | 15 |
| Stampede Prevention | 13 | 8 |
| Monitoring | 17 | 12 |
| Error Handling | 13 | 10 |
| Performance | 14 | 8 |
| Testing | 12 | 8 |
| Documentation | 10 | 6 |
| **Total** | **164** | **113** |
