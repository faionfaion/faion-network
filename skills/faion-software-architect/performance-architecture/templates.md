# Performance Architecture Templates

Copy-paste configurations for performance optimization across different technologies.

---

## SLO Definition Templates

### Basic SLO Template

```yaml
# slo.yaml
service: api-gateway
version: "1.0"

slos:
  - name: availability
    description: Service should be available 99.9% of the time
    sli:
      type: availability
      metric: http_requests_total{status!~"5.."}
    target: 99.9
    window: 30d
    error_budget: 0.1%  # 43.8 minutes/month

  - name: latency
    description: 95% of requests should complete within 300ms
    sli:
      type: latency
      metric: http_request_duration_seconds
      threshold: 0.3
    target: 95
    window: 30d

  - name: throughput
    description: Service should handle at least 10000 RPS
    sli:
      type: throughput
      metric: rate(http_requests_total[5m])
    target: 10000
    window: 1h

alerts:
  - name: error_budget_burn_fast
    description: Consuming error budget too quickly
    condition: burn_rate_1h > 14.4  # 2% of monthly budget in 1 hour
    severity: critical
    action: page-oncall

  - name: error_budget_burn_slow
    description: Elevated error budget consumption
    condition: burn_rate_6h > 6
    severity: warning
    action: slack-alert
```

### Prometheus SLO Rules

```yaml
# prometheus-slo-rules.yaml
groups:
  - name: slo-api-gateway
    rules:
      # Error rate SLI
      - record: slo:api_gateway:error_rate
        expr: |
          sum(rate(http_requests_total{service="api-gateway",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{service="api-gateway"}[5m]))

      # Latency SLI (% of requests under threshold)
      - record: slo:api_gateway:latency_good
        expr: |
          sum(rate(http_request_duration_seconds_bucket{service="api-gateway",le="0.3"}[5m]))
          /
          sum(rate(http_request_duration_seconds_count{service="api-gateway"}[5m]))

      # Error budget remaining (monthly)
      - record: slo:api_gateway:error_budget_remaining
        expr: |
          1 - (
            (1 - slo:api_gateway:latency_good)
            /
            (1 - 0.999)  # SLO target
          )

      # Fast burn alert
      - alert: APIGatewayErrorBudgetFastBurn
        expr: |
          (
            (1 - slo:api_gateway:latency_good)
            /
            (1 - 0.999)
          ) > 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "API Gateway burning error budget too fast"
          description: "Consuming {{ $value | printf \"%.1f\" }}x the normal error rate"
```

---

## Caching Configuration Templates

### Redis Configuration

```conf
# redis.conf - Production configuration
# Memory
maxmemory 4gb
maxmemory-policy allkeys-lru

# Persistence (disable for pure cache)
save ""
appendonly no

# Performance
tcp-keepalive 300
timeout 0
tcp-backlog 511

# Connections
maxclients 10000

# Slow log
slowlog-log-slower-than 10000
slowlog-max-len 128

# Cluster mode (if using)
# cluster-enabled yes
# cluster-config-file nodes.conf
# cluster-node-timeout 5000
```

### Redis Cluster Docker Compose

```yaml
# docker-compose-redis-cluster.yaml
version: '3.8'

services:
  redis-node-1:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis-cluster.conf:/etc/redis/redis.conf
      - redis-data-1:/data
    ports:
      - "6379:6379"
      - "16379:16379"
    networks:
      - redis-cluster

  redis-node-2:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis-cluster.conf:/etc/redis/redis.conf
      - redis-data-2:/data
    ports:
      - "6380:6379"
      - "16380:16379"
    networks:
      - redis-cluster

  redis-node-3:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis-cluster.conf:/etc/redis/redis.conf
      - redis-data-3:/data
    ports:
      - "6381:6379"
      - "16381:16379"
    networks:
      - redis-cluster

  redis-cluster-init:
    image: redis:7-alpine
    depends_on:
      - redis-node-1
      - redis-node-2
      - redis-node-3
    command: |
      sh -c "sleep 5 && redis-cli --cluster create \
        redis-node-1:6379 redis-node-2:6379 redis-node-3:6379 \
        --cluster-replicas 0 --cluster-yes"
    networks:
      - redis-cluster

volumes:
  redis-data-1:
  redis-data-2:
  redis-data-3:

networks:
  redis-cluster:
    driver: bridge
```

