# Load Balancing Templates

## HAProxy Templates

### Template: Production HAProxy Configuration

```haproxy
# /etc/haproxy/haproxy.cfg
# Template: Production L7 Load Balancer
# Replace: {{DOMAIN}}, {{CERT_PATH}}, {{BACKEND_*}}

global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    maxconn 50000

    # Modern TLS settings
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
    ssl-default-server-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-server-options ssl-min-ver TLSv1.2 no-tls-tickets
    tune.ssl.default-dh-param 2048

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option  forwardfor
    option  http-server-close
    option  redispatch
    retries 3
    timeout connect 5s
    timeout client  30s
    timeout server  30s
    timeout http-keep-alive 10s
    timeout http-request 10s
    timeout queue 30s
    maxconn 10000

    # Error pages
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

# Stats dashboard (restrict in production)
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats admin if LOCALHOST
    stats auth admin:{{STATS_PASSWORD}}

# HTTP to HTTPS redirect
frontend http_front
    bind *:80
    http-request redirect scheme https code 301 unless { ssl_fc }

# HTTPS frontend
frontend https_front
    bind *:443 ssl crt {{CERT_PATH}}/{{DOMAIN}}.pem alpn h2,http/1.1

    # Security headers
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    http-response set-header X-Content-Type-Options nosniff
    http-response set-header X-Frame-Options DENY
    http-response set-header X-XSS-Protection "1; mode=block"

    # Forwarded headers
    http-request set-header X-Forwarded-Proto https
    http-request set-header X-Real-IP %[src]

    # Rate limiting (100 req/10s per IP)
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }

    # Routing ACLs
    acl is_api path_beg /api
    acl is_ws hdr(Upgrade) -i websocket

    use_backend ws_servers if is_ws
    use_backend api_servers if is_api
    default_backend web_servers

# Web backend
backend web_servers
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200

    # Connection draining
    default-server inter 10s fall 3 rise 2 on-marked-down shutdown-sessions

    server web1 {{BACKEND_WEB1}}:8080 check weight 100
    server web2 {{BACKEND_WEB2}}:8080 check weight 100
    server web3 {{BACKEND_WEB3}}:8080 check weight 50 backup

# API backend with sticky sessions
backend api_servers
    balance leastconn
    option httpchk GET /api/health
    http-check expect status 200

    # Sticky sessions via cookie
    cookie SERVERID insert indirect nocache httponly secure

    default-server inter 10s fall 3 rise 2

    server api1 {{BACKEND_API1}}:8000 check cookie api1
    server api2 {{BACKEND_API2}}:8000 check cookie api2
    server api3 {{BACKEND_API3}}:8000 check cookie api3

# WebSocket backend
backend ws_servers
    balance source
    option httpchk GET /health

    # WebSocket timeouts
    timeout tunnel 1h

    server ws1 {{BACKEND_WS1}}:8080 check
    server ws2 {{BACKEND_WS2}}:8080 check
```

### Template: HAProxy L4 TCP Load Balancer

```haproxy
# /etc/haproxy/haproxy-tcp.cfg
# Template: L4 TCP Load Balancer
# Replace: {{SERVICE}}, {{PORT}}, {{BACKEND_*}}

global
    log /dev/log local0
    chroot /var/lib/haproxy
    user haproxy
    group haproxy
    daemon
    maxconn 50000

defaults
    log     global
    mode    tcp
    option  tcplog
    option  dontlognull
    timeout connect 5s
    timeout client  1h
    timeout server  1h
    maxconn 10000

# {{SERVICE}} Load Balancer
frontend {{SERVICE}}_front
    bind *:{{PORT}}
    default_backend {{SERVICE}}_servers

backend {{SERVICE}}_servers
    balance leastconn
    option tcp-check

    # Health check
    tcp-check connect

    default-server inter 10s fall 3 rise 2

    server {{SERVICE}}1 {{BACKEND_1}}:{{PORT}} check
    server {{SERVICE}}2 {{BACKEND_2}}:{{PORT}} check
    server {{SERVICE}}3 {{BACKEND_3}}:{{PORT}} check backup
```

## Nginx Templates

### Template: Production Nginx Load Balancer

