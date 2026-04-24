# Performance Architecture Examples

Real-world performance optimization examples across different domains and scales.

---

## Example 1: E-Commerce Platform Optimization

### Context

**Company:** Mid-size e-commerce platform
**Scale:** 500K daily active users, 50K orders/day
**Problem:** Black Friday preparation - need to handle 10x normal traffic
**Stack:** Python/Django, PostgreSQL, Redis, Nginx

### Initial State

| Metric | Value | Target |
|--------|-------|--------|
| p95 latency | 1.2s | <300ms |
| Throughput | 500 RPS | 5,000 RPS |
| Error rate | 2% | <0.1% |
| DB connections | 200 (maxed out) | Scalable |

### Optimization 1: Database Performance

**Problem:** Product listing queries taking 800ms

```sql
-- Before: Slow query (800ms)
SELECT p.*, c.name as category_name,
       (SELECT COUNT(*) FROM reviews r WHERE r.product_id = p.id) as review_count,
       (SELECT AVG(rating) FROM reviews r WHERE r.product_id = p.id) as avg_rating
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = true
  AND p.category_id IN (SELECT id FROM categories WHERE parent_id = 5)
ORDER BY p.created_at DESC
LIMIT 20;

-- After: Optimized query (15ms)
-- Step 1: Add materialized columns
ALTER TABLE products ADD COLUMN review_count INTEGER DEFAULT 0;
ALTER TABLE products ADD COLUMN avg_rating DECIMAL(3,2) DEFAULT 0;

-- Step 2: Create composite index
CREATE INDEX idx_products_active_category_created
ON products(is_active, category_id, created_at DESC)
WHERE is_active = true;

-- Step 3: Simplified query
SELECT p.id, p.name, p.price, p.review_count, p.avg_rating, c.name as category_name
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = true
  AND p.category_id IN (5, 12, 13, 14)  -- Pre-resolved category IDs
ORDER BY p.created_at DESC
LIMIT 20;
```

**Result:** Query time reduced from 800ms to 15ms (53x improvement)

### Optimization 2: Caching Strategy

**Implementation:**

```python
# cache_service.py
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='redis-cluster', port=6379, decode_responses=True)

def cache_product_listing(category_id: int, page: int = 1) -> list:
    cache_key = f"products:category:{category_id}:page:{page}"

    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from DB
    products = fetch_products_from_db(category_id, page)

    # Cache with 5 minute TTL
    redis_client.setex(cache_key, 300, json.dumps(products))

    return products

def invalidate_category_cache(category_id: int):
    """Invalidate all pages for a category"""
    pattern = f"products:category:{category_id}:*"
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)

# Prevent cache stampede with locking
def cache_with_lock(cache_key: str, ttl: int, fetch_func):
    lock_key = f"lock:{cache_key}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Try to acquire lock
    if redis_client.set(lock_key, "1", nx=True, ex=10):
        try:
            data = fetch_func()
            redis_client.setex(cache_key, ttl, json.dumps(data))
            return data
        finally:
            redis_client.delete(lock_key)
    else:
        # Wait for other process to populate cache
        import time
        for _ in range(50):  # 5 seconds max
            time.sleep(0.1)
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        # Fallback to DB if cache not populated
        return fetch_func()
```

**Cache Configuration:**

| Data Type | TTL | Invalidation |
|-----------|-----|--------------|
| Product listings | 5 min | On product update |
| Product details | 15 min | On product update |
| User sessions | 24 hours | On logout |
| Cart data | 7 days | On checkout |

### Optimization 3: Connection Pooling

**Before:** Django default (new connection per request)

**After:** PgBouncer with connection pooling

```ini
# pgbouncer.ini
[databases]
ecommerce = host=postgres-primary port=5432 dbname=ecommerce

[pgbouncer]
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

pool_mode = transaction
max_client_conn = 1000
default_pool_size = 50
min_pool_size = 10
reserve_pool_size = 5
reserve_pool_timeout = 3

# Performance tuning
server_idle_timeout = 600
server_lifetime = 3600
server_connect_timeout = 15
query_timeout = 300
```

