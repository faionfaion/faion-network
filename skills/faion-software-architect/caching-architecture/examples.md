# Caching Architecture Examples

Real-world case studies and implementation examples for various caching scenarios.

## Case Study 1: E-Commerce Platform

### Context
- 500K daily active users
- 10M product catalog
- 50K orders/day
- Peak traffic: 10x normal during sales

### Caching Architecture

```
           Cloudflare CDN
                 |
           +-----------+
           |  nginx    |  (Page cache, rate limiting)
           +-----------+
                 |
    +------------+------------+
    |            |            |
+-------+   +-------+    +-------+
| API-1 |   | API-2 |    | API-3 |
+-------+   +-------+    +-------+
    |            |            |
    +------------+------------+
                 |
         +--------------+
         | Redis Cluster|  (6 nodes, 3 masters + 3 replicas)
         +--------------+
                 |
         +--------------+
         |  PostgreSQL  |  (Primary + 2 read replicas)
         +--------------+
```

### Caching Strategies by Data Type

| Data Type | Pattern | TTL | Invalidation | Redis Structure |
|-----------|---------|-----|--------------|-----------------|
| Product catalog | Cache-Aside | 15 min | Event on update | Hash |
| Product inventory | Write-Through | 30 sec | Immediate | String |
| User sessions | Read-Through | 24h | On logout | Hash |
| Shopping cart | Write-Through | 7 days | On checkout | Hash |
| Search results | Cache-Aside | 5 min | TTL only | Sorted Set |
| Recommendations | Cache-Aside | 1h | Nightly refresh | List |

### Implementation: Product Catalog

```python
# Python/FastAPI implementation

from redis import Redis
from fastapi import FastAPI, Depends
import json
from typing import Optional

app = FastAPI()
redis = Redis(host='redis-cluster', port=6379, decode_responses=True)

PRODUCT_TTL = 900  # 15 minutes

def get_product(product_id: str) -> Optional[dict]:
    """Cache-aside pattern for product data."""
    cache_key = f"product:{product_id}:v2"

    # 1. Try cache first
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2. Cache miss - fetch from database
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    product_data = product.to_dict()

    # 3. Store in cache
    redis.setex(cache_key, PRODUCT_TTL, json.dumps(product_data))

    return product_data

def update_product(product_id: str, data: dict) -> dict:
    """Update with cache invalidation."""
    # 1. Update database
    product = db.query(Product).filter(Product.id == product_id).first()
    for key, value in data.items():
        setattr(product, key, value)
    db.commit()

    # 2. Invalidate cache
    redis.delete(f"product:{product_id}:v2")

    # 3. Publish event for distributed invalidation
    redis.publish("product:updates", json.dumps({
        "action": "invalidate",
        "product_id": product_id
    }))

    return product.to_dict()
```

### Implementation: Inventory (Write-Through)

```python
class InventoryService:
    def __init__(self, redis: Redis, db):
        self.redis = redis
        self.db = db

    def get_stock(self, product_id: str) -> int:
        """Get current stock level."""
        cache_key = f"inventory:{product_id}"

        stock = self.redis.get(cache_key)
        if stock is not None:
            return int(stock)

        # Cache miss - load from DB
        inventory = self.db.query(Inventory).filter(
            Inventory.product_id == product_id
        ).first()

        stock = inventory.quantity if inventory else 0
        self.redis.setex(cache_key, 30, stock)

        return stock

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """Atomic stock reservation with write-through."""
        cache_key = f"inventory:{product_id}"
        lock_key = f"lock:inventory:{product_id}"

        # Acquire distributed lock
        if not self.redis.set(lock_key, "1", nx=True, ex=5):
            raise ConcurrencyError("Could not acquire lock")

        try:
            # Check and update in single transaction
            current = self.get_stock(product_id)
            if current < quantity:
                return False

            new_stock = current - quantity

            # Update database first
            self.db.query(Inventory).filter(
                Inventory.product_id == product_id
            ).update({"quantity": new_stock})
            self.db.commit()

            # Update cache (write-through)
            self.redis.setex(cache_key, 30, new_stock)

            return True
        finally:
            self.redis.delete(lock_key)
```

### Results
- Cache hit ratio: 94%
- Average response time: 45ms (down from 320ms)
- Database load: 80% reduction
- Handled 10x traffic during Black Friday

---

## Case Study 2: Social Media Feed

