# LLM Prompts for Load Balancing

Prompts for AI assistants to help with load balancing tasks.

## Architecture Design Prompts

### Prompt: Load Balancer Architecture Review

```
Review my load balancing architecture and provide recommendations.

Context:
- Application type: [web app / API / microservices / database]
- Expected traffic: [requests/second]
- Session requirements: [stateless / sticky sessions needed]
- Geographic distribution: [single region / multi-region / global]
- Current infrastructure: [on-premise / AWS / GCP / Azure / Kubernetes]
- High availability requirements: [99.9% / 99.99% / 99.999%]

Current setup:
[Describe current load balancing setup or "none"]

Please provide:
1. Recommended load balancer type (L4 vs L7)
2. Optimal algorithm for this use case
3. Health check strategy
4. SSL/TLS termination approach
5. High availability design
6. Potential issues and mitigations
```

### Prompt: Algorithm Selection

```
Help me choose the right load balancing algorithm.

Application characteristics:
- Request duration: [short <100ms / medium 100ms-1s / long >1s]
- Server capacity: [equal / varying]
- Session persistence: [needed / not needed]
- Connection type: [HTTP / WebSocket / gRPC / TCP]
- Backend count: [number of servers]
- Traffic pattern: [steady / spiky / unpredictable]

Current issues (if any):
[Describe any current load distribution problems]

Please recommend:
1. Primary algorithm with rationale
2. Alternative algorithms to consider
3. Configuration parameters
4. Monitoring metrics to track
```

## Configuration Prompts

### Prompt: HAProxy Configuration

```
Generate HAProxy configuration for my application.

Requirements:
- Frontends: [list domains and ports]
- Backends:
  - [backend name]: [servers with IPs/ports]
  - [backend name]: [servers with IPs/ports]
- SSL: [terminate at LB / passthrough / re-encrypt]
- Certificate path: [path to cert files]
- Load balancing algorithm: [roundrobin / leastconn / etc]
- Session persistence: [none / cookie / ip_hash]
- Health checks: [path and expected response]
- Rate limiting: [requests per second, if any]
- Special requirements: [any additional needs]

Please provide:
1. Complete haproxy.cfg file
2. Required system settings (sysctl, ulimits)
3. SSL certificate preparation commands
4. Testing commands
```

### Prompt: Nginx Load Balancer Configuration

```
Generate Nginx load balancer configuration.

Setup requirements:
- Domain: [domain name]
- Upstreams:
  - web: [servers with ports]
  - api: [servers with ports]
- SSL certificate: [path or "use Let's Encrypt"]
- Load balancing method: [least_conn / ip_hash / etc]
- Keepalive connections: [yes/no, how many]
- Rate limiting: [limits per zone]
- Caching: [static assets / none]
- Retry behavior: [on which errors]

Please provide:
1. Complete nginx.conf
2. SSL configuration with modern settings
3. Rate limiting configuration
4. Health check setup
5. Logging configuration
```

### Prompt: Kubernetes Ingress Setup

```
Create Kubernetes Ingress configuration.

Environment:
- Kubernetes version: [version]
- Ingress controller: [nginx / traefik / AWS ALB / GCP]
- Cloud provider: [AWS / GCP / Azure / on-prem]

Requirements:
- Domains: [list of domains]
- Services:
  - [path]: [service:port]
  - [path]: [service:port]
- TLS: [cert-manager / manual / cloud certificate]
- Annotations needed: [list any specific annotations]
- Rate limiting: [if needed]
- Authentication: [if needed]

Please provide:
1. Ingress resource YAML
2. Required Service definitions
3. TLS Secret or cert-manager configuration
4. Any required ConfigMaps
5. Testing commands
```

## Cloud-Specific Prompts

### Prompt: AWS ALB Setup

```
Create AWS Application Load Balancer configuration.

Requirements:
- VPC ID: [vpc-xxx]
- Subnets: [public subnet IDs for ALB]
- Security requirements: [allowed IPs/CIDRs]
- Target type: [instance / ip / lambda]
- Target groups:
  - [name]: port [port], health check [path]
- Listener rules:
  - [condition]: forward to [target group]
- SSL certificate: [ACM ARN or "create new"]
- Access logs: [S3 bucket or "not needed"]
- WAF: [attach existing / create new / none]

Please provide:
1. Terraform/CloudFormation template
2. Security group configuration
3. Target group settings
4. Listener rules
5. IAM roles if needed
```

### Prompt: GCP Load Balancer Setup

```
Create GCP HTTP(S) Load Balancer configuration.

Requirements:
- Project ID: [project]
- Region: [region or "global"]
- Backend type: [instance group / NEG / Cloud Run]
- URL map rules:
  - [host/path]: [backend service]
- SSL: [managed certificate / custom]
- CDN: [enable / disable]
- Cloud Armor: [policy name or "none"]

Please provide:
1. Terraform configuration
2. Backend service settings
3. URL map configuration
4. SSL certificate setup
5. Health check configuration
```