**Result:** Supported 10x more concurrent users with same DB resources

### Optimization 4: Async Order Processing

**Before:** Synchronous order processing (2-5 seconds)

**After:** Async with Celery + RabbitMQ

```python
# tasks.py
from celery import Celery

app = Celery('ecommerce', broker='amqp://rabbitmq:5672')

@app.task(bind=True, max_retries=3)
def process_order(self, order_id: int):
    """Process order asynchronously"""
    try:
        order = Order.objects.get(id=order_id)

        # These happen in parallel in worker
        update_inventory(order)
        send_confirmation_email(order)
        notify_warehouse(order)
        update_analytics(order)

        order.status = 'processing'
        order.save()

    except Exception as exc:
        self.retry(exc=exc, countdown=60)

# views.py
def create_order(request):
    order = Order.objects.create(
        user=request.user,
        status='pending',
        **order_data
    )

    # Queue async processing
    process_order.delay(order.id)

    # Return immediately
    return JsonResponse({
        'order_id': order.id,
        'status': 'pending',
        'message': 'Order received, processing...'
    }, status=202)
```

### Final Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| p95 latency | 1.2s | 180ms | 6.7x |
| Throughput | 500 RPS | 6,000 RPS | 12x |
| Error rate | 2% | 0.05% | 40x |
| DB connections | 200 | 50 (pooled) | 4x efficiency |

**Black Friday Result:** Handled 8x normal traffic with no degradation

---

## Example 2: Real-Time Analytics Dashboard

### Context

**Company:** SaaS analytics platform
**Scale:** 10M events/day, 1000 concurrent dashboard users
**Problem:** Dashboard queries timing out, high infrastructure costs
**Stack:** Node.js, PostgreSQL, ClickHouse, Redis

### Initial State

PostgreSQL struggling with time-series analytics queries:

```sql
-- Query taking 45 seconds
SELECT
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as events,
    COUNT(DISTINCT user_id) as unique_users,
    AVG(duration_ms) as avg_duration
FROM events
WHERE tenant_id = 123
  AND created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('hour', created_at)
ORDER BY hour;
```

### Solution: ClickHouse for Analytics

**Step 1: Data Pipeline with Kafka**

```yaml
# docker-compose.yml (partial)
services:
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'

  clickhouse:
    image: clickhouse/clickhouse-server:23.8
    volumes:
      - ./clickhouse/config.xml:/etc/clickhouse-server/config.xml
      - clickhouse_data:/var/lib/clickhouse
```

**Step 2: ClickHouse Schema**

```sql
-- ClickHouse table for events
CREATE TABLE events (
    tenant_id UInt32,
    event_type LowCardinality(String),
    user_id UInt64,
    session_id String,
    created_at DateTime,
    duration_ms UInt32,
    properties String  -- JSON
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_at)
ORDER BY (tenant_id, created_at, event_type)
TTL created_at + INTERVAL 90 DAY;

-- Materialized view for hourly aggregates
CREATE MATERIALIZED VIEW events_hourly_mv
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (tenant_id, hour, event_type)
AS SELECT
    tenant_id,
    event_type,
    toStartOfHour(created_at) as hour,
    count() as event_count,
    uniqState(user_id) as unique_users_state,
    sumState(duration_ms) as total_duration_state,
    countState() as count_state
FROM events
GROUP BY tenant_id, event_type, hour;

-- Query using materialized view (sub-second)
SELECT
    hour,
    sum(event_count) as events,
    uniqMerge(unique_users_state) as unique_users,
    sumMerge(total_duration_state) / countMerge(count_state) as avg_duration
FROM events_hourly_mv
WHERE tenant_id = 123
  AND hour >= now() - INTERVAL 7 DAY
GROUP BY hour
ORDER BY hour;
```

**Step 3: Kafka Consumer for ClickHouse**

