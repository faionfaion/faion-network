# Load Balancing Examples

## Health Check Implementation

### Python Flask Health Endpoints

```python
from flask import Flask, jsonify
import psycopg2
import redis
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')
REDIS_URL = os.environ.get('REDIS_URL')

@app.route('/health')
def health():
    """Basic health check - process is running"""
    return jsonify({"status": "healthy"}), 200

@app.route('/health/live')
def liveness():
    """Liveness probe - is the process alive?
    Kubernetes restarts pod if this fails.
    """
    return jsonify({"status": "alive"}), 200

@app.route('/health/ready')
def readiness():
    """Readiness probe - can we serve traffic?
    LB removes from pool if this fails.
    """
    checks = {
        "database": check_database(),
        "cache": check_cache(),
        "dependencies": check_dependencies()
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return jsonify({
        "status": "ready" if all_healthy else "not ready",
        "checks": checks
    }), status_code

def check_database():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return True
    except Exception:
        return False

def check_cache():
    try:
        r = redis.Redis.from_url(REDIS_URL)
        r.ping()
        return True
    except Exception:
        return False

def check_dependencies():
    # Check external APIs, message queues, etc.
    return True
```

### Node.js Express Health Endpoints

```javascript
const express = require('express');
const { Pool } = require('pg');
const Redis = require('ioredis');

const app = express();
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const redis = new Redis(process.env.REDIS_URL);

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.get('/health/live', (req, res) => {
  res.json({ status: 'alive' });
});

app.get('/health/ready', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    cache: await checkCache(),
  };

  const allHealthy = Object.values(checks).every(v => v);
  const status = allHealthy ? 200 : 503;

  res.status(status).json({
    status: allHealthy ? 'ready' : 'not ready',
    checks
  });
});

async function checkDatabase() {
  try {
    await pool.query('SELECT 1');
    return true;
  } catch {
    return false;
  }
}

async function checkCache() {
  try {
    await redis.ping();
    return true;
  } catch {
    return false;
  }
}
```

### Go Health Endpoints

```go
package main

import (
    "context"
    "database/sql"
    "encoding/json"
    "net/http"
    "time"

    "github.com/go-redis/redis/v8"
    _ "github.com/lib/pq"
)

type HealthResponse struct {
    Status string            `json:"status"`
    Checks map[string]bool   `json:"checks,omitempty"`
}

var db *sql.DB
var rdb *redis.Client

func healthHandler(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(HealthResponse{Status: "healthy"})
}

func livenessHandler(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(HealthResponse{Status: "alive"})
}

func readinessHandler(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel()

    checks := map[string]bool{
        "database": checkDatabase(ctx),
        "cache":    checkCache(ctx),
    }

    allHealthy := true
    for _, v := range checks {
        if !v {
            allHealthy = false
            break
        }
    }

    status := "ready"
    httpStatus := http.StatusOK
    if !allHealthy {
        status = "not ready"
        httpStatus = http.StatusServiceUnavailable
    }

    w.WriteHeader(httpStatus)
    json.NewEncoder(w).Encode(HealthResponse{
        Status: status,
        Checks: checks,
    })
}

func checkDatabase(ctx context.Context) bool {
    return db.PingContext(ctx) == nil
}

func checkCache(ctx context.Context) bool {
    return rdb.Ping(ctx).Err() == nil
}
```

---

## HAProxy Configuration Examples

### Basic HTTP Load Balancing

```haproxy
global
    log /dev/log local0
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

frontend http_front
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    server web1 10.0.0.1:8080 check
    server web2 10.0.0.2:8080 check
    server web3 10.0.0.3:8080 check backup
```

### Production HA Setup with Rate Limiting

```haproxy
global
    log /dev/log local0
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

    # Performance tuning
    maxconn 20000
    nbthread 4
    cpu-map auto:1/1-4 0-3

    # SSL settings
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
    tune.ssl.default-dh-param 2048

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

    # Enable compression
    compression algo gzip
    compression type text/html text/plain text/css application/json

frontend main
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/ alpn h2,http/1.1

    # Redirect HTTP to HTTPS
    http-request redirect scheme https unless { ssl_fc }

    # Rate limiting - 100 req/10s per IP
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }

    # Security headers
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains"
    http-response set-header X-Frame-Options "SAMEORIGIN"
    http-response set-header X-Content-Type-Options "nosniff"

    # Route based on path
    acl is_api path_beg /api
    use_backend api_servers if is_api
    default_backend web_servers

backend web_servers
    balance leastconn
    option httpchk GET /health
    http-check expect status 200

    # Connection reuse
    option http-server-close
    option forwardfor

    # Servers with health checks
    server web1 10.0.0.1:8080 check weight 100 maxconn 5000
    server web2 10.0.0.2:8080 check weight 100 maxconn 5000
    server web3 10.0.0.3:8080 check weight 50 backup

backend api_servers
    balance roundrobin
    option httpchk GET /health/ready
    http-check expect status 200

    # Sticky sessions for stateful APIs
    cookie SERVERID insert indirect nocache

    server api1 10.0.1.1:8080 check cookie api1
    server api2 10.0.1.2:8080 check cookie api2
```

