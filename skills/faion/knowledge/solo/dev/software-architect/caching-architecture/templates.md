# Caching Templates

Copy-paste templates for common caching configurations and implementations.

## Redis Configuration

### Redis Standalone (Development)

```conf
# redis.conf - Development

# Network
bind 127.0.0.1
port 6379
protected-mode yes

# Memory
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence (disable for pure cache)
save ""
appendonly no

# Logging
loglevel notice
logfile ""
```

### Redis Standalone (Production Cache)

```conf
# redis.conf - Production Cache

# Network
bind 0.0.0.0
port 6379
protected-mode yes
requirepass ${REDIS_PASSWORD}
tcp-keepalive 300

# TLS (recommended)
# tls-port 6380
# tls-cert-file /path/to/redis.crt
# tls-key-file /path/to/redis.key
# tls-ca-cert-file /path/to/ca.crt

# Memory
maxmemory 4gb
maxmemory-policy allkeys-lru
maxmemory-samples 10

# Persistence (disable for pure cache)
save ""
appendonly no

# Performance
tcp-backlog 511
timeout 0
databases 16

# Logging
loglevel notice
logfile /var/log/redis/redis.log
```

### Redis Sentinel Configuration

```conf
# sentinel.conf

port 26379
sentinel monitor mymaster 10.0.0.1 6379 2
sentinel auth-pass mymaster ${REDIS_PASSWORD}
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
```

### Redis Cluster Configuration

```conf
# redis-cluster.conf

port 7000
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes

maxmemory 2gb
maxmemory-policy allkeys-lru
```

---

## Docker Compose Templates

### Redis Single Node

```yaml
# docker-compose.yml

version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    command: redis-server /usr/local/etc/redis/redis.conf
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  redis_data:
```

### Redis with Sentinel (HA)

```yaml
# docker-compose-sentinel.yml

version: '3.8'

services:
  redis-master:
    image: redis:7-alpine
    container_name: redis-master
    ports:
      - "6379:6379"
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_master_data:/data

  redis-replica-1:
    image: redis:7-alpine
    container_name: redis-replica-1
    ports:
      - "6380:6379"
    command: redis-server --replicaof redis-master 6379 --masterauth ${REDIS_PASSWORD} --requirepass ${REDIS_PASSWORD}
    depends_on:
      - redis-master

  redis-replica-2:
    image: redis:7-alpine
    container_name: redis-replica-2
    ports:
      - "6381:6379"
    command: redis-server --replicaof redis-master 6379 --masterauth ${REDIS_PASSWORD} --requirepass ${REDIS_PASSWORD}
    depends_on:
      - redis-master

  sentinel-1:
    image: redis:7-alpine
    container_name: sentinel-1
    ports:
      - "26379:26379"
    command: redis-sentinel /etc/redis/sentinel.conf
    volumes:
      - ./sentinel.conf:/etc/redis/sentinel.conf
    depends_on:
      - redis-master
      - redis-replica-1
      - redis-replica-2

volumes:
  redis_master_data:
```

### Redis Cluster (6 nodes)

```yaml
# docker-compose-cluster.yml

version: '3.8'

services:
  redis-node-1:
    image: redis:7-alpine
    container_name: redis-node-1
    ports:
      - "7001:7001"
      - "17001:17001"
    volumes:
      - ./cluster/node1:/data
    command: redis-server --port 7001 --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes

  redis-node-2:
    image: redis:7-alpine
    container_name: redis-node-2
    ports:
      - "7002:7002"
      - "17002:17002"
    volumes:
      - ./cluster/node2:/data
    command: redis-server --port 7002 --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes

  redis-node-3:
    image: redis:7-alpine
    container_name: redis-node-3
    ports:
      - "7003:7003"
      - "17003:17003"
    volumes:
      - ./cluster/node3:/data
    command: redis-server --port 7003 --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes

  redis-node-4:
    image: redis:7-alpine
    container_name: redis-node-4
    ports:
      - "7004:7004"
      - "17004:17004"
    volumes:
      - ./cluster/node4:/data
    command: redis-server --port 7004 --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes

  redis-node-5:
    image: redis:7-alpine
    container_name: redis-node-5
    ports:
      - "7005:7005"
      - "17005:17005"
    volumes:
      - ./cluster/node5:/data
    command: redis-server --port 7005 --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes

  redis-node-6:
    image: redis:7-alpine
    container_name: redis-node-6
    ports:
      - "7006:7006"
      - "17006:17006"
    volumes:
      - ./cluster/node6:/data
    command: redis-server --port 7006 --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes

  redis-cluster-init:
    image: redis:7-alpine
    depends_on:
      - redis-node-1
      - redis-node-2
      - redis-node-3
      - redis-node-4
      - redis-node-5
      - redis-node-6
    command: >
      sh -c "sleep 5 &&
      redis-cli --cluster create
      redis-node-1:7001
      redis-node-2:7002
      redis-node-3:7003
      redis-node-4:7004
      redis-node-5:7005
      redis-node-6:7006
      --cluster-replicas 1 --cluster-yes"
```

