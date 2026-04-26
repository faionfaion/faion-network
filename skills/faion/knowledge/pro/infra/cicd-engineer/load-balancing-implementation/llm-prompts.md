# LLM Prompts for Load Balancing

## Analysis Prompts

### Analyze Current Setup

```
Analyze this load balancer configuration and identify:
1. Security issues (TLS version, ciphers, headers)
2. Performance bottlenecks (connection limits, timeouts)
3. High availability gaps (single points of failure)
4. Monitoring gaps (missing metrics, alerts)
5. Best practice violations

Configuration:
[PASTE CONFIG HERE]

Provide specific recommendations with code examples.
```

### Compare Solutions

```
Compare HAProxy vs Nginx for this use case:
- Traffic type: [HTTP/TCP/gRPC/WebSocket]
- Expected RPS: [NUMBER]
- Concurrent connections: [NUMBER]
- Session persistence required: [YES/NO]
- Environment: [Cloud/Bare-metal/Kubernetes]

Recommend the best solution with justification and provide a starter configuration.
```

### Troubleshoot Issues

```
I'm experiencing [ISSUE] with my load balancer.

Environment:
- LB type: [HAProxy/Nginx/ALB/Ingress]
- Backend count: [NUMBER]
- Traffic pattern: [DESCRIPTION]

Symptoms:
[DESCRIBE SYMPTOMS]

Current configuration:
[PASTE RELEVANT CONFIG]

Logs/Errors:
[PASTE LOGS]

Diagnose the issue and provide fix.
```

---

## Generation Prompts

### Generate HAProxy Config

```
Generate a production-ready HAProxy configuration for:

Requirements:
- Frontend: HTTPS on port 443 with HTTP redirect
- SSL certificate path: /etc/haproxy/certs/example.com.pem
- Backends: [LIST SERVERS WITH IPs AND PORTS]
- Load balancing algorithm: [roundrobin/leastconn/source]
- Health check endpoint: /health
- Rate limiting: [NUMBER] requests per 10 seconds per IP
- Session persistence: [YES/NO, if yes specify method]

Include:
- Security headers (HSTS, X-Frame-Options, etc.)
- Connection timeouts
- Logging configuration
- Stats page on port 8404
- Comments explaining each section
```

### Generate Nginx Config

```
Generate a production Nginx load balancer configuration:

Requirements:
- Domain: [DOMAIN]
- SSL: Let's Encrypt certificate at /etc/letsencrypt/live/[DOMAIN]/
- Upstreams:
  - web: [LIST SERVERS] - least_conn balancing
  - api: [LIST SERVERS] - ip_hash for sticky sessions
- Rate limiting: 10 req/s for /api endpoints
- WebSocket support on /ws path
- Gzip compression enabled

Include:
- Worker process tuning
- Security headers
- Upstream health checks (passive)
- Proxy buffering settings
- Error handling with proxy_next_upstream
```

### Generate Kubernetes Ingress

```
Generate Kubernetes Ingress resources for:

Environment:
- Ingress controller: [nginx/haproxy/traefik]
- Cluster: [EKS/GKE/AKS/bare-metal]
- TLS: cert-manager with Let's Encrypt

Services:
- frontend: web-frontend:80 at example.com/
- api: api-service:80 at api.example.com/
- docs: docs-service:80 at docs.example.com/

Requirements:
- Force HTTPS redirect
- Rate limiting: 100 req/s
- CORS enabled for frontend
- Body size limit: 50MB for API
- Custom timeouts for API (2 minutes)

Include annotations and TLS configuration.
```

### Generate Terraform IaC

```
Generate Terraform configuration for AWS Application Load Balancer:

Requirements:
- Environment: [production/staging]
- VPC ID: [VPC_ID]
- Subnets: [SUBNET_IDS]
- Certificate ARN: [CERT_ARN]

Target groups:
- web: port 8080, health check /health
- api: port 3000, health check /health/ready

Features:
- Access logs to S3
- Deletion protection
- HTTP to HTTPS redirect
- WAF integration (optional)

Include security groups and outputs.
```

---

## Optimization Prompts

### Optimize for Performance