### Python Redis Cache Decorator

```python
# cache.py
import redis
import json
import hashlib
from functools import wraps
from typing import Optional, Callable, Any

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True
)

def cache(
    ttl: int = 300,
    key_prefix: str = "",
    key_builder: Optional[Callable] = None
):
    """
    Cache decorator with configurable TTL and key building.

    Usage:
        @cache(ttl=600, key_prefix="user")
        def get_user(user_id: int):
            return db.query(User).get(user_id)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
                key_hash = hashlib.md5(key_data.encode()).hexdigest()[:12]
                cache_key = f"{key_prefix}:{func.__name__}:{key_hash}"

            # Try cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function
            result = func(*args, **kwargs)

            # Store in cache
            redis_client.setex(cache_key, ttl, json.dumps(result))

            return result

        # Add cache invalidation method
        def invalidate(*args, **kwargs):
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
                key_hash = hashlib.md5(key_data.encode()).hexdigest()[:12]
                cache_key = f"{key_prefix}:{func.__name__}:{key_hash}"
            redis_client.delete(cache_key)

        wrapper.invalidate = invalidate
        return wrapper

    return decorator

# Usage examples
@cache(ttl=600, key_prefix="product")
def get_product(product_id: int) -> dict:
    return Product.query.get(product_id).to_dict()

@cache(
    ttl=300,
    key_builder=lambda category_id, page: f"products:cat:{category_id}:p:{page}"
)
def get_products_by_category(category_id: int, page: int = 1) -> list:
    return Product.query.filter_by(category_id=category_id).paginate(page=page).items
```

---

## Database Optimization Templates

### PostgreSQL Configuration

```conf
# postgresql.conf - Performance tuning

# Memory (assuming 16GB total RAM)
shared_buffers = 4GB                    # 25% of RAM
effective_cache_size = 12GB             # 75% of RAM
work_mem = 256MB                        # Per-operation memory
maintenance_work_mem = 1GB              # For VACUUM, CREATE INDEX
wal_buffers = 64MB

# Checkpoints
checkpoint_completion_target = 0.9
max_wal_size = 4GB
min_wal_size = 1GB

# Query planner
random_page_cost = 1.1                  # For SSD
effective_io_concurrency = 200          # For SSD
default_statistics_target = 100

# Connections
max_connections = 200                   # Use connection pooling for more

# Parallel queries
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
max_parallel_maintenance_workers = 4

# Logging (for debugging)
log_min_duration_statement = 1000       # Log queries > 1s
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0

# Statistics
track_activities = on
track_counts = on
track_io_timing = on
track_functions = all
```

### PgBouncer Configuration

```ini
# pgbouncer.ini
[databases]
myapp = host=postgres-primary port=5432 dbname=myapp
myapp_replica = host=postgres-replica port=5432 dbname=myapp

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Pool mode: transaction is best for web apps
pool_mode = transaction

# Connections
max_client_conn = 1000
default_pool_size = 50
min_pool_size = 10
reserve_pool_size = 5
reserve_pool_timeout = 3

# Timeouts
server_connect_timeout = 15
server_idle_timeout = 600
server_lifetime = 3600
query_timeout = 300
query_wait_timeout = 120

# Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1
stats_period = 60

# Admin console
admin_users = admin
```

### Common Index Templates

