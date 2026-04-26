# Load Balancing Examples

## HAProxy Configuration

### Basic L7 Load Balancer

```haproxy
# /etc/haproxy/haproxy.cfg

global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

    # SSL/TLS settings (TLS 1.2+)
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
    tune.ssl.default-dh-param 2048

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option  forwardfor
    option  http-server-close
    timeout connect 5s
    timeout client  30s
    timeout server  30s
    timeout http-keep-alive 10s

# Stats dashboard
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats admin if LOCALHOST

# HTTP to HTTPS redirect
frontend http_front
    bind *:80
    redirect scheme https code 301 if !{ ssl_fc }

# HTTPS frontend
frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/example.com.pem
    http-request add-header X-Forwarded-Proto https

    # ACL routing
    acl is_api path_beg /api
    acl is_static path_beg /static

    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend web_servers

# Web backend - Round Robin
backend web_servers
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200

    server web1 10.0.0.1:8080 check weight 5
    server web2 10.0.0.2:8080 check weight 5
    server web3 10.0.0.3:8080 check weight 3 backup

# API backend - Least Connections with Sticky Sessions
backend api_servers
    balance leastconn
    option httpchk GET /api/health
    http-check expect status 200

    # Cookie-based sticky sessions
    cookie SERVERID insert indirect nocache

    server api1 10.0.1.1:8000 check cookie api1
    server api2 10.0.1.2:8000 check cookie api2
    server api3 10.0.1.3:8000 check cookie api3

# Static backend - Round Robin
backend static_servers
    balance roundrobin
    option httpchk GET /health

    server static1 10.0.2.1:80 check
    server static2 10.0.2.2:80 check
```

### HAProxy L4 Load Balancer (TCP)

```haproxy
# /etc/haproxy/haproxy-l4.cfg

global
    log /dev/log local0
    chroot /var/lib/haproxy
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    tcp
    option  tcplog
    timeout connect 5s
    timeout client  30s
    timeout server  30s

# Database load balancing
frontend db_front
    bind *:5432
    default_backend postgres_servers

backend postgres_servers
    balance leastconn
    option tcp-check

    server db1 10.0.3.1:5432 check
    server db2 10.0.3.2:5432 check
    server db3 10.0.3.3:5432 check backup

# Redis cluster
frontend redis_front
    bind *:6379
    default_backend redis_servers

backend redis_servers
    balance roundrobin
    option tcp-check

    server redis1 10.0.4.1:6379 check
    server redis2 10.0.4.2:6379 check
```

## Nginx Configuration

### Basic Load Balancer

```nginx
# /etc/nginx/nginx.conf

upstream web_backend {
    least_conn;

    server 10.0.0.1:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:8080 weight=2 backup;

    keepalive 32;
}

upstream api_backend {
    ip_hash;  # Sticky sessions

    server 10.0.1.1:8000 max_fails=3 fail_timeout=30s;
    server 10.0.1.2:8000 max_fails=3 fail_timeout=30s;
    server 10.0.1.3:8000 max_fails=3 fail_timeout=30s;

    keepalive 16;
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;

    location / {
        proxy_pass http://web_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
    }

    location /api {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### Nginx Stream (L4) Load Balancer

```nginx
# /etc/nginx/stream.conf

stream {
    upstream postgres_backend {
        least_conn;
        server 10.0.3.1:5432 weight=5;
        server 10.0.3.2:5432 weight=5;
        server 10.0.3.3:5432 backup;
    }

    upstream redis_backend {
        hash $remote_addr consistent;
        server 10.0.4.1:6379;
        server 10.0.4.2:6379;
    }

    server {
        listen 5432;
        proxy_pass postgres_backend;
        proxy_connect_timeout 5s;
        proxy_timeout 1h;
    }

    server {
        listen 6379;
        proxy_pass redis_backend;
        proxy_connect_timeout 5s;
        proxy_timeout 1h;
    }
}
```

## AWS Application Load Balancer (Terraform)

```hcl
# alb.tf

resource "aws_lb" "main" {
  name               = "my-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = true
  enable_http2              = true

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.id
    prefix  = "alb"
    enabled = true
  }

  tags = {
    Environment = "production"
  }
}

# HTTPS Listener
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# HTTP to HTTPS redirect
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# Web Target Group
resource "aws_lb_target_group" "web" {
  name     = "web-targets"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200"
  }

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }

  deregistration_delay = 30

  tags = {
    Name = "web-targets"
  }
}

# API Target Group
resource "aws_lb_target_group" "api" {
  name     = "api-targets"
  port     = 8000
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/api/health"
    protocol            = "HTTP"
    matcher             = "200"
  }

  tags = {
    Name = "api-targets"
  }
}

# Listener Rule for API
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 10

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}

# Security Group
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "ALB security group"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb-sg"
  }
}
```

## AWS Network Load Balancer (Terraform)

```hcl
# nlb.tf

resource "aws_lb" "nlb" {
  name               = "my-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = var.public_subnet_ids

  enable_deletion_protection = true
  enable_cross_zone_load_balancing = true

  tags = {
    Environment = "production"
  }
}

resource "aws_lb_listener" "tcp" {
  load_balancer_arn = aws_lb.nlb.arn
  port              = "443"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tcp.arn
  }
}

