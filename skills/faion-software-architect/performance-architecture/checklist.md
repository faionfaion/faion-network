# Performance Architecture Checklist

Step-by-step checklist for designing and implementing high-performance systems.

---

## Phase 1: Requirements and SLOs

### 1.1 Define Performance Requirements

- [ ] Identify user-facing performance expectations
- [ ] Document peak traffic patterns (daily, weekly, seasonal)
- [ ] Estimate growth projections (6 months, 1 year, 3 years)
- [ ] Identify critical user journeys requiring low latency
- [ ] Document geographic distribution of users

### 1.2 Establish Service Level Objectives

- [ ] Define latency SLOs (p50, p95, p99)
  - [ ] API response time targets
  - [ ] Page load time targets
  - [ ] Background job completion targets
- [ ] Define throughput SLOs
  - [ ] Requests per second targets
  - [ ] Concurrent user capacity
- [ ] Define availability SLOs
  - [ ] Uptime percentage (99.9%, 99.95%, 99.99%)
  - [ ] Planned maintenance windows
- [ ] Calculate error budgets
  - [ ] Monthly error budget in minutes
  - [ ] Error budget policies (freeze deployments at 25% remaining)
- [ ] Document SLIs (Service Level Indicators) for each SLO

### 1.3 Define Capacity Requirements

- [ ] Calculate peak RPS requirements
  ```
  Peak users * requests/user/minute / 60 = RPS
  ```
- [ ] Add headroom multiplier (2x minimum, 3x recommended)
- [ ] Document storage growth rate
- [ ] Identify bandwidth requirements
- [ ] Plan for burst capacity

---

## Phase 2: Architecture Design

### 2.1 Scalability Architecture

- [ ] Design for horizontal scaling
  - [ ] Stateless application services
  - [ ] Externalized session storage
  - [ ] Shared-nothing architecture where possible
- [ ] Plan data partitioning strategy
  - [ ] Sharding key selection
  - [ ] Partition rebalancing approach
- [ ] Design auto-scaling policies
  - [ ] CPU-based scaling thresholds
  - [ ] Memory-based scaling thresholds
  - [ ] Custom metrics for scaling (queue depth, etc.)
- [ ] Document scaling limits and breakpoints

### 2.2 Caching Strategy

- [ ] Design cache hierarchy
  - [ ] Browser/client caching
  - [ ] CDN edge caching
  - [ ] Application-level caching
  - [ ] Database query caching
- [ ] Select caching patterns per use case
  - [ ] Cache-aside for read-heavy workloads
  - [ ] Write-through for consistency
  - [ ] Write-behind for write-heavy workloads
- [ ] Define cache invalidation strategy
  - [ ] TTL-based expiration
  - [ ] Event-driven invalidation
  - [ ] Version tagging
- [ ] Plan cache warming approach
- [ ] Design cache stampede prevention (request coalescing)

### 2.3 Database Performance Design

- [ ] Select appropriate database type per workload
  - [ ] OLTP: PostgreSQL, MySQL
  - [ ] OLAP: ClickHouse, BigQuery
  - [ ] Key-value: Redis, DynamoDB
  - [ ] Document: MongoDB
  - [ ] Vector: pgvector, Qdrant
- [ ] Design indexing strategy
  - [ ] Primary key design
  - [ ] Secondary indexes for query patterns
  - [ ] Composite indexes for multi-column queries
  - [ ] Partial indexes for filtered queries
- [ ] Plan connection pooling
  - [ ] Pool size calculation
  - [ ] Connection timeout settings
  - [ ] Idle connection management
- [ ] Design read replica strategy (if needed)
- [ ] Plan database sharding (if needed)

### 2.4 Async Processing Design

- [ ] Identify operations to make asynchronous
  - [ ] Long-running computations
  - [ ] External API calls
  - [ ] Email/notification sending
  - [ ] Report generation
- [ ] Select message broker
  - [ ] Kafka for event streaming
  - [ ] RabbitMQ for complex routing
  - [ ] Redis Streams for simple queues
  - [ ] Cloud queues for serverless
- [ ] Design dead letter queue handling
- [ ] Plan retry and backoff strategies
- [ ] Design idempotency for message processing

### 2.5 CDN and Edge Strategy

- [ ] Identify content for CDN caching
  - [ ] Static assets (JS, CSS, images)
  - [ ] API responses (where appropriate)
  - [ ] Dynamic content at edge
- [ ] Select CDN provider
- [ ] Configure cache headers
- [ ] Plan cache invalidation workflow
- [ ] Evaluate edge functions for
  - [ ] A/B testing
  - [ ] Geolocation routing
  - [ ] Authentication
  - [ ] Rate limiting