```nginx
# /etc/nginx/nginx.conf
# Template: Production L7 Load Balancer
# Replace: {{DOMAIN}}, {{UPSTREAM_*}}

user nginx;
worker_processes auto;
worker_rlimit_nofile 65535;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;

events {
    worker_connections 10240;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main buffer=16k;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript
               application/xml application/xml+rss text/javascript;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    # Upstreams
    upstream web_backend {
        least_conn;
        keepalive 32;

        server {{UPSTREAM_WEB1}}:8080 weight=5 max_fails=3 fail_timeout=30s;
        server {{UPSTREAM_WEB2}}:8080 weight=5 max_fails=3 fail_timeout=30s;
        server {{UPSTREAM_WEB3}}:8080 weight=2 backup;
    }

    upstream api_backend {
        ip_hash;
        keepalive 16;

        server {{UPSTREAM_API1}}:8000 max_fails=3 fail_timeout=30s;
        server {{UPSTREAM_API2}}:8000 max_fails=3 fail_timeout=30s;
        server {{UPSTREAM_API3}}:8000 max_fails=3 fail_timeout=30s;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        listen [::]:80;
        server_name {{DOMAIN}};
        return 301 https://$host$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name {{DOMAIN}};

        # SSL
        ssl_certificate /etc/nginx/ssl/{{DOMAIN}}.crt;
        ssl_certificate_key /etc/nginx/ssl/{{DOMAIN}}.key;
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_session_tickets off;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Content-Type-Options nosniff always;
        add_header X-Frame-Options DENY always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Connection limits
        limit_conn conn_limit 20;

        # Proxy settings
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Web application
        location / {
            proxy_pass http://web_backend;
            proxy_connect_timeout 5s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
            proxy_next_upstream_tries 3;
        }

        # API
        location /api {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://api_backend;
            proxy_connect_timeout 5s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

## Terraform Templates

### Template: AWS ALB

```hcl
# alb.tf
# Template: AWS Application Load Balancer
# Replace: {{PROJECT}}, {{ENVIRONMENT}}, {{VPC_ID}}, {{SUBNET_IDS}}, {{CERTIFICATE_ARN}}

variable "project" {
  default = "{{PROJECT}}"
}

variable "environment" {
  default = "{{ENVIRONMENT}}"
}

variable "vpc_id" {
  default = "{{VPC_ID}}"
}

variable "public_subnet_ids" {
  type    = list(string)
  default = {{SUBNET_IDS}}
}

variable "certificate_arn" {
  default = "{{CERTIFICATE_ARN}}"
}

# ALB
resource "aws_lb" "main" {
  name               = "${var.project}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.environment == "production" ? true : false
  enable_http2              = true
  idle_timeout              = 60

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.id
    prefix  = "alb"
    enabled = true
  }

  tags = {
    Name        = "${var.project}-${var.environment}-alb"
    Project     = var.project
    Environment = var.environment
  }
}

# HTTPS Listener
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# HTTP Redirect
resource "aws_lb_listener" "http_redirect" {
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
  name                 = "${var.project}-${var.environment}-web"
  port                 = 8080
  protocol             = "HTTP"
  vpc_id               = var.vpc_id
  target_type          = "instance"
  deregistration_delay = 30

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
    enabled         = false
  }

  tags = {
    Name        = "${var.project}-${var.environment}-web"
    Project     = var.project
    Environment = var.environment
  }
}

# API Target Group
resource "aws_lb_target_group" "api" {
  name                 = "${var.project}-${var.environment}-api"
  port                 = 8000
  protocol             = "HTTP"
  vpc_id               = var.vpc_id
  target_type          = "instance"
  deregistration_delay = 30

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
    Name        = "${var.project}-${var.environment}-api"
    Project     = var.project
    Environment = var.environment
  }
}

# API Listener Rule
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
  name        = "${var.project}-${var.environment}-alb-sg"
  description = "ALB security group"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP (redirect only)"
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
    Name        = "${var.project}-${var.environment}-alb-sg"
    Project     = var.project
    Environment = var.environment
  }
}

# S3 Bucket for logs
resource "aws_s3_bucket" "lb_logs" {
  bucket = "${var.project}-${var.environment}-alb-logs"

  tags = {
    Name        = "${var.project}-${var.environment}-alb-logs"
    Project     = var.project
    Environment = var.environment
  }
}

# Outputs
output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "alb_zone_id" {
  value = aws_lb.main.zone_id
}