### TCP Load Balancing (Database, Redis)

```haproxy
frontend mysql_front
    bind *:3306
    mode tcp
    option tcplog
    default_backend mysql_servers

backend mysql_servers
    mode tcp
    balance roundrobin
    option tcp-check

    # MySQL health check
    tcp-check connect
    tcp-check send-binary 00000001  # COM_PING

    server mysql1 10.0.2.1:3306 check
    server mysql2 10.0.2.2:3306 check backup

frontend redis_front
    bind *:6379
    mode tcp
    default_backend redis_servers

backend redis_servers
    mode tcp
    balance first  # Always use first available
    option tcp-check

    tcp-check connect
    tcp-check send PING\r\n
    tcp-check expect string +PONG

    server redis1 10.0.3.1:6379 check
    server redis2 10.0.3.2:6379 check backup
```

---

## Nginx Configuration Examples

### Basic HTTP Load Balancing

```nginx
upstream web_backend {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080 backup;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://web_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Production Setup with All Features

```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

# Upstream with health checks and keepalive
upstream web_backend {
    least_conn;

    # Shared memory zone for state
    zone web_backend 64k;

    # Servers with weights and failure handling
    server 10.0.0.1:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:8080 weight=2 backup;

    # Connection reuse
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

upstream api_backend {
    zone api_backend 64k;

    # IP hash for session persistence
    ip_hash;

    server 10.0.1.1:8080;
    server 10.0.1.2:8080;

    keepalive 16;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

# Main HTTPS server
server {
    listen 443 ssl http2;
    server_name example.com;

    # SSL configuration
    ssl_certificate /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_min_length 1000;

    # Main application
    location / {
        proxy_pass http://web_backend;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # HTTP/1.1 for keepalive
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Error handling - retry on failure
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
    }

    # API with rate limiting
    location /api {
        limit_req zone=api_limit burst=20 nodelay;
        limit_conn conn_limit 10;

        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://web_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 3600s;
    }

    # Health check endpoint (bypass backend)
    location /nginx-health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

---

## Kubernetes Ingress Examples

### Basic Nginx Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```

### Production Ingress with TLS and Rate Limiting

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: production-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod

    # SSL
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"

    # Rate limiting
    nginx.ingress.kubernetes.io/limit-rps: "10"
    nginx.ingress.kubernetes.io/limit-connections: "5"

    # Request size
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"

    # Timeouts
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "5"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"

    # CORS
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://example.com"

    # Backend protocol
    nginx.ingress.kubernetes.io/backend-protocol: "HTTP"
spec:
  tls:
    - hosts:
        - api.example.com
        - www.example.com
      secretName: example-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: api-v1
                port:
                  number: 80
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: api-v2
                port:
                  number: 80
    - host: www.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-frontend
                port:
                  number: 80
```

### HAProxy Ingress Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: haproxy-ingress
  annotations:
    kubernetes.io/ingress.class: haproxy

    # SSL
    haproxy.org/ssl-redirect: "true"
    haproxy.org/ssl-certificate: "default/example-tls"

    # Load balancing
    haproxy.org/load-balance: "leastconn"

    # Rate limiting
    haproxy.org/rate-limit-requests: "100"
    haproxy.org/rate-limit-period: "10s"

    # Timeouts
    haproxy.org/timeout-connect: "5s"
    haproxy.org/timeout-server: "60s"
    haproxy.org/timeout-client: "60s"

    # Health checks
    haproxy.org/check: "true"
    haproxy.org/check-http: "/health"
    haproxy.org/check-interval: "10s"
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```

### Gateway API (Modern Alternative)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-gateway
spec:
  gatewayClassName: nginx
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - name: example-tls
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-route
spec:
  parentRefs:
    - name: production-gateway
  hostnames:
    - "api.example.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /v1
      backendRefs:
        - name: api-v1
          port: 80
    - matches:
        - path:
            type: PathPrefix
            value: /v2
      backendRefs:
        - name: api-v2
          port: 80
```

---

## Monitoring Examples

### Prometheus Scrape Config

```yaml
scrape_configs:
  - job_name: 'haproxy'
    static_configs:
      - targets: ['haproxy-exporter:9101']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'haproxy-prod'

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx-exporter:9113']
```

### Alert Rules

```yaml
groups:
  - name: load_balancer_alerts
    rules:
      - alert: BackendDown
        expr: haproxy_backend_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Backend {{ $labels.backend }} is down"
          description: "Backend has been down for more than 1 minute"

      - alert: HighErrorRate
        expr: |
          rate(haproxy_backend_http_responses_total{code="5xx"}[5m])
          / rate(haproxy_backend_http_responses_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High 5xx error rate on {{ $labels.backend }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            rate(haproxy_backend_http_response_time_seconds_bucket[5m])
          ) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency on {{ $labels.backend }}"

      - alert: ConnectionPoolExhausted
        expr: haproxy_backend_current_sessions / haproxy_backend_limit_sessions > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Connection pool near exhaustion on {{ $labels.backend }}"
```

---

*Load Balancing Examples | faion-cicd-engineer*