### Context
- 10M users
- 1B posts
- Real-time feed updates
- Global distribution

### Architecture

```
                    Cloudflare Workers
                    (Edge computation)
                           |
              +------------+------------+
              |            |            |
         US-East       EU-West      Asia-Pac
              |            |            |
         +--------+   +--------+   +--------+
         | Redis  |   | Redis  |   | Redis  |
         | Cluster|   | Cluster|   | Cluster|
         +--------+   +--------+   +--------+
              |            |            |
              +------------+------------+
                           |
                    +-----------+
                    | Cassandra |
                    | (Global)  |
                    +-----------+
```

### Feed Generation Strategy

**Push Model (Fan-out on Write):**
```python
class FeedService:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.FEED_SIZE = 100
        self.FEED_TTL = 86400  # 24 hours

    def on_new_post(self, user_id: str, post: dict):
        """Fan-out new post to followers' feeds."""
        followers = self.get_followers(user_id)

        # Fan-out to active users only (< 10K followers)
        if len(followers) < 10000:
            pipe = self.redis.pipeline()
            for follower_id in followers:
                feed_key = f"feed:{follower_id}"
                pipe.lpush(feed_key, json.dumps(post))
                pipe.ltrim(feed_key, 0, self.FEED_SIZE - 1)
                pipe.expire(feed_key, self.FEED_TTL)
            pipe.execute()
        else:
            # For celebrities, use pull model
            self.redis.lpush(f"posts:{user_id}", json.dumps(post))

    def get_feed(self, user_id: str, page: int = 0, size: int = 20) -> list:
        """Get user's feed with hybrid approach."""
        feed_key = f"feed:{user_id}"

        # Get cached feed
        start = page * size
        end = start + size - 1

        cached_feed = self.redis.lrange(feed_key, start, end)

        if cached_feed:
            return [json.loads(post) for post in cached_feed]

        # Cache miss - rebuild feed
        return self.rebuild_feed(user_id)

    def rebuild_feed(self, user_id: str) -> list:
        """Rebuild feed from followed users (pull model)."""
        following = self.get_following(user_id)

        # Get recent posts from each followed user
        pipe = self.redis.pipeline()
        for followed_id in following[:100]:  # Limit for performance
            pipe.lrange(f"posts:{followed_id}", 0, 10)

        results = pipe.execute()

        # Merge and sort by timestamp
        all_posts = []
        for posts in results:
            all_posts.extend([json.loads(p) for p in posts])

        all_posts.sort(key=lambda x: x['timestamp'], reverse=True)
        feed = all_posts[:100]

        # Cache the feed
        feed_key = f"feed:{user_id}"
        pipe = self.redis.pipeline()
        for post in feed:
            pipe.rpush(feed_key, json.dumps(post))
        pipe.expire(feed_key, self.FEED_TTL)
        pipe.execute()

        return feed[:20]
```

### Hot Key Mitigation

```python
class HotKeyHandler:
    """Handle celebrity posts that would cause hot keys."""

    def __init__(self, redis: Redis):
        self.redis = redis
        self.LOCAL_CACHE = {}  # In-memory cache
        self.LOCAL_TTL = 5  # 5 seconds

    def get_viral_post(self, post_id: str) -> dict:
        """Get viral post with local + distributed caching."""
        # Level 1: Local in-memory cache
        local_key = f"local:{post_id}"
        if local_key in self.LOCAL_CACHE:
            entry = self.LOCAL_CACHE[local_key]
            if time.time() < entry['expires']:
                return entry['data']

        # Level 2: Distributed cache with replicated keys
        # Use random suffix to spread load
        replica = random.randint(0, 4)
        cache_key = f"viral:{post_id}:r{replica}"

        cached = self.redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            # Update local cache
            self.LOCAL_CACHE[local_key] = {
                'data': data,
                'expires': time.time() + self.LOCAL_TTL
            }
            return data

        # Cache miss - fetch and populate all replicas
        post = self.fetch_from_db(post_id)

        pipe = self.redis.pipeline()
        for i in range(5):
            pipe.setex(f"viral:{post_id}:r{i}", 60, json.dumps(post))
        pipe.execute()

        return post
```

### Results
- Feed load time: <100ms globally
- Handled 100K concurrent users
- Celebrity posts (100M+ followers) served without issues

---

## Case Study 3: SaaS API with Rate Limiting