---

## Python Templates

### Django Cache Configuration

```python
# settings.py

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': os.environ.get('REDIS_PASSWORD'),
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True
            },
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
        },
        'KEY_PREFIX': 'myapp',
        'TIMEOUT': 300,  # Default TTL: 5 minutes
    },
    'sessions': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'session',
        'TIMEOUT': 86400,  # 24 hours
    }
}

# Use Redis for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'

# Cache middleware settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'page'
```

### Django Cache Decorators

```python
# views.py

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache
from functools import wraps

# Simple page caching
@cache_page(60 * 15)  # 15 minutes
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

# Vary cache by user
@cache_page(60 * 5)
@vary_on_cookie
def user_dashboard(request):
    return render(request, 'dashboard.html')

# Manual caching in views
def product_detail(request, product_id):
    cache_key = f'product:{product_id}:v1'
    product = cache.get(cache_key)

    if product is None:
        product = get_object_or_404(Product, id=product_id)
        cache.set(cache_key, product, timeout=900)

    return render(request, 'products/detail.html', {'product': product})

# Custom cache decorator with key builder
def cache_result(timeout=300, key_builder=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                cache_key = f"{func.__module__}.{func.__name__}:{args}:{kwargs}"

            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout=timeout)

            return result
        return wrapper
    return decorator

# Usage
@cache_result(timeout=600, key_builder=lambda user_id: f"user:{user_id}:stats")
def get_user_stats(user_id):
    return calculate_expensive_stats(user_id)
```

### FastAPI Cache Configuration

```python
# cache.py

from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import json

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://localhost:6379",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# Simple endpoint caching
@app.get("/products")
@cache(expire=300)
async def get_products():
    products = await fetch_products_from_db()
    return products

# Cache with custom key builder
def product_key_builder(func, namespace: str = "", *, product_id: int, **kwargs):
    return f"product:{product_id}"

@app.get("/products/{product_id}")
@cache(expire=600, key_builder=product_key_builder)
async def get_product(product_id: int):
    product = await fetch_product_from_db(product_id)
    return product

# Manual caching
from redis import asyncio as aioredis

redis = aioredis.from_url("redis://localhost:6379")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    cache_key = f"user:{user_id}"

    # Try cache
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # Fetch and cache
    user = await fetch_user_from_db(user_id)
    await redis.setex(cache_key, 300, json.dumps(user))

    return user
```

### Generic Cache Service (Python)

