# Load Balancing Templates

Ready-to-use templates for common load balancing scenarios.

## HAProxy Templates

### Template: Production Web Application

```haproxy
# /etc/haproxy/haproxy.cfg
# Template: Production Web Application Load Balancer

global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    maxconn 50000

    # TLS 1.2+ with strong ciphers
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
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
    timeout http-request 10s
    timeout http-keep-alive 10s
    timeout queue 30s

# Stats dashboard (restrict in production)
listen stats
    bind 127.0.0.1:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats admin if LOCALHOST
    stats hide-version

# HTTP redirect to HTTPS
frontend http_redirect
    bind *:80
    http-request redirect scheme https code 301 unless { ssl_fc }

# HTTPS frontend
frontend https_in
    bind *:443 ssl crt /etc/haproxy/certs/ alpn h2,http/1.1

    # Security headers
    http-response set-header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    http-response set-header X-Content-Type-Options nosniff
    http-response set-header X-Frame-Options DENY

    # Forwarded headers
    http-request set-header X-Forwarded-Proto https
    http-request set-header X-Forwarded-Port %[dst_port]

    # Rate limiting (100 req/10s per IP)
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }

    # Routing
    acl is_api path_beg /api
    use_backend api_backend if is_api
    default_backend web_backend

# Web backend
backend web_backend
    balance roundrobin
    option httpchk GET /health HTTP/1.1\r\nHost:\ localhost
    http-check expect status 200

    # Connection draining
    option redispatch
    retries 3

    server web1 {{WEB_SERVER_1}}:{{WEB_PORT}} check inter 10s fall 3 rise 2 weight 100
    server web2 {{WEB_SERVER_2}}:{{WEB_PORT}} check inter 10s fall 3 rise 2 weight 100
    server web3 {{WEB_SERVER_3}}:{{WEB_PORT}} check inter 10s fall 3 rise 2 weight 50 backup

# API backend
backend api_backend
    balance leastconn
    option httpchk GET /api/health HTTP/1.1\r\nHost:\ localhost
    http-check expect status 200

    # Sticky sessions
    cookie SERVERID insert indirect nocache httponly secure

    server api1 {{API_SERVER_1}}:{{API_PORT}} check cookie s1
    server api2 {{API_SERVER_2}}:{{API_PORT}} check cookie s2
    server api3 {{API_SERVER_3}}:{{API_PORT}} check cookie s3
```

### Template: TCP Load Balancer (Database/Redis)

```haproxy
# /etc/haproxy/haproxy.cfg
# Template: TCP Load Balancer for Databases

global
    log /dev/log local0
    maxconn 10000
    user haproxy
    group haproxy
    daemon

defaults
    mode tcp
    log global
    option tcplog
    option dontlognull
    timeout connect 10s
    timeout client 1h
    timeout server 1h
    retries 3

# PostgreSQL primary (read-write)
frontend pg_primary
    bind *:5432
    default_backend pg_primary_backend

backend pg_primary_backend
    option pgsql-check user haproxy
    server pg1 {{PG_PRIMARY}}:5432 check inter 3s fall 3 rise 2

# PostgreSQL replicas (read-only)
frontend pg_replicas
    bind *:5433
    default_backend pg_replicas_backend

backend pg_replicas_backend
    balance roundrobin
    option pgsql-check user haproxy

    server pg_replica1 {{PG_REPLICA_1}}:5432 check inter 3s
    server pg_replica2 {{PG_REPLICA_2}}:5432 check inter 3s
    server pg_replica3 {{PG_REPLICA_3}}:5432 check inter 3s backup

# Redis cluster
frontend redis
    bind *:6379
    default_backend redis_backend

backend redis_backend
    balance first
    option tcp-check
    tcp-check send PING\r\n
    tcp-check expect string +PONG

    server redis1 {{REDIS_1}}:6379 check inter 1s
    server redis2 {{REDIS_2}}:6379 check inter 1s
    server redis3 {{REDIS_3}}:6379 check inter 1s
```

## Nginx Templates

### Template: Production Web Application