### Context
- Multi-tenant SaaS platform
- API rate limiting per tenant
- Real-time usage tracking
- Metered billing

### Architecture

```python
class RateLimiter:
    """Sliding window rate limiter with Redis."""

    def __init__(self, redis: Redis):
        self.redis = redis

    def is_allowed(
        self,
        tenant_id: str,
        endpoint: str,
        limit: int = 100,
        window_seconds: int = 60
    ) -> tuple[bool, dict]:
        """Check if request is allowed under rate limit."""
        key = f"ratelimit:{tenant_id}:{endpoint}"
        now = time.time()
        window_start = now - window_seconds

        pipe = self.redis.pipeline()

        # Remove old entries outside window
        pipe.zremrangebyscore(key, 0, window_start)

        # Count current requests in window
        pipe.zcard(key)

        # Add current request
        pipe.zadd(key, {f"{now}:{uuid.uuid4()}": now})

        # Set expiry on key
        pipe.expire(key, window_seconds + 1)

        results = pipe.execute()
        current_count = results[1]

        remaining = max(0, limit - current_count - 1)
        reset_time = int(now + window_seconds)

        headers = {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset_time)
        }

        return current_count < limit, headers


class UsageTracker:
    """Track API usage for billing."""

    def __init__(self, redis: Redis):
        self.redis = redis

    def record_usage(self, tenant_id: str, endpoint: str, tokens: int = 1):
        """Record API usage with hourly and daily aggregation."""
        now = datetime.utcnow()
        hour_key = now.strftime("%Y%m%d%H")
        day_key = now.strftime("%Y%m%d")
        month_key = now.strftime("%Y%m")

        pipe = self.redis.pipeline()

        # Increment hourly counter
        hourly_key = f"usage:{tenant_id}:{hour_key}"
        pipe.hincrby(hourly_key, endpoint, tokens)
        pipe.expire(hourly_key, 86400 * 7)  # Keep 7 days

        # Increment daily counter
        daily_key = f"usage:{tenant_id}:daily:{day_key}"
        pipe.hincrby(daily_key, endpoint, tokens)
        pipe.expire(daily_key, 86400 * 90)  # Keep 90 days

        # Increment monthly counter for billing
        monthly_key = f"usage:{tenant_id}:monthly:{month_key}"
        pipe.hincrby(monthly_key, endpoint, tokens)
        pipe.hincrby(monthly_key, "total", tokens)
        pipe.expire(monthly_key, 86400 * 400)  # Keep ~13 months

        pipe.execute()

    def get_monthly_usage(self, tenant_id: str, month: str = None) -> dict:
        """Get usage for billing."""
        if month is None:
            month = datetime.utcnow().strftime("%Y%m")

        key = f"usage:{tenant_id}:monthly:{month}"
        return self.redis.hgetall(key)
```

### Multi-Tenant Configuration Caching

```python
class TenantConfigCache:
    """Cache tenant configurations with pub/sub invalidation."""

    def __init__(self, redis: Redis):
        self.redis = redis
        self.local_cache = {}
        self.CONFIG_TTL = 300  # 5 minutes

    def get_config(self, tenant_id: str) -> dict:
        """Get tenant config with local + Redis caching."""
        # Local cache first
        if tenant_id in self.local_cache:
            entry = self.local_cache[tenant_id]
            if time.time() < entry['expires']:
                return entry['config']

        # Redis cache
        cache_key = f"tenant:config:{tenant_id}"
        cached = self.redis.get(cache_key)

        if cached:
            config = json.loads(cached)
        else:
            # Fetch from database
            config = self.fetch_config_from_db(tenant_id)
            self.redis.setex(cache_key, self.CONFIG_TTL, json.dumps(config))

        # Update local cache
        self.local_cache[tenant_id] = {
            'config': config,
            'expires': time.time() + 60  # Local TTL shorter
        }

        return config

    def invalidate_config(self, tenant_id: str):
        """Invalidate config across all instances."""
        # Delete from Redis
        self.redis.delete(f"tenant:config:{tenant_id}")

        # Publish invalidation event
        self.redis.publish("tenant:config:invalidated", tenant_id)

        # Clear local cache
        self.local_cache.pop(tenant_id, None)

    def start_invalidation_listener(self):
        """Listen for invalidation events from other instances."""
        pubsub = self.redis.pubsub()
        pubsub.subscribe("tenant:config:invalidated")

        for message in pubsub.listen():
            if message['type'] == 'message':
                tenant_id = message['data']
                self.local_cache.pop(tenant_id, None)
```

