# LLM Prompts for Container Orchestration

Effective prompts for LLM-assisted Kubernetes design and troubleshooting.

## Architecture Design Prompts

### New Application Deployment

```
Design a Kubernetes deployment architecture for:

Application: [e.g., E-commerce API]
Traffic: [e.g., 1000 RPS average, 5000 RPS peak]
Requirements:
- [e.g., High availability across zones]
- [e.g., Zero-downtime deployments]
- [e.g., Scale to handle 10x traffic spikes]

Include:
1. Deployment configuration with resource limits
2. Service and Ingress setup
3. HPA configuration
4. Health check strategy
5. Security considerations

Use production-ready settings, not development defaults.
```

### Migration from Docker Compose

```
Convert this Docker Compose to production Kubernetes manifests:

```yaml
[paste docker-compose.yaml]
```

Requirements:
- Environment: [production/staging]
- Cloud provider: [AWS/GCP/Azure]
- Add production-ready features:
  - Resource requests/limits
  - Health checks
  - Security contexts
  - Proper secrets management
  - HPA for scalable services

Provide:
1. Deployment for each service
2. Services and networking
3. ConfigMaps and Secrets structure
4. StorageClass and PVC for stateful services
5. Ingress configuration
```

### Microservices Architecture

```
Design Kubernetes architecture for a microservices system:

Services:
- [Service 1]: [Description, traffic, requirements]
- [Service 2]: [Description, traffic, requirements]
- [Service 3]: [Description, traffic, requirements]

Communication patterns:
- [e.g., Sync REST between frontend and API]
- [e.g., Async events via Kafka between services]

Requirements:
- [e.g., Service mesh for mTLS]
- [e.g., Canary deployments]
- [e.g., Cross-namespace communication]

Provide:
1. Namespace strategy
2. Deployment configurations for each service
3. Service discovery approach
4. Network policies for isolation
5. Observability setup
```

---

## Resource Optimization Prompts

### Right-sizing Resources

```
Analyze and optimize resource configuration for this deployment:

Current config:
```yaml
[paste deployment yaml]
```

Metrics (last 7 days):
- CPU usage: [avg/max/p95]
- Memory usage: [avg/max/p95]
- Replicas: [min/max during period]

Goals:
- Reduce cost while maintaining performance
- Handle traffic spikes without OOM kills
- Efficient cluster bin-packing

Provide:
1. Recommended requests and limits
2. QoS class analysis
3. HPA configuration
4. Cost impact estimate
5. Risk assessment
```

### Cluster Capacity Planning

```
Plan Kubernetes cluster capacity for:

Workloads:
- [X] deployments with [Y] replicas each
- Total resource needs: [CPU, Memory]
- Growth expectation: [e.g., 50% in 6 months]

Requirements:
- High availability (multi-zone)
- [X]% headroom for traffic spikes
- Cost optimization priority: [high/medium/low]

Provide:
1. Node pool configuration
2. Instance types recommendation
3. Cluster autoscaler settings
4. ResourceQuotas per namespace
5. Cost estimate
```

---

## Security Review Prompts

### Security Audit

```
Perform a security audit of this Kubernetes configuration:

```yaml
[paste manifests]
```

Check for:
1. Pod security issues
   - Running as root
   - Privileged containers
   - Capability escalation
   - Host path mounts

2. RBAC issues
   - Overly permissive roles
   - Cluster-admin usage
   - Service account misuse

3. Network security
   - Missing network policies
   - Unrestricted egress
   - Exposed services

4. Secrets management
   - Plain text secrets
   - Secrets in environment variables vs volumes
   - Missing encryption

5. Image security
   - Latest tags
   - Unsigned images
   - Known vulnerabilities

Provide findings with severity (Critical/High/Medium/Low) and fixes.
```

### RBAC Design

```
Design RBAC configuration for:

Team structure:
- Platform team: Full cluster access
- Dev team A: Namespace [X] - deploy and debug
- Dev team B: Namespace [Y] - deploy and debug
- CI/CD pipeline: Deploy to all namespaces
- Monitoring: Read-only cluster-wide

Requirements:
- Principle of least privilege
- Separate roles for different operations
- Audit capability

Provide:
1. ClusterRoles and Roles
2. RoleBindings and ClusterRoleBindings
3. ServiceAccounts for automation
4. Namespace labels for RBAC
5. Audit policy recommendations
```