---

## Phase 3: Implementation

### 3.1 Application Performance

- [ ] Implement efficient algorithms
  - [ ] Profile hot paths
  - [ ] Optimize O(n^2) or worse algorithms
- [ ] Implement connection pooling
  - [ ] Database connections
  - [ ] HTTP client connections
  - [ ] Redis connections
- [ ] Implement async I/O
  - [ ] Non-blocking database calls
  - [ ] Parallel external API calls
  - [ ] Async file operations
- [ ] Implement batch processing
  - [ ] Bulk database operations
  - [ ] Batch API requests
- [ ] Minimize serialization overhead
  - [ ] Use efficient formats (Protocol Buffers, MessagePack)
  - [ ] Avoid unnecessary marshaling

### 3.2 Database Implementation

- [ ] Create necessary indexes
  ```sql
  -- Verify with EXPLAIN ANALYZE
  EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
  ```
- [ ] Optimize slow queries
  - [ ] Review EXPLAIN plans
  - [ ] Eliminate N+1 queries
  - [ ] Use appropriate JOINs
- [ ] Configure connection pooling
  - [ ] PgBouncer for PostgreSQL
  - [ ] ProxySQL for MySQL
- [ ] Set up query monitoring
  - [ ] Enable pg_stat_statements
  - [ ] Configure slow query logging
- [ ] Implement database-level caching
  - [ ] Configure shared_buffers
  - [ ] Set effective_cache_size

### 3.3 Caching Implementation

- [ ] Implement cache layer
  - [ ] Redis cluster setup
  - [ ] Memcached setup (if chosen)
- [ ] Configure eviction policies
  - [ ] LRU for general caching
  - [ ] LFU for hot data
- [ ] Implement cache-aside pattern
  ```python
  def get_user(user_id):
      cached = cache.get(f"user:{user_id}")
      if cached:
          return cached
      user = db.get_user(user_id)
      cache.set(f"user:{user_id}", user, ttl=3600)
      return user
  ```
- [ ] Implement cache invalidation
- [ ] Add cache metrics (hit rate, miss rate)

### 3.4 Load Balancing Implementation

- [ ] Configure load balancer
  - [ ] Select algorithm (round-robin, least-connections)
  - [ ] Configure health checks
  - [ ] Set up SSL termination
- [ ] Configure connection limits
- [ ] Set up session affinity (if required)
- [ ] Configure rate limiting
- [ ] Implement circuit breakers

### 3.5 CDN Implementation

- [ ] Configure CDN
  - [ ] Origin settings
  - [ ] Cache rules
  - [ ] SSL/TLS settings
- [ ] Set cache headers
  ```
  Cache-Control: public, max-age=31536000, immutable
  ```
- [ ] Configure compression (Brotli, gzip)
- [ ] Implement cache purging workflow
- [ ] Set up edge functions (if needed)

---

## Phase 4: Testing

### 4.1 Performance Testing Setup

- [ ] Set up load testing environment
  - [ ] Isolated from production
  - [ ] Production-like data volume
  - [ ] Similar infrastructure
- [ ] Create realistic test scenarios
  - [ ] User registration flow
  - [ ] Login and authentication
  - [ ] Core business workflows
  - [ ] API endpoint load
- [ ] Define acceptance criteria
  - [ ] Latency thresholds
  - [ ] Error rate thresholds
  - [ ] Throughput targets

### 4.2 Load Testing Execution

- [ ] Run smoke tests (baseline functionality)
- [ ] Run load tests (expected traffic)
  ```javascript
  // k6 example
  export const options = {
    stages: [
      { duration: '2m', target: 100 },
      { duration: '5m', target: 100 },
      { duration: '2m', target: 0 },
    ],
    thresholds: {
      http_req_duration: ['p95<300'],
      http_req_failed: ['rate<0.01'],
    },
  };
  ```
- [ ] Run stress tests (beyond expected load)
- [ ] Run spike tests (sudden traffic bursts)
- [ ] Run soak tests (sustained load for hours)

### 4.3 Performance Test Analysis

- [ ] Analyze latency distribution (p50, p95, p99)
- [ ] Identify bottlenecks
  - [ ] CPU saturation
  - [ ] Memory pressure
  - [ ] I/O bottlenecks
  - [ ] Network limits
- [ ] Review error rates under load
- [ ] Document breaking points
- [ ] Create performance baseline report

### 4.4 Profiling

- [ ] Profile application code
  - [ ] CPU profiling (flame graphs)
  - [ ] Memory profiling (heap analysis)
  - [ ] I/O profiling
- [ ] Profile database queries
  - [ ] Identify slow queries
  - [ ] Analyze execution plans
  - [ ] Check index usage