```javascript
// clickhouse-consumer.js
const { Kafka } = require('kafkajs');
const { ClickHouse } = require('clickhouse');

const kafka = new Kafka({
  clientId: 'analytics-consumer',
  brokers: ['kafka:9092']
});

const clickhouse = new ClickHouse({
  url: 'http://clickhouse:8123',
  basicAuth: { username: 'default', password: '' }
});

const consumer = kafka.consumer({ groupId: 'clickhouse-writers' });

async function run() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'events', fromBeginning: false });

  let batch = [];
  const BATCH_SIZE = 1000;
  const FLUSH_INTERVAL = 5000; // 5 seconds

  setInterval(async () => {
    if (batch.length > 0) {
      await flushBatch();
    }
  }, FLUSH_INTERVAL);

  await consumer.run({
    eachMessage: async ({ message }) => {
      const event = JSON.parse(message.value.toString());
      batch.push(event);

      if (batch.length >= BATCH_SIZE) {
        await flushBatch();
      }
    }
  });
}

async function flushBatch() {
  const events = batch;
  batch = [];

  const values = events.map(e => ({
    tenant_id: e.tenant_id,
    event_type: e.event_type,
    user_id: e.user_id,
    session_id: e.session_id,
    created_at: new Date(e.timestamp),
    duration_ms: e.duration_ms || 0,
    properties: JSON.stringify(e.properties || {})
  }));

  await clickhouse.insert('INSERT INTO events', values).toPromise();
  console.log(`Inserted ${values.length} events`);
}

run().catch(console.error);
```

### Results

| Metric | PostgreSQL | ClickHouse | Improvement |
|--------|------------|------------|-------------|
| 7-day aggregation | 45s | 0.3s | 150x |
| 30-day aggregation | Timeout | 1.2s | - |
| Storage (1 month) | 500GB | 50GB | 10x compression |
| Query cost | High | Low | 80% reduction |

---

## Example 3: API Gateway Performance

### Context

**Company:** Fintech API provider
**Scale:** 100M API calls/day, strict SLAs (p99 < 100ms)
**Problem:** Variable latency, some requests exceeding SLA
**Stack:** Go, PostgreSQL, Redis, Kubernetes

### Initial State

| Percentile | Latency | SLA |
|------------|---------|-----|
| p50 | 25ms | - |
| p95 | 150ms | <200ms |
| p99 | 800ms | <100ms (FAILING) |

### Root Cause Analysis

Using distributed tracing (Jaeger), identified issues:

1. Cold database connections (15% of requests)
2. Rate limiting check hitting Redis synchronously
3. JSON serialization overhead
4. Garbage collection pauses

### Solution 1: Connection Pool Warming

```go
// pool.go
package db

import (
    "context"
    "database/sql"
    "time"

    _ "github.com/lib/pq"
)

type Pool struct {
    db *sql.DB
}

func NewPool(dsn string, maxConns int) (*Pool, error) {
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        return nil, err
    }

    db.SetMaxOpenConns(maxConns)
    db.SetMaxIdleConns(maxConns)
    db.SetConnMaxLifetime(30 * time.Minute)
    db.SetConnMaxIdleTime(10 * time.Minute)

    pool := &Pool{db: db}

    // Warm the pool
    if err := pool.warmConnections(maxConns); err != nil {
        return nil, err
    }

    return pool, nil
}

func (p *Pool) warmConnections(count int) error {
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    conns := make([]*sql.Conn, count)

    // Acquire all connections
    for i := 0; i < count; i++ {
        conn, err := p.db.Conn(ctx)
        if err != nil {
            return err
        }
        // Ping to ensure connection is established
        if err := conn.PingContext(ctx); err != nil {
            return err
        }
        conns[i] = conn
    }

    // Release connections back to pool
    for _, conn := range conns {
        conn.Close()
    }

    return nil
}
```

### Solution 2: Async Rate Limiting