```python
# cache_service.py

from redis import Redis
from typing import TypeVar, Generic, Optional, Callable
import json
import hashlib
import time
import random
import math

T = TypeVar('T')

class CacheService(Generic[T]):
    """Generic caching service with common patterns."""

    def __init__(
        self,
        redis: Redis,
        prefix: str,
        default_ttl: int = 300,
        serializer: Callable[[T], str] = json.dumps,
        deserializer: Callable[[str], T] = json.loads
    ):
        self.redis = redis
        self.prefix = prefix
        self.default_ttl = default_ttl
        self.serializer = serializer
        self.deserializer = deserializer

    def _key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    def get(self, key: str) -> Optional[T]:
        """Get value from cache."""
        data = self.redis.get(self._key(key))
        if data:
            return self.deserializer(data)
        return None

    def set(self, key: str, value: T, ttl: int = None) -> None:
        """Set value in cache."""
        ttl = ttl or self.default_ttl
        self.redis.setex(
            self._key(key),
            ttl,
            self.serializer(value)
        )

    def delete(self, key: str) -> None:
        """Delete from cache."""
        self.redis.delete(self._key(key))

    def get_or_set(
        self,
        key: str,
        factory: Callable[[], T],
        ttl: int = None
    ) -> T:
        """Get from cache or compute and store."""
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl)
        return value

    def get_or_set_with_lock(
        self,
        key: str,
        factory: Callable[[], T],
        ttl: int = None,
        lock_timeout: int = 10
    ) -> T:
        """Get with lock to prevent stampede."""
        value = self.get(key)
        if value is not None:
            return value

        lock_key = f"{self._key(key)}:lock"

        # Try to acquire lock
        if self.redis.set(lock_key, "1", nx=True, ex=lock_timeout):
            try:
                # Double-check cache
                value = self.get(key)
                if value is not None:
                    return value

                # Compute and store
                value = factory()
                self.set(key, value, ttl)
                return value
            finally:
                self.redis.delete(lock_key)
        else:
            # Wait for other process to populate cache
            for _ in range(lock_timeout * 10):
                time.sleep(0.1)
                value = self.get(key)
                if value is not None:
                    return value

            # Timeout - compute ourselves
            return factory()

    def get_with_early_expiration(
        self,
        key: str,
        factory: Callable[[], T],
        ttl: int = None,
        beta: float = 1.0
    ) -> T:
        """Probabilistic early expiration to prevent stampede."""
        ttl = ttl or self.default_ttl
        full_key = self._key(key)

        # Get value with TTL
        pipe = self.redis.pipeline()
        pipe.get(full_key)
        pipe.ttl(full_key)
        data, remaining_ttl = pipe.execute()

        if data is not None:
            value = self.deserializer(data)

            # Probabilistic early refresh
            if remaining_ttl > 0:
                # XFetch algorithm
                delta = ttl - remaining_ttl
                should_refresh = delta > 0 and (
                    -delta * beta * math.log(random.random()) >= remaining_ttl
                )

                if should_refresh:
                    # Refresh in background (simplified - sync here)
                    value = factory()
                    self.set(key, value, ttl)

            return value

        # Cache miss
        value = factory()
        self.set(key, value, ttl)
        return value

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate keys matching pattern."""
        full_pattern = self._key(pattern)
        keys = self.redis.keys(full_pattern)
        if keys:
            return self.redis.delete(*keys)
        return 0


# Usage
class ProductCache(CacheService[dict]):
    def __init__(self, redis: Redis):
        super().__init__(redis, "product", default_ttl=900)

    def get_product(self, product_id: str) -> dict:
        return self.get_or_set_with_lock(
            product_id,
            lambda: fetch_product_from_db(product_id)
        )

    def invalidate_product(self, product_id: str):
        self.delete(product_id)
```

---

## Node.js/TypeScript Templates

### Redis Client Setup

