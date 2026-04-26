# Service Mesh LLM Prompts

Effective prompts for LLM-assisted service mesh design, configuration, and troubleshooting.

## Table of Contents

1. [Mesh Selection](#mesh-selection)
2. [Architecture Design](#architecture-design)
3. [Configuration Generation](#configuration-generation)
4. [Traffic Management](#traffic-management)
5. [Security Configuration](#security-configuration)
6. [Observability Setup](#observability-setup)
7. [Troubleshooting](#troubleshooting)
8. [Migration Planning](#migration-planning)
9. [Performance Optimization](#performance-optimization)

---

## Mesh Selection

### Initial Assessment

```
I need to select a service mesh for my Kubernetes deployment.

Context:
- Cluster: [EKS/GKE/AKS/on-prem]
- Services: [number] microservices
- Traffic: [RPS estimate]
- Team experience: [K8s experience level]
- Current stack: [CNI, ingress, etc.]

Requirements:
- [x] mTLS encryption
- [ ] Advanced traffic management (canary, blue-green)
- [ ] Multi-cluster support
- [ ] L7 network policies
- [ ] [Other requirements]

Constraints:
- Latency SLO: p99 < [X]ms
- Memory budget per pod: [X]Mi
- Team can dedicate [X] hours/week to operations

Compare Istio, Linkerd, and Cilium for this use case. Provide:
1. Feature coverage matrix
2. Expected resource overhead
3. Operational complexity assessment
4. Recommendation with trade-offs
```

### Sidecar vs Sidecarless

```
Compare sidecar and sidecarless service mesh architectures for:

Environment:
- [number] pods across [number] nodes
- Average [X] services per node
- Latency requirement: p99 < [X]ms
- Primary need: [mTLS only / full L7 features]

Consider:
1. Resource overhead (memory, CPU per pod vs per node)
2. Latency impact
3. Operational complexity
4. Feature limitations of sidecarless

Options to compare:
- Istio sidecar mode
- Istio Ambient mode
- Cilium with eBPF
- Linkerd

Recommend the best approach with specific configuration.
```

---

## Architecture Design

### Multi-cluster Design

```
Design a multi-cluster service mesh architecture:

Clusters:
- Primary: [cloud provider, region]
- Secondary: [cloud provider, region]
- Purpose: [DR / geo-distribution / multi-cloud]

Requirements:
- Cross-cluster service discovery
- Unified mTLS trust domain
- Locality-aware load balancing
- Failover within [X] seconds

Services that need cross-cluster:
- [service A] in cluster 1 calls [service B] in cluster 2
- [list other cross-cluster dependencies]

Provide:
1. Architecture diagram (text description)
2. Control plane topology (single primary vs multi-primary)
3. Network connectivity requirements
4. Step-by-step setup procedure
5. Failover testing approach
```

### Gateway Architecture

```
Design an API gateway architecture with service mesh integration:

Current state:
- External traffic: [current ingress solution]
- Internal traffic: [direct pod-to-pod / existing mesh]
- APIs: [REST/GraphQL/gRPC]

Requirements:
- TLS termination at edge
- Rate limiting per client
- Authentication (JWT/OAuth2)
- Request routing by path/header
- mTLS to backend services

Traffic patterns:
- External: [X] RPS peak
- Internal: [X] RPS between services

Recommend:
1. Gateway solution (Istio gateway vs Kong vs Envoy Gateway)
2. Configuration for TLS, auth, rate limiting
3. Integration with service mesh for mTLS
4. Observability setup
```

---

## Configuration Generation

### Generate Istio Configuration

```
Generate Istio configuration for this service:

Service: [name]
Namespace: [namespace]
Port: [port]
Protocol: [HTTP/gRPC/TCP]

Traffic requirements:
- Canary deployment: [X]% to new version
- Timeout: [X]s
- Retries: [X] attempts on [conditions]
- Circuit breaker: after [X] consecutive 5xx errors

Security requirements:
- mTLS: strict
- Allow traffic from: [list of services/namespaces]
- Deny all other traffic

Generate:
1. VirtualService
2. DestinationRule
3. AuthorizationPolicy
4. PeerAuthentication (if needed)

Include comments explaining each configuration choice.
```

### Generate Linkerd Configuration

```
Generate Linkerd configuration for:

Service: [name]
Namespace: [namespace]
Routes:
- GET /api/v1/users/{id} - timeout 5s, retryable
- POST /api/v1/users - timeout 10s, not retryable
- GET /health - timeout 1s, retryable

Authorization:
- Allow from: [service accounts]
- Deny all other

Generate:
1. ServiceProfile with routes
2. Server resource
3. ServerAuthorization
4. TrafficSplit (if canary needed)
```

### Generate Cilium Policies

```
Generate Cilium network policies for:

Service: [name]
Namespace: [namespace]
Function: [API server / worker / database]

Allowed ingress:
- From [service A] on port [X]: allow [HTTP methods/paths OR Kafka topics]
- From [service B] on port [Y]: allow all

Allowed egress:
- To [database] on port 5432
- To [cache] on port 6379
- To external [API endpoint]

Generate:
1. CiliumNetworkPolicy with L3/L4 rules
2. L7 rules where applicable (HTTP, Kafka)
3. Cluster-wide deny-all policy if needed
```

---

## Traffic Management

### Canary Deployment Setup

```
Configure a canary deployment with automatic rollback:

Service: [name]
Current version: v1
New version: v2
Mesh: [Istio/Linkerd/Cilium+Flagger]

Rollout strategy:
- Start: 5% traffic to v2
- Step: increase 10% every [X] minutes
- Max: 50% before full promotion
- Success criteria: error rate < 1%, p99 < 500ms

Failure handling:
- Rollback if: error rate > 5% OR p99 > 1000ms
- Alert on: rollback triggered

Generate:
1. Deployment manifests for v1 and v2
2. Traffic splitting configuration
3. Flagger Canary resource (if using Flagger)
4. Prometheus queries for metrics
5. Alerting rules
```

### Blue-Green Deployment

```
Configure blue-green deployment:

Service: [name]
Mesh: [Istio/Linkerd]
Gateway: [gateway name]

Requirements:
- Instant traffic switch (not gradual)
- Ability to rollback in < 30 seconds
- Pre-switch validation (smoke tests)
- Traffic mirroring before switch (optional)

Generate:
1. Blue and green deployment manifests
2. Service configuration
3. VirtualService/TrafficSplit for switching
4. Rollback procedure
5. Smoke test script
```

### Header-based Routing (A/B Testing)

```
Configure A/B testing with header-based routing:

Service: [name]
Mesh: [Istio/Linkerd]

Routing rules:
- Header "x-test-group: A" -> version v1
- Header "x-test-group: B" -> version v2
- No header -> version v1 (default)
- Cookie "beta=true" -> version v2

Generate complete configuration with:
1. VirtualService/HTTPRoute
2. DestinationRule with subsets
3. Example curl commands to test
```

---

## Security Configuration

### Zero Trust Setup

```
Configure zero-trust security for namespace:

Namespace: [namespace]
Mesh: [Istio/Linkerd/Cilium]

Services and their dependencies:
- frontend: calls api-gateway
- api-gateway: calls users, orders, payments
- users: calls database
- orders: calls database, inventory
- payments: calls external-payment-api

Requirements:
- Default deny all
- mTLS strict
- Only allow documented dependencies
- External egress only from payments service

Generate:
1. Namespace-level deny-all policy
2. Service-specific allow policies
3. Egress policy for external API
4. mTLS enforcement configuration
5. Verification commands
```

### mTLS Migration

```
Plan mTLS migration from permissive to strict:

Current state:
- Mesh: [Istio/Linkerd] installed
- Namespaces: [list]
- Some services not yet in mesh

Goal:
- Cluster-wide strict mTLS
- No service disruption

Generate:
1. Pre-migration checklist
2. Step-by-step migration procedure
3. Monitoring queries to detect plaintext traffic
4. Rollback procedure
5. Verification commands
```

### External CA Integration

```
Configure service mesh with external CA:

Mesh: [Istio/Linkerd]
CA: [Vault/cert-manager/AWS ACM PCA]

Requirements:
- Certificates from external CA
- Automatic rotation
- Short-lived certificates (24h)
- SPIFFE identity format

Generate:
1. CA configuration (Vault setup or cert-manager issuer)
2. Mesh configuration to use external CA
3. Certificate rotation verification
4. Monitoring for certificate expiry
```

---

## Observability Setup

### Full Stack Observability

```
Configure observability stack for service mesh:

Mesh: [Istio/Linkerd/Cilium]
Existing stack: [Prometheus/Grafana/none]

Requirements:
- Metrics: request rate, error rate, latency percentiles
- Tracing: 10% sampling, correlation with logs
- Logs: structured JSON, trace ID correlation
- Service graph visualization

Generate:
1. Prometheus scrape configuration
2. Grafana dashboard JSON for RED metrics
3. Jaeger/Tempo configuration
4. Log format configuration
5. Alerting rules for SLO violations
```

### SLO-based Alerting

```
Configure SLO-based alerting for service mesh:

SLOs:
- Availability: 99.9% (error rate < 0.1%)
- Latency: p99 < 500ms

Alert tiers:
- Page (critical): 1% error budget burned in 1 hour
- Ticket (warning): 10% error budget burned in 6 hours
- Info: 50% error budget burned in 24 hours

Generate:
1. Prometheus recording rules for error budget
2. Alerting rules for each tier
3. Grafana dashboard showing error budget
4. Alert routing configuration (example for Alertmanager)
```

---

## Troubleshooting

### Connectivity Issues

```
Help troubleshoot service mesh connectivity issue:

Mesh: [Istio/Linkerd/Cilium]
Symptom: [describe the issue]

Service A (source):
- Namespace: [namespace]
- Pod name: [pod]
- Sidecar status: [injected/not injected]

Service B (destination):
- Namespace: [namespace]
- Service name: [service]
- Port: [port]

Error message:
```
[paste error message]
```

I've already tried:
- [list what you've checked]

Provide:
1. Diagnostic commands to run
2. What to look for in output
3. Common causes for this symptom
4. Resolution steps
```

### High Latency Investigation

```
Help investigate high latency in service mesh:

Mesh: [Istio/Linkerd]
Service: [name]
Normal latency: p99 ~[X]ms
Current latency: p99 ~[Y]ms

When it started: [timestamp/event]
Changes made recently: [list any changes]

Current metrics:
- CPU usage: [X]%
- Memory usage: [X]%
- Request rate: [X] RPS

Provide:
1. Diagnostic queries (Prometheus)
2. Proxy-level investigation commands
3. Common latency causes in service mesh
4. Optimization recommendations
```

### mTLS Failures

```
Troubleshoot mTLS authentication failure:

Mesh: [Istio/Linkerd]
Error: [paste error]

Source:
- Service: [name]
- Namespace: [namespace]
- Service account: [sa]

Destination:
- Service: [name]
- Namespace: [namespace]

Current configuration:
```yaml
[paste relevant configs]
```

Provide:
1. Certificate inspection commands
2. Policy verification steps
3. Common mTLS issues and fixes
4. How to verify fix worked
```

---

## Migration Planning

### Migrate to Service Mesh

```
Plan migration to service mesh:

Current state:
- [X] services in Kubernetes
- No service mesh
- Traffic: direct pod-to-pod
- Security: network policies only
- Observability: [current stack]

Target state:
- Mesh: [Istio/Linkerd/Cilium]
- mTLS everywhere
- Canary deployments
- Unified observability

Constraints:
- Zero downtime
- Gradual migration (not big bang)
- Some services can't have sidecars (e.g., [list])

Generate:
1. Migration phases with milestones
2. Namespace migration order (least critical first)
3. Rollback procedure per phase
4. Success criteria per phase
5. Risk assessment and mitigation
```

### Migrate Between Meshes

```
Plan migration from [source mesh] to [target mesh]:

Current state:
- Mesh: [Istio/Linkerd/Consul]
- Services: [count]
- Current features used: [list]

Target:
- Mesh: [Istio/Linkerd/Cilium]
- Reason for migration: [cost/performance/features]

Constraints:
- Zero downtime
- [X] weeks migration window
- Team of [X] engineers

Generate:
1. Feature mapping (current vs new mesh)
2. Configuration translation guide
3. Migration strategy (parallel run vs cutover)
4. Validation test plan
5. Rollback procedure
```

---

## Performance Optimization

### Resource Optimization

```
Optimize service mesh resource usage:

Mesh: [Istio/Linkerd]
Current state:
- Pods: [count]
- Sidecar CPU: [request/limit]
- Sidecar memory: [request/limit]
- Control plane resources: [current]

Observed issues:
- [high memory usage / high CPU / slow startup / etc.]

Traffic patterns:
- RPS per service: [range]
- Payload size: [average]
- Connection patterns: [many short / few long]

Generate:
1. Resource tuning recommendations
2. Proxy configuration optimizations
3. Control plane scaling recommendations
4. Metrics to monitor after changes
```

### Latency Optimization

```
Reduce service mesh latency overhead:

Mesh: [Istio/Linkerd/Cilium]
Current overhead: [X]ms added latency
Target: < [Y]ms

Current configuration:
```yaml
[paste relevant config]
```

Features in use:
- [ ] mTLS
- [ ] Access logging
- [ ] Tracing (sampling rate: [X]%)
- [ ] Metrics
- [ ] Authorization policies

Generate:
1. Configuration changes to reduce latency
2. Features that can be disabled/tuned
3. Alternative approaches (ambient mode, eBPF)
4. Expected improvement per change
5. Trade-offs of each optimization
```

---

## Prompt Engineering Tips

### Context to Always Include

1. **Mesh and version** - Configurations differ significantly
2. **Kubernetes version** - API compatibility matters
3. **Cloud provider** - LoadBalancer, CNI specifics
4. **Current configuration** - Paste YAML when troubleshooting
5. **Error messages** - Exact text, not paraphrased

### Effective Prompt Structure

```
1. State the goal clearly
2. Provide relevant context (environment, constraints)
3. List specific requirements
4. Ask for specific outputs (YAML, commands, explanations)
5. Request trade-off analysis when choosing between options
```

### Follow-up Prompts

After receiving configuration:
```
Review the generated configuration for:
1. Security issues
2. Resource over/under provisioning
3. Missing best practices
4. Potential operational issues

Explain any concerns and suggest improvements.
```

After troubleshooting:
```
The issue is now resolved. Generate:
1. Post-incident documentation
2. Preventive measures
3. Monitoring additions to detect this earlier
```
