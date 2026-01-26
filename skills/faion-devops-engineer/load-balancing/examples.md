# Load Balancing Examples

## HAProxy Examples

### Basic HTTP Load Balancer

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

    # Modern SSL settings
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
    tune.ssl.default-dh-param 2048

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option  forwardfor
    option  http-server-close
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

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

    # Path-based routing
    acl is_api path_beg /api
    acl is_static path_beg /static

    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend web_servers

# Web backend with round robin
backend web_servers
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200

    server web1 10.0.0.1:8080 check weight 5
    server web2 10.0.0.2:8080 check weight 5
    server web3 10.0.0.3:8080 check weight 3 backup

# API backend with least connections and sticky sessions
backend api_servers
    balance leastconn
    option httpchk GET /api/health
    http-check expect status 200

    cookie SERVERID insert indirect nocache

    server api1 10.0.1.1:8000 check cookie api1
    server api2 10.0.1.2:8000 check cookie api2
    server api3 10.0.1.3:8000 check cookie api3

# Static content backend
backend static_servers
    balance roundrobin
    option httpchk GET /health

    server static1 10.0.2.1:80 check
    server static2 10.0.2.2:80 check
```

### HAProxy TCP Load Balancer (L4)

```haproxy
# L4 load balancing for database or other TCP services

global
    log /dev/log local0
    maxconn 50000

defaults
    mode tcp
    log global
    option tcplog
    timeout connect 10s
    timeout client 30s
    timeout server 30s

frontend mysql_front
    bind *:3306
    default_backend mysql_servers

backend mysql_servers
    balance leastconn
    option mysql-check user haproxy

    server mysql1 10.0.3.1:3306 check
    server mysql2 10.0.3.2:3306 check
    server mysql3 10.0.3.3:3306 check backup
```

### HAProxy with Rate Limiting

```haproxy
frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/example.com.pem

    # Rate limiting: 100 requests per 10 seconds per IP
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }

    # Slowdown instead of blocking
    # http-request tarpit if { sc_http_req_rate(0) gt 50 }

    default_backend web_servers
```

## Nginx Examples

### Basic HTTP Load Balancer

```nginx
# /etc/nginx/nginx.conf

upstream web_backend {
    # Load balancing method
    least_conn;

    # Servers with weights and health checks
    server 10.0.0.1:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:8080 weight=2 backup;

    # Keepalive connections to backend
    keepalive 32;
}

upstream api_backend {
    # IP hash for sticky sessions
    ip_hash;

    server 10.0.1.1:8000;
    server 10.0.1.2:8000;
    server 10.0.1.3:8000;
}

upstream static_backend {
    server 10.0.2.1:80;
    server 10.0.2.2:80;
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;

    # Modern TLS settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;

    location / {
        proxy_pass http://web_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Retry on failure
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

    location /static {
        proxy_pass http://static_backend;
        proxy_cache_valid 200 1d;
        expires 1d;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### Nginx TCP/UDP Load Balancer (Stream)

```nginx
# /etc/nginx/nginx.conf

stream {
    upstream mysql_backend {
        least_conn;
        server 10.0.3.1:3306 weight=5;
        server 10.0.3.2:3306 weight=5;
        server 10.0.3.3:3306 backup;
    }

    upstream redis_backend {
        hash $remote_addr consistent;
        server 10.0.4.1:6379;
        server 10.0.4.2:6379;
    }

    server {
        listen 3306;
        proxy_pass mysql_backend;
        proxy_timeout 10s;
        proxy_connect_timeout 5s;
    }

    server {
        listen 6379;
        proxy_pass redis_backend;
        proxy_timeout 10s;
    }
}
```

## AWS Examples

### ALB with CloudFormation

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Application Load Balancer

Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
  PublicSubnet1:
    Type: AWS::EC2::Subnet::Id
  PublicSubnet2:
    Type: AWS::EC2::Subnet::Id
  CertificateArn:
    Type: String

Resources:
  # Security Group for ALB
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: ALB Security Group
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0

  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: my-alb
      Scheme: internet-facing
      Type: application
      IpAddressType: ipv4
      SecurityGroups:
        - !Ref ALBSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      LoadBalancerAttributes:
        - Key: idle_timeout.timeout_seconds
          Value: '60'
        - Key: routing.http2.enabled
          Value: 'true'
        - Key: access_logs.s3.enabled
          Value: 'true'
        - Key: access_logs.s3.bucket
          Value: my-alb-logs

  # HTTPS Listener
  HTTPSListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 443
      Protocol: HTTPS
      SslPolicy: ELBSecurityPolicy-TLS13-1-2-2021-06
      Certificates:
        - CertificateArn: !Ref CertificateArn
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref WebTargetGroup

  # HTTP to HTTPS Redirect
  HTTPListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP
      DefaultActions:
        - Type: redirect
          RedirectConfig:
            Protocol: HTTPS
            Port: '443'
            StatusCode: HTTP_301

  # Web Target Group
  WebTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: web-targets
      Port: 8080
      Protocol: HTTP
      VpcId: !Ref VpcId
      TargetType: instance
      HealthCheckEnabled: true
      HealthCheckIntervalSeconds: 30
      HealthCheckPath: /health
      HealthCheckProtocol: HTTP
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      Matcher:
        HttpCode: '200'
      TargetGroupAttributes:
        - Key: deregistration_delay.timeout_seconds
          Value: '30'
        - Key: stickiness.enabled
          Value: 'true'
        - Key: stickiness.type
          Value: lb_cookie
        - Key: stickiness.lb_cookie.duration_seconds
          Value: '86400'

  # API Target Group
  APITargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: api-targets
      Port: 8000
      Protocol: HTTP
      VpcId: !Ref VpcId
      TargetType: instance
      HealthCheckPath: /api/health

  # Listener Rule for API
  APIListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HTTPSListener
      Priority: 10
      Conditions:
        - Field: path-pattern
          Values:
            - /api/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref APITargetGroup

Outputs:
  LoadBalancerDNS:
    Value: !GetAtt ApplicationLoadBalancer.DNSName
  LoadBalancerArn:
    Value: !Ref ApplicationLoadBalancer
```

### NLB with Terraform

```hcl
# Network Load Balancer for TCP traffic

resource "aws_lb" "nlb" {
  name               = "my-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = var.public_subnet_ids

  enable_cross_zone_load_balancing = true

  tags = {
    Environment = "production"
  }
}

resource "aws_lb_target_group" "tcp" {
  name     = "tcp-targets"
  port     = 8080
  protocol = "TCP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    protocol            = "TCP"
    interval            = 30
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }

  deregistration_delay = 30
}

resource "aws_lb_listener" "tcp" {
  load_balancer_arn = aws_lb.nlb.arn
  port              = 443
  protocol          = "TLS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tcp.arn
  }
}
```

## Kubernetes Examples

### Service Types

```yaml
# ClusterIP - Internal only
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
# NodePort - External via node ports
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
# LoadBalancer - Cloud provider LB
apiVersion: v1
kind: Service
metadata:
  name: web-loadbalancer
  annotations:
    # AWS NLB
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    # GCP
    # cloud.google.com/load-balancer-type: "Internal"
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 443
      targetPort: 8080
```

### Nginx Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "5"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - example.com
        - api.example.com
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
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

### Traefik IngressRoute

```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: web-ingressroute
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`example.com`) && PathPrefix(`/api`)
      kind: Rule
      services:
        - name: api-service
          port: 80
      middlewares:
        - name: rate-limit
    - match: Host(`example.com`)
      kind: Rule
      services:
        - name: web-service
          port: 80
  tls:
    secretName: example-tls