### Network Policy Design

```
Design network policies for:

Namespace structure:
- frontend: Web applications
- backend: API services
- database: Databases and caches
- monitoring: Prometheus, Grafana

Communication requirements:
- frontend -> backend: HTTP on port 8080
- backend -> database: PostgreSQL 5432, Redis 6379
- monitoring -> all: Metrics on port 9090
- backend -> external: HTTPS to third-party APIs

Security requirements:
- Default deny all
- Explicit allow rules only
- Egress control

Provide:
1. Default deny policies per namespace
2. Allow policies for each communication path
3. DNS access policy
4. External egress policy
5. Testing commands to verify policies
```

---

## Troubleshooting Prompts

### Pod Issues

```
Troubleshoot pod issue:

Symptoms:
- [e.g., Pods stuck in CrashLoopBackOff]
- [e.g., Containers OOMKilled]
- [e.g., Pods pending for 5 minutes]

kubectl describe output:
```
[paste relevant output]
```

kubectl logs output:
```
[paste relevant logs]
```

Events:
```
[paste kubectl get events output]
```

Provide:
1. Root cause analysis
2. Immediate fix
3. Long-term prevention
4. Monitoring to detect similar issues
```

### Networking Issues

```
Troubleshoot networking issue:

Symptoms:
- [e.g., Service unreachable from other pods]
- [e.g., Ingress returning 502]
- [e.g., DNS resolution failing]

Configuration:
```yaml
[paste service/ingress/networkpolicy yaml]
```

Debug output:
```
[paste curl/dig/netcat output]
```

Provide:
1. Diagnostic steps to isolate the issue
2. Root cause
3. Fix configuration
4. Verification steps
```

### Performance Issues

```
Troubleshoot performance degradation:

Application: [description]

Symptoms:
- [e.g., Latency increased from 50ms to 500ms]
- [e.g., Timeouts during peak hours]
- [e.g., HPA not scaling fast enough]

Current configuration:
```yaml
[paste deployment and HPA yaml]
```

Metrics:
- CPU utilization: [values]
- Memory utilization: [values]
- Request latency: [p50, p95, p99]
- Request rate: [values]

Provide:
1. Performance analysis
2. Bottleneck identification
3. Configuration fixes
4. Scaling recommendations
5. Monitoring improvements
```

---

## Deployment Strategy Prompts

### Canary Deployment Setup

```
Design canary deployment for:

Application: [name]
Current traffic: [RPS]
Risk tolerance: [low/medium/high]

Requirements:
- [e.g., Automatic rollback on error rate > 1%]
- [e.g., Progressive traffic increase: 5% -> 25% -> 50% -> 100%]
- [e.g., Minimum 10 minutes between steps]

Tools available:
- [Argo Rollouts / Flagger / Istio / nginx]

Provide:
1. Rollout configuration
2. Analysis template for metrics
3. Traffic routing setup
4. Rollback conditions
5. Monitoring dashboards
```

### Blue-Green Deployment

```
Design blue-green deployment for:

Application: [name]
Downtime tolerance: [zero/minimal]
Database: [yes/no - migration considerations]

Requirements:
- [e.g., Manual promotion after testing]
- [e.g., Quick rollback capability]
- [e.g., Preview URL for testing]

Provide:
1. Deployment configuration (blue and green)
2. Service configuration for traffic switch
3. Promotion workflow
4. Rollback procedure
5. Database migration strategy (if applicable)
```

---

## Storage Prompts

### Persistent Storage Design

```
Design persistent storage for:

Application: [e.g., PostgreSQL database]
Data volume: [e.g., 500GB initial, 2TB expected]
IOPS requirement: [e.g., 10000 IOPS]
Access pattern: [e.g., Random read-heavy]

Requirements:
- [e.g., Encryption at rest]
- [e.g., Daily snapshots]
- [e.g., Cross-zone replication]

Cloud provider: [AWS/GCP/Azure]

Provide:
1. StorageClass configuration
2. PVC template
3. VolumeSnapshot setup
4. Backup strategy with Velero
5. Disaster recovery procedure
```

---

## Observability Prompts

### Monitoring Setup