```sql
-- B-tree index for equality and range queries
CREATE INDEX CONCURRENTLY idx_orders_user_created
ON orders (user_id, created_at DESC);

-- Partial index for active records only
CREATE INDEX CONCURRENTLY idx_products_active
ON products (category_id, price)
WHERE is_active = true;

-- Covering index (includes all columns needed)
CREATE INDEX CONCURRENTLY idx_users_email_covering
ON users (email) INCLUDE (id, name, created_at);

-- GIN index for JSONB
CREATE INDEX CONCURRENTLY idx_events_metadata
ON events USING gin (metadata jsonb_path_ops);

-- Full-text search index
CREATE INDEX CONCURRENTLY idx_products_search
ON products USING gin (to_tsvector('english', name || ' ' || description));

-- Expression index for case-insensitive search
CREATE INDEX CONCURRENTLY idx_users_email_lower
ON users (LOWER(email));

-- BRIN index for time-series data
CREATE INDEX CONCURRENTLY idx_events_time_brin
ON events USING brin (created_at) WITH (pages_per_range = 128);
```

---

## Load Testing Templates

### k6 Basic Load Test

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const apiLatency = new Trend('api_latency');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 50 },    // Ramp up
    { duration: '5m', target: 50 },    // Stay at 50 users
    { duration: '2m', target: 100 },   // Ramp to 100
    { duration: '5m', target: 100 },   // Stay at 100
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
    errors: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  group('API Health Check', function () {
    const res = http.get(`${BASE_URL}/health`);
    check(res, {
      'health check status is 200': (r) => r.status === 200,
    });
  });

  group('Product Listing', function () {
    const res = http.get(`${BASE_URL}/api/products?page=1&limit=20`);
    const success = check(res, {
      'products status is 200': (r) => r.status === 200,
      'products has items': (r) => JSON.parse(r.body).items.length > 0,
    });
    errorRate.add(!success);
    apiLatency.add(res.timings.duration);
  });

  group('Product Detail', function () {
    const productId = Math.floor(Math.random() * 1000) + 1;
    const res = http.get(`${BASE_URL}/api/products/${productId}`);
    check(res, {
      'product detail status is 200': (r) => r.status === 200,
    });
  });

  sleep(Math.random() * 2 + 1); // 1-3 seconds between requests
}

// Setup: Run once before test
export function setup() {
  const loginRes = http.post(`${BASE_URL}/api/auth/login`, {
    email: 'test@example.com',
    password: 'testpassword',
  });
  return { token: loginRes.json('token') };
}

// Teardown: Run once after test
export function teardown(data) {
  console.log('Test completed');
}
```

### k6 Stress Test

```javascript
// stress-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 300 },
    { duration: '5m', target: 300 },
    { duration: '2m', target: 400 },
    { duration: '5m', target: 400 },
    { duration: '5m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<1500'], // Relaxed for stress test
    http_req_failed: ['rate<0.05'],     // Allow higher error rate
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/products`);
  check(res, { 'status was 200': (r) => r.status === 200 });
  sleep(1);
}
```

### k6 with Scenarios

```javascript
// scenarios.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    browse: {
      executor: 'constant-vus',
      vus: 50,
      duration: '10m',
      exec: 'browse',
    },
    checkout: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      preAllocatedVUs: 50,
      stages: [
        { target: 10, duration: '2m' },
        { target: 50, duration: '5m' },
        { target: 10, duration: '3m' },
      ],
      exec: 'checkout',
    },
  },
};

export function browse() {
  http.get(`${__ENV.BASE_URL}/api/products`);
  sleep(Math.random() * 3);
}

export function checkout() {
  const payload = JSON.stringify({
    items: [{ product_id: 1, quantity: 1 }],
    payment_method: 'card',
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(`${__ENV.BASE_URL}/api/checkout`, payload, params);
  check(res, {
    'checkout successful': (r) => r.status === 200 || r.status === 201,
  });
}
```

### Locust Python Template