```
Optimize this load balancer configuration for maximum performance:

Current config:
[PASTE CONFIG]

Traffic profile:
- Peak RPS: [NUMBER]
- Average request size: [SIZE]
- Average response size: [SIZE]
- Concurrent connections: [NUMBER]

Constraints:
- Available CPU cores: [NUMBER]
- Available RAM: [SIZE]
- Network bandwidth: [SPEED]

Focus on:
1. Connection handling optimization
2. Buffer sizing
3. Keepalive tuning
4. SSL/TLS optimization
5. Compression settings
```

### Optimize for Security

```
Review and harden this load balancer configuration:

Current config:
[PASTE CONFIG]

Security requirements:
- Compliance: [PCI-DSS/HIPAA/SOC2/none]
- DDoS protection level: [basic/advanced]
- WAF: [required/optional]

Audit for:
1. TLS configuration (protocols, ciphers)
2. Security headers
3. Rate limiting adequacy
4. Access controls
5. Logging for audit trail
6. Sensitive data exposure

Provide hardened configuration with explanations.
```

### Optimize for High Availability

```
Design a highly available load balancing architecture:

Current setup:
[DESCRIBE CURRENT SETUP]

Requirements:
- Target uptime: [99.9%/99.95%/99.99%]
- RTO: [TIME]
- RPO: [TIME]
- Geographic distribution: [single region/multi-region/global]

Consider:
1. LB redundancy (active-passive/active-active)
2. Health check strategy
3. Failover mechanisms
4. Cross-zone/cross-region balancing
5. DNS-based failover
6. Session persistence during failover

Provide architecture diagram (text) and configurations.
```

---

## Migration Prompts

### Migrate to Cloud LB

```
Plan migration from [HAProxy/Nginx] to [AWS ALB/GCP LB/Azure LB]:

Current configuration:
[PASTE CONFIG]

Current features used:
- [LIST FEATURES]

Requirements:
- Zero downtime migration
- Feature parity where possible
- Cost optimization

Provide:
1. Feature mapping (current -> cloud equivalent)
2. Migration steps
3. Terraform configuration for new setup
4. Rollback plan
5. Validation checklist
```

### Migrate to Kubernetes Ingress

```
Migrate this standalone load balancer to Kubernetes Ingress:

Current setup:
- LB type: [HAProxy/Nginx]
- Configuration: [PASTE CONFIG]

Target Kubernetes environment:
- Cluster type: [EKS/GKE/AKS/self-managed]
- Ingress controller: [nginx/haproxy/traefik/istio]

Provide:
1. Ingress controller deployment
2. Ingress resources for each route
3. ConfigMap for controller tuning
4. Migration strategy (blue-green/canary)
5. Testing plan
```

---

## Monitoring Prompts

### Generate Monitoring Stack

```
Generate monitoring configuration for load balancer:

LB type: [HAProxy/Nginx/ALB]
Stack: [Prometheus + Grafana / Datadog / CloudWatch]

Requirements:
- Key metrics to collect
- Alert thresholds
- Dashboard panels
- Log aggregation

Include:
1. Exporter configuration (if applicable)
2. Prometheus scrape config
3. Alert rules (YAML)
4. Grafana dashboard JSON
5. Log parsing patterns
```

### Define SLIs/SLOs

```
Define SLIs and SLOs for this load balancer setup:

Service type: [Web app/API/Real-time]
Current traffic: [RPS]
Business requirements: [DESCRIBE]

Define:
1. Availability SLI/SLO (e.g., 99.9%)
2. Latency SLI/SLO (e.g., p99 < 200ms)
3. Error rate SLI/SLO (e.g., < 0.1%)
4. Throughput SLI/SLO

Provide:
- Prometheus queries for each SLI
- Error budget calculations
- Alert rules for SLO breaches
- Runbook templates for common issues
```

---

## Quick Reference Prompts

### Explain Concept

```
Explain [CONCEPT] in the context of load balancing:
- What it is
- When to use it
- Configuration example
- Common pitfalls

Concepts: [sticky sessions / health checks / connection draining /
           cross-zone balancing / SSL termination / rate limiting /
           circuit breaking / blue-green deployment / canary release]
```

### Debug Command

```
What commands should I run to debug [ISSUE] on [HAProxy/Nginx]?

Issue types:
- Backend not receiving traffic
- High latency
- Connection refused errors
- SSL handshake failures
- Health check failures
- Rate limiting triggering unexpectedly

Provide commands with expected output interpretation.
```

---

*LLM Prompts for Load Balancing | faion-cicd-engineer*