```
Design monitoring for Kubernetes cluster:

Components to monitor:
- [X] applications across [Y] namespaces
- Cluster health and resources
- Ingress and networking

Requirements:
- Prometheus + Grafana stack
- AlertManager for notifications
- [e.g., Slack integration for alerts]

Key metrics:
- Application: [latency, error rate, throughput]
- Infrastructure: [CPU, memory, disk, network]
- Kubernetes: [pod health, deployment status, HPA activity]

Provide:
1. ServiceMonitor configurations
2. PrometheusRule for alerts
3. Grafana dashboard recommendations
4. Alert severity and routing
5. On-call runbook template
```

---

## Review Prompts

### Production Readiness Review

```
Review this configuration for production readiness:

```yaml
[paste all manifests]
```

Check against:
1. Resource management
   - Requests and limits set appropriately
   - QoS class considerations
   - HPA or KEDA for scaling

2. Reliability
   - Health probes configured correctly
   - PodDisruptionBudget
   - Anti-affinity for HA
   - TopologySpreadConstraints

3. Security
   - Security contexts
   - RBAC minimum privileges
   - Network policies
   - Secret management

4. Observability
   - Metrics exposure
   - Structured logging
   - Tracing headers

5. Operations
   - Deployment strategy
   - Rollback capability
   - Resource versioning

Rate each area: Ready / Needs Work / Critical Issues
Provide specific fixes for issues found.
```

### Cost Optimization Review

```
Review Kubernetes configuration for cost optimization:

Current setup:
- Node pools: [describe]
- Total deployments: [count]
- Current monthly cost: [estimate]

```yaml
[paste key manifests or describe workloads]
```

Analyze:
1. Right-sizing opportunities
   - Over-provisioned resources
   - Underutilized nodes
   - Idle pods

2. Scaling efficiency
   - HPA tuning
   - Scale-to-zero opportunities (KEDA)
   - Cluster autoscaler settings

3. Storage optimization
   - Unused PVCs
   - Over-provisioned volumes
   - Storage class selection

4. Spot/Preemptible usage
   - Workloads suitable for spot
   - Required on-demand workloads

Provide:
1. Prioritized optimization list
2. Estimated savings per optimization
3. Risk assessment
4. Implementation steps
```

---

## Prompt Engineering Tips

### Be Specific

**Bad:**
```
Help me with Kubernetes
```

**Good:**
```
Design a Kubernetes deployment for a Node.js API that:
- Handles 500 RPS with p99 latency < 200ms
- Needs 256MB RAM and 0.2 CPU per instance
- Connects to PostgreSQL and Redis
- Requires zero-downtime deployments
```

### Provide Context

**Bad:**
```
Why is my pod crashing?
```

**Good:**
```
Pod crashing with CrashLoopBackOff.

kubectl describe pod output:
[paste output]

Container logs:
[paste logs]

This started after deploying version 2.1.0 yesterday.
The same image works in staging.
```

### Request Specific Outputs

**Bad:**
```
How do I set up HPA?
```

**Good:**
```
Create an HPA configuration for my deployment that:
- Scales between 3-20 replicas
- Targets 70% CPU and 80% memory utilization
- Has slow scale-down (5 min stabilization)
- Aggressive scale-up (immediate)

Include the HPA YAML and explain each setting.
```

### Ask for Trade-offs

```
Compare deployment strategies for my use case:
[describe application and requirements]

For each strategy (Rolling, Blue-Green, Canary):
1. Pros and cons for my case
2. Resource requirements
3. Complexity to implement
4. Rollback capabilities
5. Recommendation with reasoning
```

---

## LLM Strengths and Limitations

### What LLMs Do Well

| Task | Effectiveness |
|------|---------------|
| Generating YAML configurations | Excellent |
| Explaining K8s concepts | Excellent |
| Reviewing configs for issues | Good |
| Suggesting best practices | Good |
| Troubleshooting common issues | Good |
| Converting between formats | Good |

### What Requires Human Judgment

| Task | Reason |
|------|--------|
| Exact resource numbers | Depends on actual app behavior |
| Cost calculations | Requires current pricing |
| Compliance requirements | Organization-specific |
| Performance tuning | Needs real metrics |
| Incident response | Context-dependent |
| Architecture decisions | Business tradeoffs |

### Iteration Strategy

1. **Start broad** - Get overall architecture
2. **Drill down** - Focus on specific components
3. **Review and refine** - Ask for improvements
4. **Validate** - Test in non-production first
5. **Monitor** - Gather real metrics
6. **Optimize** - Return with actual data