```python
# locustfile.py
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import random
import json

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    def on_start(self):
        """Called when user starts - login"""
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "testpassword"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            self.token = None

    @task(10)  # Weight: 10x more likely
    def browse_products(self):
        self.client.get("/api/products", params={"page": 1, "limit": 20})

    @task(5)
    def view_product(self):
        product_id = random.randint(1, 1000)
        self.client.get(f"/api/products/{product_id}")

    @task(2)
    def search_products(self):
        queries = ["laptop", "phone", "tablet", "headphones"]
        self.client.get("/api/search", params={"q": random.choice(queries)})

    @task(1)
    def add_to_cart(self):
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post(
            "/api/cart/items",
            json={"product_id": random.randint(1, 100), "quantity": 1},
            headers=headers
        )

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("Beginning distributed test")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Test completed")
```

---

## Kubernetes Autoscaling Templates

### Horizontal Pod Autoscaler

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 3
  maxReplicas: 50
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 5 min cooldown
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0  # Scale up immediately
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

### KEDA ScaledObject (Queue-based)

```yaml
# keda-scaledobject.yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: worker-scaler
  namespace: production
spec:
  scaleTargetRef:
    name: worker-deployment
  minReplicaCount: 1
  maxReplicaCount: 100
  pollingInterval: 15
  cooldownPeriod: 300
  triggers:
    - type: rabbitmq
      metadata:
        host: "amqp://rabbitmq.production:5672"
        queueName: tasks
        queueLength: "50"  # Scale when queue > 50 messages
    - type: prometheus
      metadata:
        serverAddress: http://prometheus:9090
        metricName: job_queue_depth
        threshold: "100"
        query: |
          sum(job_queue_depth{queue="priority"})
```

### Vertical Pod Autoscaler

```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  updatePolicy:
    updateMode: Auto  # or "Off" for recommendations only
  resourcePolicy:
    containerPolicies:
      - containerName: api
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 4
          memory: 8Gi
        controlledResources: ["cpu", "memory"]
```

---

## CDN Configuration Templates

### Cloudflare Page Rules (via API)

```bash
# cloudflare-rules.sh
#!/bin/bash
ZONE_ID="your-zone-id"
API_TOKEN="your-api-token"

# Cache static assets for 1 year
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "targets": [
      {"target": "url", "constraint": {"operator": "matches", "value": "*example.com/static/*"}}
    ],
    "actions": [
      {"id": "cache_level", "value": "cache_everything"},
      {"id": "edge_cache_ttl", "value": 31536000},
      {"id": "browser_cache_ttl", "value": 31536000}
    ],
    "status": "active"
  }'

# Cache API responses for 5 minutes
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/pagerules" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "targets": [
      {"target": "url", "constraint": {"operator": "matches", "value": "*api.example.com/v1/public/*"}}
    ],
    "actions": [
      {"id": "cache_level", "value": "cache_everything"},
      {"id": "edge_cache_ttl", "value": 300}
    ],
    "status": "active"
  }'
```

### Nginx Caching Configuration

```nginx
# nginx-cache.conf
# Cache zone configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:100m
                 max_size=10g inactive=60m use_temp_path=off;

# Upstream configuration
upstream api_servers {
    least_conn;
    server api-1:8000 weight=5;
    server api-2:8000 weight=5;
    server api-3:8000 weight=5;
    keepalive 32;
}

server {
    listen 80;
    server_name api.example.com;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript
               application/xml application/xml+rss text/javascript;

    # Brotli compression (if module available)
    # brotli on;
    # brotli_comp_level 6;
    # brotli_types text/plain text/css text/xml application/json application/javascript;

    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # API with caching
    location /api/ {
        proxy_pass http://api_servers;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        # Caching
        proxy_cache api_cache;
        proxy_cache_valid 200 5m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;

        # Cache key
        proxy_cache_key "$scheme$request_method$host$request_uri";

        # Headers
        add_header X-Cache-Status $upstream_cache_status;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Bypass cache for authenticated requests
    location /api/user/ {
        proxy_pass http://api_servers;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_cache off;
    }
}
```

---

## Monitoring Templates

### Prometheus Alerting Rules