```nginx
# /etc/nginx/nginx.conf
# Template: Production Web Application Load Balancer

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript application/xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=web_limit:10m rate=50r/s;

    # Upstreams
    upstream web_backend {
        least_conn;

        server {{WEB_SERVER_1}}:{{WEB_PORT}} weight=5 max_fails=3 fail_timeout=30s;
        server {{WEB_SERVER_2}}:{{WEB_PORT}} weight=5 max_fails=3 fail_timeout=30s;
        server {{WEB_SERVER_3}}:{{WEB_PORT}} weight=2 backup;

        keepalive 32;
    }

    upstream api_backend {
        least_conn;

        server {{API_SERVER_1}}:{{API_PORT}} weight=5;
        server {{API_SERVER_2}}:{{API_PORT}} weight=5;
        server {{API_SERVER_3}}:{{API_PORT}} weight=5;

        keepalive 64;
    }

    # HTTP redirect
    server {
        listen 80;
        server_name {{DOMAIN}};
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name {{DOMAIN}};

        ssl_certificate /etc/nginx/ssl/{{DOMAIN}}.crt;
        ssl_certificate_key /etc/nginx/ssl/{{DOMAIN}}.key;
        ssl_session_timeout 1d;
        ssl_session_cache shared:SSL:50m;
        ssl_session_tickets off;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # HSTS
        add_header Strict-Transport-Security "max-age=63072000" always;

        # Web routes
        location / {
            limit_req zone=web_limit burst=20 nodelay;

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
        }

        # API routes
        location /api {
            limit_req zone=api_limit burst=50 nodelay;

            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            proxy_connect_timeout 5s;
            proxy_send_timeout 120s;
            proxy_read_timeout 120s;
        }

        # Health check
        location /nginx-health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

## Kubernetes Templates

### Template: Complete Ingress Setup

```yaml
# kubernetes/ingress.yaml
# Template: Production Ingress with TLS

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-ingress-config
data:
  proxy-connect-timeout: "5"
  proxy-read-timeout: "60"
  proxy-send-timeout: "60"
  proxy-body-size: "10m"
  use-forwarded-headers: "true"
  enable-real-ip: "true"

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{APP_NAME}}-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "5"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
    # Rate limiting
    nginx.ingress.kubernetes.io/limit-rps: "100"
    nginx.ingress.kubernetes.io/limit-connections: "50"
    # TLS with cert-manager
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - {{DOMAIN}}
        - api.{{DOMAIN}}
      secretName: {{APP_NAME}}-tls
  rules:
    - host: {{DOMAIN}}
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: {{APP_NAME}}-api
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{APP_NAME}}-web
                port:
                  number: 80
    - host: api.{{DOMAIN}}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{APP_NAME}}-api
                port:
                  number: 80

---
# Service for web
apiVersion: v1
kind: Service
metadata:
  name: {{APP_NAME}}-web
spec:
  type: ClusterIP
  selector:
    app: {{APP_NAME}}
    component: web
  ports:
    - port: 80
      targetPort: 8080

---
# Service for API
apiVersion: v1
kind: Service
metadata:
  name: {{APP_NAME}}-api
spec:
  type: ClusterIP
  selector:
    app: {{APP_NAME}}
    component: api
  ports:
    - port: 80
      targetPort: 8000
```

### Template: AWS Load Balancer Controller

```yaml
# kubernetes/aws-lb.yaml
# Template: AWS ALB via Load Balancer Controller

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{APP_NAME}}-alb
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
    alb.ingress.kubernetes.io/ssl-redirect: "443"
    alb.ingress.kubernetes.io/certificate-arn: {{ACM_CERT_ARN}}
    alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS13-1-2-2021-06
    alb.ingress.kubernetes.io/healthcheck-path: /health
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: "15"
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: "5"
    alb.ingress.kubernetes.io/healthy-threshold-count: "2"
    alb.ingress.kubernetes.io/unhealthy-threshold-count: "3"
    # Sticky sessions
    alb.ingress.kubernetes.io/target-group-attributes: stickiness.enabled=true,stickiness.lb_cookie.duration_seconds=86400
spec:
  rules:
    - host: {{DOMAIN}}
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: {{APP_NAME}}-api
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{APP_NAME}}-web
                port:
                  number: 80
```

## Terraform Templates

### Template: AWS ALB

```hcl
# terraform/alb.tf
# Template: AWS Application Load Balancer

variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "vpc_id" {
  type = string
}

variable "public_subnet_ids" {
  type = list(string)
}

variable "certificate_arn" {
  type = string
}

variable "health_check_path" {
  type    = string
  default = "/health"
}

# Security Group
resource "aws_security_group" "alb" {
  name        = "${var.name}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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
    Name = "${var.name}-alb-sg"
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = true
  enable_http2               = true

  access_logs {
    bucket  = aws_s3_bucket.alb_logs.bucket
    prefix  = var.name
    enabled = true
  }

  tags = {
    Name        = "${var.name}-alb"
    Environment = terraform.workspace
  }
}

# Target Group
resource "aws_lb_target_group" "main" {
  name                 = "${var.name}-tg"
  port                 = 8080
  protocol             = "HTTP"
  vpc_id               = var.vpc_id
  target_type          = "ip"
  deregistration_delay = 30

  health_check {
    enabled             = true
    path                = var.health_check_path
    port                = "traffic-port"
    protocol            = "HTTP"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    matcher             = "200"
  }

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }

  tags = {
    Name = "${var.name}-tg"
  }
}

# HTTPS Listener
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}

# HTTP to HTTPS Redirect
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
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

# Outputs
output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "alb_zone_id" {
  value = aws_lb.main.zone_id
}