resource "aws_lb_target_group" "tcp" {
  name        = "tcp-targets"
  port        = 8080
  protocol    = "TCP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 10
    protocol            = "TCP"
  }

  stickiness {
    type    = "source_ip"
    enabled = true
  }

  tags = {
    Name = "tcp-targets"
  }
}
```

## Kubernetes Load Balancing

### Service Types

```yaml
# ClusterIP (internal only)
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
---
# NodePort (external via node ports)
apiVersion: v1
kind: Service
metadata:
  name: web-nodeport
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080
---
# LoadBalancer (cloud provider LB)
apiVersion: v1
kind: Service
metadata:
  name: web-loadbalancer
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 443
      targetPort: 8080
```

### Ingress with Nginx Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "SERVERID"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "86400"
spec:
  tls:
    - hosts:
        - example.com
      secretName: example-tls
  rules:
    - host: example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```

### Ingress with Traefik

```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: web-ingress
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`example.com`) && PathPrefix(`/api`)
      kind: Rule
      services:
        - name: api-service
          port: 80
          sticky:
            cookie:
              name: traefik_sticky
              secure: true
              httpOnly: true
    - match: Host(`example.com`)
      kind: Rule
      services:
        - name: web-service
          port: 80
  tls:
    secretName: example-tls
```

## Health Check Endpoint Examples

### Python (FastAPI)

```python
from fastapi import FastAPI, Response
import redis
import psycopg2
import os

app = FastAPI()

@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy"}

@app.get("/health/ready")
async def readiness_check():
    """Readiness check with dependencies"""
    checks = {
        "status": "healthy",
        "checks": {}
    }

    # Database check
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        conn.close()
        checks["checks"]["database"] = "healthy"
    except Exception as e:
        checks["checks"]["database"] = f"unhealthy: {str(e)}"
        checks["status"] = "unhealthy"

    # Redis check
    try:
        r = redis.from_url(os.environ["REDIS_URL"])
        r.ping()
        checks["checks"]["redis"] = "healthy"
    except Exception as e:
        checks["checks"]["redis"] = f"unhealthy: {str(e)}"
        checks["status"] = "unhealthy"

    status_code = 200 if checks["status"] == "healthy" else 503
    return Response(
        content=json.dumps(checks),
        status_code=status_code,
        media_type="application/json"
    )

@app.get("/health/live")
async def liveness_check():
    """Liveness check (is the process alive?)"""
    return {"status": "alive"}
```

### Node.js (Express)

```javascript
const express = require('express');
const { Pool } = require('pg');
const Redis = require('ioredis');

const app = express();

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.get('/health/ready', async (req, res) => {
  const checks = {
    status: 'healthy',
    checks: {}
  };

  // Database check
  try {
    const pool = new Pool({ connectionString: process.env.DATABASE_URL });
    await pool.query('SELECT 1');
    await pool.end();
    checks.checks.database = 'healthy';
  } catch (error) {
    checks.checks.database = `unhealthy: ${error.message}`;
    checks.status = 'unhealthy';
  }

  // Redis check
  try {
    const redis = new Redis(process.env.REDIS_URL);
    await redis.ping();
    await redis.quit();
    checks.checks.redis = 'healthy';
  } catch (error) {
    checks.checks.redis = `unhealthy: ${error.message}`;
    checks.status = 'unhealthy';
  }

  const statusCode = checks.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(checks);
});

app.get('/health/live', (req, res) => {
  res.json({ status: 'alive' });
});
```

### Go

```go
package main

import (
    "database/sql"
    "encoding/json"
    "net/http"
    "os"

    "github.com/go-redis/redis/v8"
    _ "github.com/lib/pq"
)

type HealthResponse struct {
    Status string            `json:"status"`
    Checks map[string]string `json:"checks,omitempty"`
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(HealthResponse{Status: "healthy"})
}

func readinessHandler(w http.ResponseWriter, r *http.Request) {
    response := HealthResponse{
        Status: "healthy",
        Checks: make(map[string]string),
    }

    // Database check
    db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
    if err != nil {
        response.Checks["database"] = "unhealthy: " + err.Error()
        response.Status = "unhealthy"
    } else {
        defer db.Close()
        if err := db.Ping(); err != nil {
            response.Checks["database"] = "unhealthy: " + err.Error()
            response.Status = "unhealthy"
        } else {
            response.Checks["database"] = "healthy"
        }
    }

    // Redis check
    rdb := redis.NewClient(&redis.Options{
        Addr: os.Getenv("REDIS_URL"),
    })
    defer rdb.Close()
    if _, err := rdb.Ping(r.Context()).Result(); err != nil {
        response.Checks["redis"] = "unhealthy: " + err.Error()
        response.Status = "unhealthy"
    } else {
        response.Checks["redis"] = "healthy"
    }

    if response.Status == "unhealthy" {
        w.WriteHeader(http.StatusServiceUnavailable)
    }
    json.NewEncoder(w).Encode(response)
}

func livenessHandler(w http.ResponseWriter, r *http.Request) {
    json.NewEncoder(w).Encode(HealthResponse{Status: "alive"})
}

func main() {
    http.HandleFunc("/health", healthHandler)
    http.HandleFunc("/health/ready", readinessHandler)
    http.HandleFunc("/health/live", livenessHandler)
    http.ListenAndServe(":8080", nil)
}
```

---

*Load Balancing Examples | faion-cicd-engineer*