```go
// ratelimit.go
package ratelimit

import (
    "context"
    "sync"
    "time"

    "github.com/redis/go-redis/v9"
)

type AsyncRateLimiter struct {
    redis       *redis.Client
    localCache  sync.Map
    updateChan  chan updateRequest
}

type updateRequest struct {
    key   string
    count int64
}

func NewAsyncRateLimiter(redisClient *redis.Client) *AsyncRateLimiter {
    rl := &AsyncRateLimiter{
        redis:      redisClient,
        updateChan: make(chan updateRequest, 10000),
    }

    // Background worker for Redis updates
    go rl.backgroundUpdater()

    return rl
}

func (rl *AsyncRateLimiter) Allow(ctx context.Context, key string, limit int64) bool {
    // Check local cache first (fast path)
    if val, ok := rl.localCache.Load(key); ok {
        count := val.(*int64)
        if *count >= limit {
            return false
        }
        // Increment locally, update Redis async
        newCount := atomic.AddInt64(count, 1)
        rl.updateChan <- updateRequest{key: key, count: 1}
        return newCount <= limit
    }

    // Cache miss - fetch from Redis (slow path)
    count, err := rl.redis.Get(ctx, key).Int64()
    if err != nil && err != redis.Nil {
        // On error, allow (fail open)
        return true
    }

    if count >= limit {
        return false
    }

    // Store in local cache
    newCount := count + 1
    rl.localCache.Store(key, &newCount)
    rl.updateChan <- updateRequest{key: key, count: 1}

    return true
}

func (rl *AsyncRateLimiter) backgroundUpdater() {
    batch := make(map[string]int64)
    ticker := time.NewTicker(100 * time.Millisecond)

    for {
        select {
        case req := <-rl.updateChan:
            batch[req.key] += req.count

        case <-ticker.C:
            if len(batch) > 0 {
                rl.flushBatch(batch)
                batch = make(map[string]int64)
            }
        }
    }
}

func (rl *AsyncRateLimiter) flushBatch(batch map[string]int64) {
    ctx := context.Background()
    pipe := rl.redis.Pipeline()

    for key, count := range batch {
        pipe.IncrBy(ctx, key, count)
    }

    pipe.Exec(ctx)
}
```

### Solution 3: Optimized JSON Handling

```go
// serialization.go
package api

import (
    "sync"

    jsoniter "github.com/json-iterator/go"
)

var json = jsoniter.ConfigCompatibleWithStandardLibrary

// Response pool to reduce allocations
var responsePool = sync.Pool{
    New: func() interface{} {
        return &Response{
            Data: make(map[string]interface{}, 10),
        }
    },
}

type Response struct {
    Success bool                   `json:"success"`
    Data    map[string]interface{} `json:"data,omitempty"`
    Error   string                 `json:"error,omitempty"`
}

func GetResponse() *Response {
    resp := responsePool.Get().(*Response)
    resp.Success = false
    resp.Error = ""
    for k := range resp.Data {
        delete(resp.Data, k)
    }
    return resp
}

func PutResponse(resp *Response) {
    responsePool.Put(resp)
}

// Handler example
func HandleRequest(w http.ResponseWriter, r *http.Request) {
    resp := GetResponse()
    defer PutResponse(resp)

    // Process request...
    resp.Success = true
    resp.Data["result"] = processResult

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}
```

### Solution 4: GC Tuning

```go
// main.go
package main

import (
    "runtime"
    "runtime/debug"
)

func init() {
    // Reduce GC frequency for lower latency
    debug.SetGCPercent(200)

    // Set memory limit to prevent OOM
    debug.SetMemoryLimit(4 * 1024 * 1024 * 1024) // 4GB

    // Use all available CPUs
    runtime.GOMAXPROCS(runtime.NumCPU())
}
```

### Final Results

| Percentile | Before | After | SLA |
|------------|--------|-------|-----|
| p50 | 25ms | 12ms | - |
| p95 | 150ms | 45ms | <200ms |
| p99 | 800ms | 85ms | <100ms |