```typescript
// redis.ts

import { createClient, RedisClientType } from 'redis';

let client: RedisClientType;

export async function getRedisClient(): Promise<RedisClientType> {
  if (!client) {
    client = createClient({
      url: process.env.REDIS_URL || 'redis://localhost:6379',
      password: process.env.REDIS_PASSWORD,
      socket: {
        connectTimeout: 5000,
        reconnectStrategy: (retries) => {
          if (retries > 10) {
            return new Error('Max reconnection attempts reached');
          }
          return Math.min(retries * 100, 3000);
        }
      }
    });

    client.on('error', (err) => console.error('Redis Client Error', err));
    client.on('connect', () => console.log('Redis Client Connected'));

    await client.connect();
  }

  return client;
}

// Cache wrapper
export class Cache {
  private client: RedisClientType;
  private prefix: string;
  private defaultTTL: number;

  constructor(client: RedisClientType, prefix: string, defaultTTL: number = 300) {
    this.client = client;
    this.prefix = prefix;
    this.defaultTTL = defaultTTL;
  }

  private key(k: string): string {
    return `${this.prefix}:${k}`;
  }

  async get<T>(key: string): Promise<T | null> {
    const data = await this.client.get(this.key(key));
    return data ? JSON.parse(data) : null;
  }

  async set<T>(key: string, value: T, ttl?: number): Promise<void> {
    await this.client.setEx(
      this.key(key),
      ttl || this.defaultTTL,
      JSON.stringify(value)
    );
  }

  async delete(key: string): Promise<void> {
    await this.client.del(this.key(key));
  }

  async getOrSet<T>(
    key: string,
    factory: () => Promise<T>,
    ttl?: number
  ): Promise<T> {
    let value = await this.get<T>(key);

    if (value === null) {
      value = await factory();
      await this.set(key, value, ttl);
    }

    return value;
  }
}
```

### Express Middleware

```typescript
// cache-middleware.ts

import { Request, Response, NextFunction } from 'express';
import { Cache } from './redis';

export function cacheMiddleware(cache: Cache, ttl: number = 300) {
  return async (req: Request, res: Response, next: NextFunction) => {
    // Only cache GET requests
    if (req.method !== 'GET') {
      return next();
    }

    const cacheKey = `route:${req.originalUrl}`;

    try {
      const cached = await cache.get<{ body: any; headers: Record<string, string> }>(cacheKey);

      if (cached) {
        res.set('X-Cache', 'HIT');
        Object.entries(cached.headers).forEach(([key, value]) => {
          res.set(key, value);
        });
        return res.json(cached.body);
      }

      // Store original json method
      const originalJson = res.json.bind(res);

      // Override json method to cache response
      res.json = (body: any) => {
        const headersToCache: Record<string, string> = {};

        // Cache specific headers
        ['Content-Type', 'ETag'].forEach(header => {
          const value = res.get(header);
          if (value) headersToCache[header] = value;
        });

        cache.set(cacheKey, { body, headers: headersToCache }, ttl);

        res.set('X-Cache', 'MISS');
        return originalJson(body);
      };

      next();
    } catch (error) {
      // On cache error, proceed without caching
      next();
    }
  };
}

// Usage
import express from 'express';

const app = express();
const cache = new Cache(redisClient, 'api');

app.get('/api/products', cacheMiddleware(cache, 300), async (req, res) => {
  const products = await getProducts();
  res.json(products);
});
```

---

## CDN Configuration Templates

### Cloudflare Page Rules

```yaml
# cloudflare-rules.yaml (for reference - configure in dashboard)

rules:
  # Static assets - aggressive caching
  - url_pattern: "*example.com/static/*"
    settings:
      cache_level: "cache_everything"
      edge_cache_ttl: 31536000  # 1 year
      browser_cache_ttl: 31536000

  # API responses - short cache
  - url_pattern: "*example.com/api/*"
    settings:
      cache_level: "bypass"  # Or use Cache Rules for API caching

  # Blog posts - medium cache with revalidation
  - url_pattern: "*example.com/blog/*"
    settings:
      cache_level: "cache_everything"
      edge_cache_ttl: 3600  # 1 hour
      browser_cache_ttl: 0

  # Admin/Dashboard - no cache
  - url_pattern: "*example.com/admin/*"
    settings:
      cache_level: "bypass"
      security_level: "high"
```

### Cloudflare Workers Cache API