---
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: rate-limit
spec:
  rateLimit:
    average: 100
    burst: 50
```

## Health Check Endpoint Examples

### Go Health Check

```go
package main

import (
    "encoding/json"
    "net/http"
    "time"
)

type HealthResponse struct {
    Status    string            `json:"status"`
    Version   string            `json:"version"`
    Timestamp string            `json:"timestamp"`
    Checks    map[string]string `json:"checks"`
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    checks := make(map[string]string)

    // Check database
    if err := checkDatabase(); err != nil {
        checks["database"] = "unhealthy: " + err.Error()
    } else {
        checks["database"] = "healthy"
    }

    // Check Redis
    if err := checkRedis(); err != nil {
        checks["redis"] = "unhealthy: " + err.Error()
    } else {
        checks["redis"] = "healthy"
    }

    // Determine overall status
    status := "healthy"
    statusCode := http.StatusOK
    for _, v := range checks {
        if v != "healthy" {
            status = "unhealthy"
            statusCode = http.StatusServiceUnavailable
            break
        }
    }

    response := HealthResponse{
        Status:    status,
        Version:   "1.0.0",
        Timestamp: time.Now().UTC().Format(time.RFC3339),
        Checks:    checks,
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(statusCode)
    json.NewEncoder(w).Encode(response)
}
```

### Python/FastAPI Health Check

```python
from fastapi import FastAPI, Response
from datetime import datetime
import asyncio

app = FastAPI()

async def check_database():
    # Database connectivity check
    try:
        await db.execute("SELECT 1")
        return True, None
    except Exception as e:
        return False, str(e)

async def check_redis():
    # Redis connectivity check
    try:
        await redis.ping()
        return True, None
    except Exception as e:
        return False, str(e)

@app.get("/health")
async def health_check(response: Response):
    checks = {}

    # Run checks in parallel
    db_ok, db_err = await check_database()
    redis_ok, redis_err = await check_redis()

    checks["database"] = "healthy" if db_ok else f"unhealthy: {db_err}"
    checks["redis"] = "healthy" if redis_ok else f"unhealthy: {redis_err}"

    all_healthy = db_ok and redis_ok

    if not all_healthy:
        response.status_code = 503

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }

# Separate liveness and readiness
@app.get("/healthz")
async def liveness():
    """Liveness probe - is the process running?"""
    return {"status": "alive"}

@app.get("/readyz")
async def readiness(response: Response):
    """Readiness probe - can we serve traffic?"""
    db_ok, _ = await check_database()
    if not db_ok:
        response.status_code = 503
        return {"status": "not ready"}
    return {"status": "ready"}
```

### Node.js/Express Health Check

```javascript
const express = require('express');
const app = express();

async function checkDatabase() {
  try {
    await db.query('SELECT 1');
    return { healthy: true };
  } catch (error) {
    return { healthy: false, error: error.message };
  }
}

async function checkRedis() {
  try {
    await redis.ping();
    return { healthy: true };
  } catch (error) {
    return { healthy: false, error: error.message };
  }
}

app.get('/health', async (req, res) => {
  const [dbCheck, redisCheck] = await Promise.all([
    checkDatabase(),
    checkRedis()
  ]);

  const checks = {
    database: dbCheck.healthy ? 'healthy' : `unhealthy: ${dbCheck.error}`,
    redis: redisCheck.healthy ? 'healthy' : `unhealthy: ${redisCheck.error}`
  };

  const allHealthy = dbCheck.healthy && redisCheck.healthy;

  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? 'healthy' : 'unhealthy',
    version: process.env.APP_VERSION || '1.0.0',
    timestamp: new Date().toISOString(),
    checks
  });
});
```