---

## Case Study 4: Real-Time Analytics Dashboard

### Context
- IoT platform with 1M devices
- 10K events/second ingestion
- Real-time dashboards
- Time-series aggregations

### Architecture

```
Devices --> Kafka --> Stream Processor --> Redis (aggregations)
                                              |
                                        +-----+-----+
                                        |           |
                                    Dashboard   TimescaleDB
                                    (real-time)  (historical)
```

### Real-Time Aggregation

```python
class RealTimeAggregator:
    """Aggregate metrics in Redis with time windows."""

    def __init__(self, redis: Redis):
        self.redis = redis

    def record_metric(
        self,
        device_id: str,
        metric_name: str,
        value: float,
        timestamp: float = None
    ):
        """Record metric with multi-resolution aggregation."""
        timestamp = timestamp or time.time()

        # Time bucket keys
        minute = int(timestamp // 60) * 60
        hour = int(timestamp // 3600) * 3600
        day = int(timestamp // 86400) * 86400

        pipe = self.redis.pipeline()

        # Per-minute (keep 24 hours)
        minute_key = f"metrics:{device_id}:{metric_name}:min:{minute}"
        pipe.incrbyfloat(minute_key, value)
        pipe.expire(minute_key, 86400)

        # Per-hour stats using HyperLogLog for unique counts
        hour_key = f"metrics:{device_id}:{metric_name}:hour:{hour}"
        pipe.hincrbyfloat(hour_key, "sum", value)
        pipe.hincrby(hour_key, "count", 1)
        pipe.expire(hour_key, 86400 * 7)

        # Update min/max
        pipe.execute()
        self.update_min_max(device_id, metric_name, hour, value)

    def update_min_max(
        self,
        device_id: str,
        metric_name: str,
        hour: int,
        value: float
    ):
        """Atomically update min/max values."""
        key = f"metrics:{device_id}:{metric_name}:hour:{hour}"

        # Use Lua script for atomic min/max
        script = """
        local current_min = redis.call('HGET', KEYS[1], 'min')
        local current_max = redis.call('HGET', KEYS[1], 'max')
        local value = tonumber(ARGV[1])

        if current_min == false or value < tonumber(current_min) then
            redis.call('HSET', KEYS[1], 'min', value)
        end

        if current_max == false or value > tonumber(current_max) then
            redis.call('HSET', KEYS[1], 'max', value)
        end

        return 1
        """
        self.redis.eval(script, 1, key, value)

    def get_dashboard_data(
        self,
        device_ids: list[str],
        metric_name: str,
        hours: int = 24
    ) -> dict:
        """Get aggregated data for dashboard."""
        now = time.time()
        current_hour = int(now // 3600) * 3600

        result = {}
        pipe = self.redis.pipeline()

        for device_id in device_ids:
            for h in range(hours):
                hour = current_hour - (h * 3600)
                key = f"metrics:{device_id}:{metric_name}:hour:{hour}"
                pipe.hgetall(key)

        responses = pipe.execute()

        idx = 0
        for device_id in device_ids:
            device_data = []
            for h in range(hours):
                data = responses[idx]
                if data:
                    device_data.append({
                        'hour': current_hour - (h * 3600),
                        'sum': float(data.get('sum', 0)),
                        'count': int(data.get('count', 0)),
                        'min': float(data.get('min', 0)),
                        'max': float(data.get('max', 0)),
                        'avg': float(data['sum']) / int(data['count']) if data.get('count') else 0
                    })
                idx += 1
            result[device_id] = device_data

        return result
```

### Leaderboard Implementation