**Improvements:**
- p99 latency reduced 9.4x
- Connection pool warming eliminated cold start latency
- Async rate limiting removed 50ms from hot path
- JSON optimization reduced 5ms per request
- GC tuning eliminated latency spikes

---

## Example 4: Content Delivery Optimization

### Context

**Company:** Media streaming platform
**Scale:** 5M daily active users, 50TB content served/day
**Problem:** High origin load, global latency variations
**Stack:** Next.js, AWS CloudFront, S3, Lambda@Edge

### Multi-Layer Caching Strategy

**Layer 1: Browser Cache**

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/api/content/:id',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, s-maxage=300, stale-while-revalidate=600',
          },
        ],
      },
    ];
  },
};
```

**Layer 2: CDN with Lambda@Edge**

```javascript
// lambda-edge/viewer-request.js
exports.handler = async (event) => {
    const request = event.Records[0].cf.request;
    const headers = request.headers;

    // Geo-based routing
    const country = headers['cloudfront-viewer-country']?.[0]?.value || 'US';

    // Route to regional origin
    const regionMapping = {
        'US': 'us-east-1',
        'CA': 'us-east-1',
        'GB': 'eu-west-1',
        'DE': 'eu-west-1',
        'JP': 'ap-northeast-1',
        'AU': 'ap-southeast-2',
    };

    const region = regionMapping[country] || 'us-east-1';
    request.origin.custom.domainName = `origin-${region}.example.com`;

    // Add user segment for A/B testing
    const userId = headers['x-user-id']?.[0]?.value || 'anonymous';
    const segment = parseInt(userId, 16) % 100 < 10 ? 'beta' : 'stable';
    request.headers['x-segment'] = [{ key: 'X-Segment', value: segment }];

    return request;
};
```

**Layer 3: Origin Shield**

```yaml
# CloudFormation for CloudFront with Origin Shield
Resources:
  Distribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: MediaOrigin
            DomainName: !Sub '${MediaBucket}.s3.${AWS::Region}.amazonaws.com'
            S3OriginConfig:
              OriginAccessIdentity: !Sub 'origin-access-identity/cloudfront/${OAI}'
            OriginShield:
              Enabled: true
              OriginShieldRegion: us-east-1  # Single cache layer
        CacheBehaviors:
          - PathPattern: '/media/*'
            TargetOriginId: MediaOrigin
            ViewerProtocolPolicy: redirect-to-https
            CachePolicyId: !Ref MediaCachePolicy
            Compress: true

  MediaCachePolicy:
    Type: AWS::CloudFront::CachePolicy
    Properties:
      CachePolicyConfig:
        Name: MediaCachePolicy
        DefaultTTL: 86400    # 1 day
        MaxTTL: 31536000     # 1 year
        MinTTL: 3600         # 1 hour
        ParametersInCacheKeyAndForwardedToOrigin:
          CookiesConfig:
            CookieBehavior: none
          HeadersConfig:
            HeaderBehavior: none
          QueryStringsConfig:
            QueryStringBehavior: whitelist
            QueryStrings:
              - quality
              - format
          EnableAcceptEncodingBrotli: true
          EnableAcceptEncodingGzip: true
```

### Results

| Metric | Before | After |
|--------|--------|-------|
| Origin requests | 100M/day | 5M/day |
| CDN hit ratio | 75% | 95% |
| Global p50 latency | 250ms | 45ms |
| Bandwidth costs | $50K/month | $15K/month |

---

## Example 5: Database Scaling for High Write Throughput

### Context

**Company:** IoT platform
**Scale:** 1M devices, 10K events/second peak
**Problem:** PostgreSQL cannot handle write volume
**Stack:** Python, PostgreSQL, TimescaleDB

### Solution: TimescaleDB with Compression

**Step 1: Schema Migration**

```sql
-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create hypertable for device events
CREATE TABLE device_events (
    device_id UUID NOT NULL,
    event_time TIMESTAMPTZ NOT NULL,
    event_type TEXT NOT NULL,
    value DOUBLE PRECISION,
    metadata JSONB
);