## Troubleshooting Prompts

### Prompt: Load Balancer Debugging

```
Help me troubleshoot load balancer issues.

Problem description:
[Describe the issue - 502 errors, uneven distribution, etc.]

Environment:
- Load balancer type: [HAProxy / Nginx / ALB / etc]
- Backend count: [number]
- Traffic volume: [requests/second]

Symptoms:
- Error messages: [specific errors if any]
- When it occurs: [always / under load / specific times]
- Affected percentage: [of requests]

Current configuration:
[Paste relevant config sections]

Logs/metrics:
[Paste relevant log entries or metric data]

Please help:
1. Identify likely root causes
2. Suggest diagnostic commands
3. Recommend fixes
4. Suggest monitoring improvements
```

### Prompt: Health Check Issues

```
Troubleshoot health check failures.

Load balancer: [type]
Health check configuration:
- Path: [path]
- Port: [port]
- Interval: [seconds]
- Timeout: [seconds]
- Healthy threshold: [count]
- Unhealthy threshold: [count]

Symptoms:
- Backends marked unhealthy: [which ones]
- Health check response: [if known]
- Application logs show: [relevant entries]

Backend application:
- Technology: [language/framework]
- Health endpoint implementation: [describe or paste code]

Please help:
1. Diagnose the health check failure
2. Verify health endpoint implementation
3. Suggest configuration adjustments
4. Recommend monitoring setup
```

### Prompt: Performance Optimization

```
Optimize load balancer performance.

Current setup:
- Load balancer: [type and version]
- Configuration: [paste config]
- Traffic: [requests/second]
- Average response time: [ms]
- P99 latency: [ms]

Performance issues:
- [Describe specific performance problems]

Infrastructure:
- CPU/memory usage on LB: [percentage]
- Backend server count: [number]
- Backend server specs: [CPU/memory]

Please provide:
1. Configuration optimizations
2. System tuning recommendations
3. Algorithm adjustments
4. Caching opportunities
5. Scaling recommendations
```

## Migration Prompts

### Prompt: Load Balancer Migration

```
Plan migration from [old LB] to [new LB].

Current setup:
- Load balancer: [current type]
- Configuration: [paste or describe]
- Traffic volume: [requests/second]
- Downtime tolerance: [zero / maintenance window]

Target setup:
- New load balancer: [target type]
- Additional requirements: [new features needed]

Concerns:
- [List specific migration concerns]

Please provide:
1. Migration strategy (blue-green, gradual, etc.)
2. Configuration translation
3. Testing plan
4. Rollback procedure
5. Monitoring during migration
6. Timeline with milestones
```

### Prompt: Cloud Migration

```
Migrate load balancing to cloud.

Current on-premise setup:
- Load balancer: [type]
- Configuration: [describe]
- SSL certificates: [how managed]
- Health checks: [configuration]

Target cloud: [AWS / GCP / Azure]

Requirements:
- Preserve: [what must stay the same]
- Improve: [what should be better]
- Budget: [cost considerations]

Please provide:
1. Recommended cloud load balancer service
2. Architecture comparison
3. Configuration mapping
4. Certificate migration
5. DNS cutover strategy
6. Cost estimate
```

## Security Prompts

### Prompt: Load Balancer Security Audit

```
Audit my load balancer security configuration.

Load balancer: [type]
Configuration:
[Paste full configuration]

Environment:
- Internet-facing: [yes/no]
- Protected resources: [describe]
- Compliance requirements: [PCI-DSS / HIPAA / SOC2 / none]

Please audit:
1. TLS/SSL configuration (versions, ciphers)
2. Security headers
3. Access control
4. Rate limiting
5. DDoS protection
6. Logging and monitoring
7. Certificate management
8. Provide severity ratings and remediation steps
```

### Prompt: SSL/TLS Hardening

```
Harden SSL/TLS configuration.

Current configuration:
[Paste SSL/TLS settings]

Requirements:
- Minimum TLS version: [1.2 / 1.3]
- Compliance: [requirements]
- Browser support: [modern only / legacy support needed]
- Performance priority: [security / speed balance]

Please provide:
1. Recommended TLS configuration
2. Cipher suite order
3. HSTS configuration
4. Certificate pinning (if appropriate)
5. OCSP stapling setup
6. Testing commands and expected results
```

## Usage Tips

1. **Be specific** - Include exact versions, traffic numbers, and requirements
2. **Provide context** - Explain your constraints and priorities
3. **Share configs** - Paste actual configuration for accurate help
4. **Include errors** - Exact error messages help diagnosis
5. **State goals** - What outcome are you trying to achieve?

## Response Quality Checklist

After receiving a response, verify:

- [ ] Configuration is syntactically correct
- [ ] Security best practices followed
- [ ] Health checks properly configured
- [ ] SSL/TLS settings are modern
- [ ] Logging is enabled
- [ ] Failover behavior defined
- [ ] Testing steps provided
- [ ] Rollback plan included (for changes)