```python
class Leaderboard:
    """Real-time leaderboard using Redis Sorted Sets."""

    def __init__(self, redis: Redis):
        self.redis = redis

    def update_score(self, leaderboard_id: str, user_id: str, score: float):
        """Update user score in leaderboard."""
        key = f"leaderboard:{leaderboard_id}"
        self.redis.zadd(key, {user_id: score})

    def increment_score(self, leaderboard_id: str, user_id: str, delta: float):
        """Increment user score atomically."""
        key = f"leaderboard:{leaderboard_id}"
        return self.redis.zincrby(key, delta, user_id)

    def get_top_n(self, leaderboard_id: str, n: int = 10) -> list:
        """Get top N users."""
        key = f"leaderboard:{leaderboard_id}"
        results = self.redis.zrevrange(key, 0, n - 1, withscores=True)

        return [
            {"rank": i + 1, "user_id": user_id, "score": score}
            for i, (user_id, score) in enumerate(results)
        ]

    def get_user_rank(self, leaderboard_id: str, user_id: str) -> dict:
        """Get user's rank and surrounding users."""
        key = f"leaderboard:{leaderboard_id}"

        pipe = self.redis.pipeline()
        pipe.zrevrank(key, user_id)
        pipe.zscore(key, user_id)
        pipe.zcard(key)

        rank, score, total = pipe.execute()

        if rank is None:
            return None

        # Get surrounding users
        start = max(0, rank - 2)
        end = rank + 2

        surrounding = self.redis.zrevrange(
            key, start, end, withscores=True
        )

        return {
            "user_id": user_id,
            "rank": rank + 1,
            "score": score,
            "total_users": total,
            "surrounding": [
                {"rank": start + i + 1, "user_id": uid, "score": s}
                for i, (uid, s) in enumerate(surrounding)
            ]
        }
```

---

## Case Study 5: CDN Caching for Static Site

### Context
- Gatsby/Next.js static site
- Global audience
- SEO critical
- Mixed static + dynamic content

### Cloudflare Configuration

```javascript
// Cloudflare Worker for smart caching

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)

  // Define caching strategy by path
  const cacheStrategies = {
    // Static assets - aggressive caching
    '/static/': { ttl: 31536000, browserTtl: 31536000 },  // 1 year
    '/_next/static/': { ttl: 31536000, browserTtl: 31536000 },

    // HTML pages - short edge cache, revalidate
    '/blog/': { ttl: 3600, browserTtl: 0, swr: 86400 },
    '/docs/': { ttl: 3600, browserTtl: 0, swr: 86400 },

    // API responses - vary by auth
    '/api/': { ttl: 60, browserTtl: 0, private: true },

    // Dynamic pages - no edge cache
    '/dashboard/': { ttl: 0, browserTtl: 0 }
  }

  // Find matching strategy
  let strategy = { ttl: 300, browserTtl: 60 }  // default
  for (const [path, strat] of Object.entries(cacheStrategies)) {
    if (url.pathname.startsWith(path)) {
      strategy = strat
      break
    }
  }

  // Check cache
  const cacheKey = new Request(url.toString(), request)
  const cache = caches.default

  let response = await cache.match(cacheKey)

  if (!response) {
    // Fetch from origin
    response = await fetch(request)

    if (response.ok && strategy.ttl > 0) {
      // Clone response for caching
      response = new Response(response.body, response)

      // Set cache headers
      response.headers.set('Cache-Control',
        `public, max-age=${strategy.browserTtl}, s-maxage=${strategy.ttl}` +
        (strategy.swr ? `, stale-while-revalidate=${strategy.swr}` : '')
      )

      // Store in edge cache
      event.waitUntil(cache.put(cacheKey, response.clone()))
    }
  }

  return response
}
```

### Next.js API Route with Caching

```typescript
// pages/api/products/[id].ts

import { Redis } from '@upstash/redis'
import type { NextApiRequest, NextApiResponse } from 'next'

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL!,
  token: process.env.UPSTASH_REDIS_TOKEN!,
})

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { id } = req.query
  const cacheKey = `product:${id}`

  // Try cache
  const cached = await redis.get(cacheKey)
  if (cached) {
    res.setHeader('X-Cache', 'HIT')
    res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300')
    return res.json(cached)
  }

  // Fetch from database
  const product = await prisma.product.findUnique({
    where: { id: String(id) },
    include: { category: true, reviews: { take: 5 } }
  })

  if (!product) {
    return res.status(404).json({ error: 'Product not found' })
  }

  // Cache for 5 minutes
  await redis.setex(cacheKey, 300, JSON.stringify(product))

  res.setHeader('X-Cache', 'MISS')
  res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300')
  return res.json(product)
}
```

### Results Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| TTFB (global avg) | 850ms | 120ms | 85% |
| Cache hit ratio | 0% | 94% | - |
| Origin requests | 100% | 8% | 92% reduction |
| Bandwidth costs | $500/mo | $45/mo | 91% reduction |
| Core Web Vitals | Poor | Good | All green |