SELECT create_hypertable(
    'device_events',
    'event_time',
    chunk_time_interval => INTERVAL '1 day'
);

-- Add compression
ALTER TABLE device_events SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'device_id',
    timescaledb.compress_orderby = 'event_time DESC'
);

-- Automatic compression policy
SELECT add_compression_policy('device_events', INTERVAL '7 days');

-- Retention policy
SELECT add_retention_policy('device_events', INTERVAL '90 days');

-- Create continuous aggregate for dashboards
CREATE MATERIALIZED VIEW device_events_hourly
WITH (timescaledb.continuous) AS
SELECT
    device_id,
    time_bucket('1 hour', event_time) AS bucket,
    event_type,
    COUNT(*) as event_count,
    AVG(value) as avg_value,
    MIN(value) as min_value,
    MAX(value) as max_value
FROM device_events
GROUP BY device_id, bucket, event_type;

-- Refresh policy for continuous aggregate
SELECT add_continuous_aggregate_policy('device_events_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');
```

**Step 2: Batch Insert Service**

```python
# batch_inserter.py
import asyncio
from asyncio import Queue
from datetime import datetime
import asyncpg
from typing import List, Dict

class BatchInserter:
    def __init__(self, dsn: str, batch_size: int = 1000, flush_interval: float = 1.0):
        self.dsn = dsn
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.queue: Queue = Queue()
        self.pool: asyncpg.Pool = None

    async def start(self):
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
        asyncio.create_task(self._flush_loop())

    async def insert(self, event: Dict):
        await self.queue.put(event)

    async def _flush_loop(self):
        while True:
            batch = []
            deadline = asyncio.get_event_loop().time() + self.flush_interval

            while len(batch) < self.batch_size:
                try:
                    timeout = deadline - asyncio.get_event_loop().time()
                    if timeout <= 0:
                        break
                    event = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=timeout
                    )
                    batch.append(event)
                except asyncio.TimeoutError:
                    break

            if batch:
                await self._insert_batch(batch)

    async def _insert_batch(self, batch: List[Dict]):
        async with self.pool.acquire() as conn:
            # Use COPY for maximum performance
            await conn.copy_records_to_table(
                'device_events',
                records=[
                    (
                        e['device_id'],
                        e['event_time'],
                        e['event_type'],
                        e['value'],
                        e.get('metadata')
                    )
                    for e in batch
                ],
                columns=['device_id', 'event_time', 'event_type', 'value', 'metadata']
            )

# Usage
inserter = BatchInserter(
    dsn='postgresql://user:pass@localhost/iot',
    batch_size=5000,
    flush_interval=0.5
)
await inserter.start()

# Insert events (non-blocking)
await inserter.insert({
    'device_id': '550e8400-e29b-41d4-a716-446655440000',
    'event_time': datetime.utcnow(),
    'event_type': 'temperature',
    'value': 23.5,
    'metadata': {'unit': 'celsius'}
})
```

### Results

| Metric | PostgreSQL | TimescaleDB |
|--------|------------|-------------|
| Write throughput | 2K/s | 50K/s |
| Storage (30 days) | 500GB | 50GB |
| Query (1 day agg) | 30s | 0.5s |
| Query (90 day agg) | Timeout | 3s |

---

## Key Takeaways

| Optimization | Impact | Complexity |
|--------------|--------|------------|
| Database indexing | 10-100x query speed | Low |
| Caching | 5-50x latency reduction | Medium |
| Connection pooling | 2-10x throughput | Low |
| Async processing | 5-20x perceived latency | Medium |
| CDN | 3-10x global latency | Low |
| Specialized databases | 10-100x for specific workloads | High |
| Code optimization | 1.5-5x CPU efficiency | Medium |

**Order of Optimization:**
1. Measure first (profiling, APM)
2. Fix N+1 queries and missing indexes
3. Add caching
4. Implement async for slow operations
5. Scale infrastructure
6. Consider specialized technologies