- [ ] Profile network calls
  - [ ] Identify high-latency dependencies
  - [ ] Check connection reuse
- [ ] Document optimization opportunities

---

## Phase 5: Monitoring and Observability

### 5.1 Metrics Collection

- [ ] Implement RED metrics
  - [ ] **R**ate: Request throughput
  - [ ] **E**rrors: Error rate and types
  - [ ] **D**uration: Latency percentiles
- [ ] Implement USE metrics (for resources)
  - [ ] **U**tilization: CPU, memory, disk %
  - [ ] **S**aturation: Queue depths
  - [ ] **E**rrors: Hardware/software errors
- [ ] Collect application metrics
  - [ ] Business metrics
  - [ ] Cache hit rates
  - [ ] Connection pool usage
- [ ] Collect infrastructure metrics
  - [ ] Container/VM metrics
  - [ ] Network metrics
  - [ ] Database metrics

### 5.2 Alerting Setup

- [ ] Configure SLO-based alerts
  - [ ] Fast burn: 2% budget in 1 hour (P0)
  - [ ] Medium burn: 5% budget in 6 hours (P1)
  - [ ] Slow burn: 10% budget in 3 days (P2)
- [ ] Configure resource alerts
  - [ ] CPU > 80% for 5 minutes
  - [ ] Memory > 85% for 5 minutes
  - [ ] Disk > 90%
- [ ] Configure anomaly detection (if available)
- [ ] Set up on-call rotation

### 5.3 Dashboards

- [ ] Create SLO dashboard
  - [ ] Current SLO status
  - [ ] Error budget remaining
  - [ ] Burn rate trends
- [ ] Create performance dashboard
  - [ ] Latency percentiles over time
  - [ ] Throughput trends
  - [ ] Error rate trends
- [ ] Create capacity dashboard
  - [ ] Resource utilization
  - [ ] Scaling events
  - [ ] Cost metrics
- [ ] Create database dashboard
  - [ ] Query performance
  - [ ] Connection pool status
  - [ ] Replication lag

### 5.4 Distributed Tracing

- [ ] Implement trace instrumentation
  - [ ] OpenTelemetry SDK setup
  - [ ] Span creation for key operations
  - [ ] Context propagation
- [ ] Configure trace sampling
- [ ] Set up trace visualization (Jaeger, Tempo)
- [ ] Create trace-based alerts for slow transactions

---

## Phase 6: Optimization

### 6.1 Continuous Optimization

- [ ] Establish performance review cadence (weekly/monthly)
- [ ] Review slowest endpoints weekly
- [ ] Review database slow query log weekly
- [ ] Analyze cache effectiveness monthly
- [ ] Review scaling events and costs monthly

### 6.2 Quick Wins Checklist

- [ ] Enable HTTP/2 or HTTP/3
- [ ] Enable compression (Brotli preferred)
- [ ] Add appropriate cache headers
- [ ] Enable database connection pooling
- [ ] Add missing database indexes
- [ ] Implement pagination for large datasets
- [ ] Use async for I/O-bound operations
- [ ] Batch database operations

### 6.3 Documentation

- [ ] Document performance architecture
- [ ] Document SLOs and error budgets
- [ ] Create runbooks for performance incidents
- [ ] Document scaling procedures
- [ ] Maintain capacity planning docs

---

## Checklist Summary

| Phase | Items | Critical |
|-------|-------|----------|
| 1. Requirements & SLOs | 15 | Define SLOs, calculate error budgets |
| 2. Architecture Design | 25 | Cache strategy, async design |
| 3. Implementation | 25 | Connection pooling, indexes |
| 4. Testing | 20 | Load testing, profiling |
| 5. Monitoring | 20 | SLO alerts, dashboards |
| 6. Optimization | 15 | Continuous review, quick wins |
| **Total** | **120** | |

## Quick Reference

### Performance Targets

| Metric | MVP | Growth | Enterprise |
|--------|-----|--------|------------|
| p95 latency | <500ms | <300ms | <150ms |
| Error rate | <1% | <0.1% | <0.01% |
| Availability | 99.9% | 99.95% | 99.99% |
| Cache hit rate | >80% | >90% | >95% |

### Common Issues and Solutions

| Issue | Check First | Solution |
|-------|-------------|----------|
| High latency | Database queries | Add indexes, optimize queries |
| High error rate | Error logs, dependencies | Fix bugs, add circuit breakers |
| Low throughput | Connection pools, CPU | Scale out, increase pools |
| Memory issues | Heap dumps, leaks | Fix leaks, increase limits |
| Cache misses | TTLs, keys | Adjust TTLs, warm cache |