```javascript
// worker.js

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const cache = caches.default;

    // Custom cache key (remove tracking params)
    const cacheUrl = new URL(url);
    cacheUrl.searchParams.delete('utm_source');
    cacheUrl.searchParams.delete('utm_medium');
    cacheUrl.searchParams.delete('utm_campaign');
    const cacheKey = new Request(cacheUrl.toString(), request);

    // Check cache
    let response = await cache.match(cacheKey);

    if (!response) {
      response = await fetch(request);

      // Only cache successful responses
      if (response.ok) {
        response = new Response(response.body, response);

        // Set cache headers based on content type
        const contentType = response.headers.get('content-type') || '';

        if (contentType.includes('text/html')) {
          response.headers.set('Cache-Control', 'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400');
        } else if (contentType.includes('application/json')) {
          response.headers.set('Cache-Control', 'public, max-age=0, s-maxage=60');
        } else if (contentType.includes('image/') || contentType.includes('font/')) {
          response.headers.set('Cache-Control', 'public, max-age=31536000, immutable');
        }

        ctx.waitUntil(cache.put(cacheKey, response.clone()));
      }
    } else {
      // Add cache status header
      response = new Response(response.body, response);
      response.headers.set('X-Cache-Status', 'HIT');
    }

    return response;
  }
};
```

### AWS CloudFront Cache Policy (Terraform)

```hcl
# cloudfront.tf

resource "aws_cloudfront_cache_policy" "api_cache" {
  name        = "api-cache-policy"
  comment     = "Cache policy for API responses"
  default_ttl = 60
  max_ttl     = 3600
  min_ttl     = 0

  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }

    headers_config {
      header_behavior = "whitelist"
      headers {
        items = ["Authorization", "Accept"]
      }
    }

    query_strings_config {
      query_string_behavior = "whitelist"
      query_strings {
        items = ["page", "limit", "sort"]
      }
    }

    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true
  }
}

resource "aws_cloudfront_cache_policy" "static_cache" {
  name        = "static-assets-cache-policy"
  comment     = "Long-term cache for static assets"
  default_ttl = 86400
  max_ttl     = 31536000
  min_ttl     = 86400

  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }

    headers_config {
      header_behavior = "none"
    }

    query_strings_config {
      query_string_behavior = "none"
    }

    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true
  }
}

resource "aws_cloudfront_distribution" "main" {
  enabled = true

  origin {
    domain_name = aws_s3_bucket.static.bucket_regional_domain_name
    origin_id   = "S3-static"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path
    }
  }

  origin {
    domain_name = "api.example.com"
    origin_id   = "API"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  # Static assets
  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-static"
    cache_policy_id        = aws_cloudfront_cache_policy.static_cache.id
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
  }

  # API
  ordered_cache_behavior {
    path_pattern           = "/api/*"
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "API"
    cache_policy_id        = aws_cloudfront_cache_policy.api_cache.id
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.main.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
```

---

## Monitoring Templates

### Prometheus Redis Exporter

```yaml
# docker-compose-monitoring.yml

version: '3.8'

services:
  redis-exporter:
    image: oliver006/redis_exporter:latest
    container_name: redis-exporter
    ports:
      - "9121:9121"
    environment:
      - REDIS_ADDR=redis://redis:6379
      - REDIS_PASSWORD=${REDIS_PASSWORD}
    depends_on:
      - redis

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}

volumes:
  prometheus_data:
  grafana_data:
```

### Prometheus Configuration

```yaml
# prometheus.yml

global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

rule_files:
  - "alerts/*.yml"

scrape_configs:
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'redis-primary'
```

### Alert Rules

```yaml
# alerts/redis.yml

groups:
  - name: redis
    rules:
      - alert: RedisDown
        expr: redis_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Redis instance down"
          description: "Redis instance {{ $labels.instance }} is down"

      - alert: RedisMemoryHigh
        expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Redis memory usage high"
          description: "Redis memory usage is above 90%"

      - alert: RedisCacheHitRateLow
        expr: rate(redis_keyspace_hits_total[5m]) / (rate(redis_keyspace_hits_total[5m]) + rate(redis_keyspace_misses_total[5m])) < 0.7
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Redis cache hit ratio low"
          description: "Cache hit ratio is below 70%"

      - alert: RedisConnectedClientsHigh
        expr: redis_connected_clients > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High number of Redis connections"
          description: "Redis has {{ $value }} connected clients"

      - alert: RedisEvictedKeysHigh
        expr: rate(redis_evicted_keys_total[5m]) > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High Redis key eviction rate"
          description: "Redis is evicting {{ $value }} keys per second"
```