```yaml
# prometheus-alerts.yaml
groups:
  - name: performance-alerts
    rules:
      # High latency
      - alert: HighLatencyP95
        expr: |
          histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
          > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p95 latency for {{ $labels.service }}"
          description: "P95 latency is {{ $value | printf \"%.2f\" }}s (threshold: 500ms)"

      - alert: HighLatencyP99
        expr: |
          histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
          > 1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Critical p99 latency for {{ $labels.service }}"
          description: "P99 latency is {{ $value | printf \"%.2f\" }}s (threshold: 1s)"

      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)
          > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate for {{ $labels.service }}"
          description: "Error rate is {{ $value | printf \"%.2f%%\" }}"

      # Low throughput
      - alert: LowThroughput
        expr: |
          sum(rate(http_requests_total[5m])) by (service) < 100
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Low throughput for {{ $labels.service }}"

      # Database connection pool exhaustion
      - alert: DBConnectionPoolExhausted
        expr: |
          pg_stat_activity_count / pg_settings_max_connections > 0.9
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool nearly exhausted"

      # Cache hit rate low
      - alert: LowCacheHitRate
        expr: |
          redis_keyspace_hits / (redis_keyspace_hits + redis_keyspace_misses) < 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Redis cache hit rate below 80%"
```

### Grafana Dashboard JSON (SLO Dashboard)

```json
{
  "dashboard": {
    "title": "SLO Dashboard",
    "panels": [
      {
        "title": "Availability SLO",
        "type": "gauge",
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d])) * 100",
            "legendFormat": "Availability %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "orange", "value": 99},
                {"color": "yellow", "value": 99.5},
                {"color": "green", "value": 99.9}
              ]
            },
            "min": 98,
            "max": 100
          }
        }
      },
      {
        "title": "Error Budget Remaining",
        "type": "stat",
        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 0},
        "targets": [
          {
            "expr": "(1 - ((1 - (sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d])))) / 0.001)) * 100",
            "legendFormat": "Budget %"
          }
        ]
      },
      {
        "title": "Latency Percentiles",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "p99"
          }
        ]
      }
    ]
  }
}
```

---

## Application Configuration Templates

### Django Performance Settings

```python
# settings/performance.py
import os

# Database connection pooling (using django-db-connection-pool)
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'myapp'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 20,
            'RECYCLE': 300,
        }
    }
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'RETRY_ON_TIMEOUT': True,
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        },
        'KEY_PREFIX': 'myapp',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Session in Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Query optimization
DATABASE_ROUTERS = ['myapp.routers.PrimaryReplicaRouter']

# Logging slow queries
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if os.environ.get('LOG_SQL') else 'WARNING',
        },
    },
}
```

### FastAPI Performance Configuration

```python
# config.py
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://localhost/myapp"
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_recycle: int = 300

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Performance
    workers: int = 4
    timeout: int = 30

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

settings = get_settings()

engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# main.py
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import aioredis

app = FastAPI()

# Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="api-cache")
```

---

## Quick Reference

### Cache TTL Guidelines

| Data Type | TTL | Invalidation |
|-----------|-----|--------------|
| Static assets | 1 year | Version in URL |
| User session | 24 hours | On logout |
| Product listing | 5-15 min | On update |
| Search results | 1-5 min | TTL only |
| User preferences | 1 hour | On change |
| API responses (public) | 1-5 min | TTL only |

### Database Connection Pool Sizing

```
pool_size = (CPU cores * 2) + effective_spindle_count
```

For SSD-based systems: `pool_size = CPU cores * 2`

| Workload | Pool Size | Max Overflow |
|----------|-----------|--------------|
| Light (< 100 RPS) | 5-10 | 10 |
| Medium (100-1K RPS) | 10-25 | 25 |
| Heavy (> 1K RPS) | 25-50 | 50 |

### k6 Quick Commands

```bash
# Basic run
k6 run load-test.js

# With environment variables
k6 run -e BASE_URL=https://api.example.com load-test.js

# Cloud run
k6 cloud load-test.js

# Output to JSON
k6 run --out json=results.json load-test.js

# Output to InfluxDB
k6 run --out influxdb=http://localhost:8086/k6 load-test.js
```
