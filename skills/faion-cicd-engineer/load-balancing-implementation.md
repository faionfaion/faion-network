---
id: load-balancing-implementation
name: "Load Balancing Implementation"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Load Balancing Implementation

## Overview

Implementation guide for load balancing health checks, best practices, and production-ready templates. Covers monitoring, security, and performance optimization.

## Health Checks

### Health Check Types

```yaml
health_checks:
  tcp:
    description: "TCP connection check"
    use_case: "Basic connectivity"
    example:
      haproxy: "option tcp-check"
      nginx: "server ... check"

  http:
    description: "HTTP endpoint check"
    use_case: "Application health"
    example:
      endpoint: "/health"
      expected_status: 200
      expected_body: "OK"

  https:
    description: "HTTPS endpoint check"
    use_case: "SSL-enabled services"
    verify_ssl: true

  script:
    description: "Custom script check"
    use_case: "Complex health logic"
    example: "/usr/local/bin/check-app.sh"

  grpc:
    description: "gRPC health check"
    use_case: "gRPC services"
    example: "grpc.health.v1.Health/Check"
```

### Health Check Implementation

```python
# Python Flask health endpoint
from flask import Flask, jsonify
import psycopg2
import redis

app = Flask(__name__)

@app.route('/health')
def health():
    """Basic health check"""
    return jsonify({"status": "healthy"}), 200

@app.route('/health/live')
def liveness():
    """Liveness probe - is the process running?"""
    return jsonify({"status": "alive"}), 200

@app.route('/health/ready')
def readiness():
    """Readiness probe - can we serve traffic?"""
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
        conn.close()
        return True
    except:
        return False

def check_cache():
    try:
        r = redis.Redis.from_url(REDIS_URL)
        r.ping()
        return True
    except:
        return False
```

## Best Practices

### High Availability

1. **Multiple LB instances** - Avoid single point of failure
2. **Cross-zone balancing** - Distribute across AZs
3. **Health check tuning** - Balance sensitivity and stability
4. **Graceful degradation** - Handle partial failures

### Performance

1. **Connection pooling** - Reduce connection overhead
2. **Keepalive connections** - Reuse backend connections
3. **SSL termination** - Offload to load balancer
4. **Caching** - Cache static content at LB

### Security

1. **DDoS protection** - Rate limiting, WAF
2. **SSL/TLS** - Use TLS 1.2+ only
3. **Security groups** - Restrict access
4. **Access logging** - Audit trail

### Monitoring

1. **Metrics collection** - Response times, error rates
2. **Alerting** - Unhealthy backends, high latency
3. **Logging** - Request logging for troubleshooting
4. **Dashboards** - Real-time visibility

## Production Templates

### Terraform AWS ALB

```hcl
resource "aws_lb" "main" {
  name               = "main-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = true

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.bucket
    prefix  = "alb"
    enabled = true
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_lb_target_group" "web" {
  name     = "web-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}
```

### HAProxy High Availability Setup

```haproxy
# Active-Passive HA with keepalived

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
    nbproc 4
    cpu-map auto:1/1-4 0-3

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

frontend main
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/

    # Rate limiting
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny if { sc_http_req_rate(0) gt 100 }

    default_backend web_servers

backend web_servers
    balance leastconn
    option httpchk GET /health

    # Connection reuse
    option http-server-close
    option forwardfor

    server web1 10.0.0.1:8080 check weight 100 maxconn 5000
    server web2 10.0.0.2:8080 check weight 100 maxconn 5000
    server web3 10.0.0.3:8080 check weight 50 backup
```

### Nginx with Advanced Features

```nginx
upstream web_backend {
    least_conn;

    # Zone for shared state
    zone web_backend 64k;

    # Servers
    server 10.0.0.1:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:8080 weight=2 backup;

    # Connection reuse
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

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

        # Error handling
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
    }

    location /api {
        # Rate limiting
        limit_req zone=api_limit burst=20 nodelay;
        limit_conn addr 10;

        proxy_pass http://web_backend;
    }
}
```

### Kubernetes Production Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: production-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/limit-rps: "10"
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://example.com"
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
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
```

## Monitoring Examples

### Prometheus Metrics

```yaml
# HAProxy exporter
scrape_configs:
  - job_name: 'haproxy'
    static_configs:
      - targets: ['haproxy:9101']

# Nginx exporter
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:9113']

# Alert rules
groups:
  - name: load_balancer
    rules:
      - alert: BackendDown
        expr: haproxy_backend_up == 0
        for: 1m
        annotations:
          summary: "Backend {{ $labels.backend }} is down"

      - alert: HighErrorRate
        expr: rate(haproxy_backend_http_responses_total{code="5xx"}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High 5xx error rate on {{ $labels.backend }}"
```

## Sources

- [HAProxy Best Practices](https://www.haproxy.com/blog/haproxy-best-practices/)
- [Nginx Performance Tuning](https://www.nginx.com/blog/tuning-nginx/)
- [AWS ALB Best Practices](https://aws.amazon.com/blogs/aws/new-application-load-balancer/)
- [K8s Ingress Patterns](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Terraform AWS Modules](https://registry.terraform.io/modules/terraform-aws-modules/alb/aws/)