output "target_group_arn" {
  value = aws_lb_target_group.main.arn
}
```

### Template: GCP Load Balancer

```hcl
# terraform/gcp-lb.tf
# Template: GCP HTTP(S) Load Balancer

variable "project_id" {
  type = string
}

variable "name" {
  type = string
}

variable "domain" {
  type = string
}

# Backend Service
resource "google_compute_backend_service" "main" {
  name                  = "${var.name}-backend"
  project               = var.project_id
  protocol              = "HTTP"
  port_name             = "http"
  timeout_sec           = 30
  enable_cdn            = true
  load_balancing_scheme = "EXTERNAL"

  health_checks = [google_compute_health_check.main.id]

  backend {
    group           = google_compute_instance_group_manager.main.instance_group
    balancing_mode  = "UTILIZATION"
    capacity_scaler = 1.0
  }

  cdn_policy {
    cache_key_policy {
      include_host         = true
      include_protocol     = true
      include_query_string = false
    }
  }
}

# Health Check
resource "google_compute_health_check" "main" {
  name    = "${var.name}-health-check"
  project = var.project_id

  check_interval_sec  = 10
  timeout_sec         = 5
  healthy_threshold   = 2
  unhealthy_threshold = 3

  http_health_check {
    port         = 8080
    request_path = "/health"
  }
}

# URL Map
resource "google_compute_url_map" "main" {
  name            = "${var.name}-url-map"
  project         = var.project_id
  default_service = google_compute_backend_service.main.id
}

# HTTPS Proxy
resource "google_compute_target_https_proxy" "main" {
  name             = "${var.name}-https-proxy"
  project          = var.project_id
  url_map          = google_compute_url_map.main.id
  ssl_certificates = [google_compute_managed_ssl_certificate.main.id]
}

# Managed SSL Certificate
resource "google_compute_managed_ssl_certificate" "main" {
  name    = "${var.name}-cert"
  project = var.project_id

  managed {
    domains = [var.domain]
  }
}

# Global Forwarding Rule (HTTPS)
resource "google_compute_global_forwarding_rule" "https" {
  name       = "${var.name}-https-rule"
  project    = var.project_id
  target     = google_compute_target_https_proxy.main.id
  port_range = "443"
  ip_address = google_compute_global_address.main.address
}

# HTTP to HTTPS Redirect
resource "google_compute_url_map" "http_redirect" {
  name    = "${var.name}-http-redirect"
  project = var.project_id

  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}

resource "google_compute_target_http_proxy" "redirect" {
  name    = "${var.name}-http-proxy"
  project = var.project_id
  url_map = google_compute_url_map.http_redirect.id
}

resource "google_compute_global_forwarding_rule" "http" {
  name       = "${var.name}-http-rule"
  project    = var.project_id
  target     = google_compute_target_http_proxy.redirect.id
  port_range = "80"
  ip_address = google_compute_global_address.main.address
}

# Static IP
resource "google_compute_global_address" "main" {
  name    = "${var.name}-ip"
  project = var.project_id
}

# Outputs
output "load_balancer_ip" {
  value = google_compute_global_address.main.address
}
```

## Docker Compose Templates

### Template: HAProxy with Docker Compose

```yaml
# docker-compose.yml
# Template: HAProxy Load Balancer with Docker Compose

version: '3.8'

services:
  haproxy:
    image: haproxy:2.9-alpine
    container_name: haproxy
    ports:
      - "80:80"
      - "443:443"
      - "8404:8404"
    volumes:
      - ./haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
      - ./certs:/etc/haproxy/certs:ro
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "haproxy", "-c", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
      interval: 30s
      timeout: 10s
      retries: 3

  web1:
    image: {{WEB_IMAGE}}
    container_name: web1
    networks:
      - backend
    environment:
      - PORT=8080
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  web2:
    image: {{WEB_IMAGE}}
    container_name: web2
    networks:
      - backend
    environment:
      - PORT=8080
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  api1:
    image: {{API_IMAGE}}
    container_name: api1
    networks:
      - backend
    environment:
      - PORT=8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  api2:
    image: {{API_IMAGE}}
    container_name: api2
    networks:
      - backend
    environment:
      - PORT=8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  backend:
    driver: bridge
```

## Variables Reference

Replace these placeholders in templates:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{DOMAIN}}` | Primary domain | `example.com` |
| `{{APP_NAME}}` | Application name | `myapp` |
| `{{WEB_SERVER_1}}` | Web server IP/hostname | `10.0.0.1` |
| `{{WEB_PORT}}` | Web server port | `8080` |
| `{{API_SERVER_1}}` | API server IP/hostname | `10.0.1.1` |
| `{{API_PORT}}` | API server port | `8000` |
| `{{ACM_CERT_ARN}}` | AWS Certificate ARN | `arn:aws:acm:...` |
| `{{WEB_IMAGE}}` | Docker image for web | `myapp-web:latest` |
| `{{API_IMAGE}}` | Docker image for API | `myapp-api:latest` |