output "web_target_group_arn" {
  value = aws_lb_target_group.web.arn
}

output "api_target_group_arn" {
  value = aws_lb_target_group.api.arn
}
```

## Kubernetes Templates

### Template: Ingress with Nginx Controller

```yaml
# ingress.yaml
# Template: Kubernetes Ingress with Nginx
# Replace: {{DOMAIN}}, {{TLS_SECRET}}, {{NAMESPACE}}

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: {{NAMESPACE}}
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "5"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    # Rate limiting
    nginx.ingress.kubernetes.io/limit-rps: "100"
    nginx.ingress.kubernetes.io/limit-connections: "20"
    # Sticky sessions (optional)
    # nginx.ingress.kubernetes.io/affinity: "cookie"
    # nginx.ingress.kubernetes.io/session-cookie-name: "SERVERID"
    # nginx.ingress.kubernetes.io/session-cookie-max-age: "86400"
spec:
  tls:
    - hosts:
        - {{DOMAIN}}
      secretName: {{TLS_SECRET}}
  rules:
    - host: {{DOMAIN}}
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

### Template: Service with LoadBalancer

```yaml
# service-lb.yaml
# Template: Kubernetes Service with Cloud Load Balancer
# Replace: {{APP_NAME}}, {{NAMESPACE}}, {{PORT}}, {{TARGET_PORT}}

apiVersion: v1
kind: Service
metadata:
  name: {{APP_NAME}}-lb
  namespace: {{NAMESPACE}}
  annotations:
    # AWS NLB
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    service.beta.kubernetes.io/aws-load-balancer-connection-draining-enabled: "true"
    service.beta.kubernetes.io/aws-load-balancer-connection-draining-timeout: "30"
    # GCP (uncomment if using GCP)
    # cloud.google.com/load-balancer-type: "Internal"
    # Azure (uncomment if using Azure)
    # service.beta.kubernetes.io/azure-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  selector:
    app: {{APP_NAME}}
  ports:
    - name: http
      port: {{PORT}}
      targetPort: {{TARGET_PORT}}
      protocol: TCP
  sessionAffinity: None  # or "ClientIP" for sticky sessions
  externalTrafficPolicy: Local  # Preserves client IP
```

## Health Check Templates

### Template: Health Check Endpoint (Python/FastAPI)

```python
# health.py
# Template: Comprehensive Health Check Endpoint
# Replace: {{DATABASE_URL}}, {{REDIS_URL}}, {{APP_NAME}}

from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Dict, Optional
import asyncio
import aioredis
import asyncpg
import os
import time

app = FastAPI()

class HealthStatus(BaseModel):
    status: str
    version: str
    checks: Dict[str, str]
    latency_ms: Optional[int] = None

APP_VERSION = os.getenv("APP_VERSION", "unknown")
DATABASE_URL = os.getenv("DATABASE_URL", "{{DATABASE_URL}}")
REDIS_URL = os.getenv("REDIS_URL", "{{REDIS_URL}}")

@app.get("/health")
async def health():
    """Basic health check - always returns 200 if app is running"""
    return {"status": "healthy", "app": "{{APP_NAME}}"}

@app.get("/health/live")
async def liveness():
    """Liveness probe - is the process alive?"""
    return {"status": "alive"}

@app.get("/health/ready", response_model=HealthStatus)
async def readiness(response: Response):
    """Readiness probe - is the app ready to serve traffic?"""
    start = time.time()
    checks = {}
    status = "healthy"

    # Database check
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.fetchval("SELECT 1")
        await conn.close()
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)[:50]}"
        status = "unhealthy"

    # Redis check
    try:
        redis = await aioredis.from_url(REDIS_URL)
        await redis.ping()
        await redis.close()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)[:50]}"
        status = "unhealthy"

    latency_ms = int((time.time() - start) * 1000)

    if status == "unhealthy":
        response.status_code = 503

    return HealthStatus(
        status=status,
        version=APP_VERSION,
        checks=checks,
        latency_ms=latency_ms
    )

@app.get("/health/startup")
async def startup():
    """Startup probe - has the app finished initializing?"""
    # Add any initialization checks here
    return {"status": "started", "version": APP_VERSION}
```

---

*Load Balancing Templates | faion-cicd-engineer*
