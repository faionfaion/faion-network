# Service Mesh Implementation Checklist

Step-by-step guide for implementing a service mesh in Kubernetes.

## Phase 1: Assessment and Planning

### 1.1 Requirements Analysis

- [ ] Document current service count and expected growth
- [ ] Identify communication patterns (sync, async, streaming)
- [ ] List security requirements (mTLS, network policies, compliance)
- [ ] Define observability needs (metrics, tracing, logging)
- [ ] Document traffic management requirements (canary, blue-green)
- [ ] Identify latency requirements (p99 SLO)
- [ ] Assess team Kubernetes experience level
- [ ] Review resource constraints (CPU, memory limits)

### 1.2 Service Mesh Selection

- [ ] Evaluate mesh options against requirements:
  - [ ] Istio - Full features, complex
  - [ ] Linkerd - Simple, low overhead
  - [ ] Cilium - eBPF, network policies
  - [ ] Consul Connect - HashiCorp ecosystem
- [ ] Test in development environment
- [ ] Benchmark performance overhead
- [ ] Assess operational complexity
- [ ] Review vendor support options
- [ ] Check CNCF graduation status
- [ ] Document selection decision (ADR)

### 1.3 Architecture Decisions

- [ ] Choose architecture approach:
  - [ ] Sidecar model (traditional)
  - [ ] Ambient/sidecarless (newer)
  - [ ] eBPF-based (Cilium)
- [ ] Define namespace strategy for mesh
- [ ] Plan multi-cluster topology (if needed)
- [ ] Design gateway architecture (ingress/egress)
- [ ] Document architecture decisions in ADR

## Phase 2: Infrastructure Preparation

### 2.1 Cluster Requirements

- [ ] Verify Kubernetes version compatibility
- [ ] Ensure sufficient cluster resources:
  - [ ] Control plane: 2+ vCPU, 4+ GB RAM
  - [ ] Data plane: +50-100 MB per pod (sidecar)
- [ ] Configure CNI compatibility (if Cilium, replace existing CNI)
- [ ] Enable required API features (CRDs)
- [ ] Set up dedicated node pools (optional, for isolation)

### 2.2 Networking Prerequisites

- [ ] Verify pod-to-pod connectivity
- [ ] Configure LoadBalancer/NodePort for ingress
- [ ] Reserve IP ranges for mesh services
- [ ] Configure DNS resolution
- [ ] Set up external DNS (if needed)
- [ ] Review network policies compatibility

### 2.3 Security Prerequisites

- [ ] Set up certificate authority (CA):
  - [ ] Production: External CA (Vault, cert-manager)
  - [ ] Development: Self-signed (acceptable)
- [ ] Configure RBAC for mesh components
- [ ] Set up secrets management
- [ ] Review Pod Security Standards compatibility

## Phase 3: Installation

### 3.1 Control Plane Installation

**Istio:**
- [ ] Download istioctl matching target version
- [ ] Choose installation profile (default, minimal, demo)
- [ ] Customize IstioOperator configuration
- [ ] Install control plane: `istioctl install`
- [ ] Verify istiod is running
- [ ] Check control plane health

**Linkerd:**
- [ ] Install linkerd CLI
- [ ] Run pre-checks: `linkerd check --pre`
- [ ] Generate certificates (production)
- [ ] Install CRDs: `linkerd install --crds`
- [ ] Install control plane: `linkerd install`
- [ ] Verify: `linkerd check`

**Cilium:**
- [ ] Install cilium CLI
- [ ] Remove existing CNI (if replacing)
- [ ] Install Cilium: `cilium install`
- [ ] Enable service mesh features
- [ ] Verify: `cilium status`

### 3.2 Observability Stack

- [ ] Install Prometheus (or integrate existing)
- [ ] Install Grafana with mesh dashboards
- [ ] Install distributed tracing (Jaeger/Tempo)
- [ ] Install service graph (Kiali for Istio)
- [ ] Configure retention policies
- [ ] Set up alerting rules
- [ ] Verify telemetry collection

### 3.3 Ingress Gateway

- [ ] Install ingress gateway component
- [ ] Configure external load balancer
- [ ] Set up TLS termination (Let's Encrypt)
- [ ] Configure Gateway resources
- [ ] Test external traffic routing
- [ ] Set up health checks

## Phase 4: Service Onboarding

### 4.1 Namespace Configuration

- [ ] Label namespaces for injection:
  ```yaml
  # Istio
  istio-injection: enabled
  # Linkerd
  linkerd.io/inject: enabled
  # Cilium
  cilium.io/service-mesh: enabled
  ```
- [ ] Configure default policies per namespace
- [ ] Set up resource quotas for sidecars
- [ ] Define network policies

### 4.2 Application Preparation

- [ ] Review application health checks (readiness/liveness)
- [ ] Verify application handles proxy headers
- [ ] Update deployment manifests for injection
- [ ] Configure appropriate resource requests/limits
- [ ] Add mesh-specific annotations if needed
- [ ] Document service dependencies

### 4.3 Gradual Rollout

- [ ] Start with non-critical services
- [ ] Deploy with permissive mTLS first
- [ ] Verify service-to-service communication
- [ ] Monitor for errors and latency changes
- [ ] Roll out to additional services incrementally
- [ ] Document any issues encountered

## Phase 5: mTLS Configuration

### 5.1 Certificate Management

- [ ] Configure certificate authority:
  - [ ] Self-signed (dev only)
  - [ ] Vault PKI
  - [ ] cert-manager with external CA
- [ ] Set certificate validity period (24h recommended)
- [ ] Configure automatic rotation
- [ ] Set up certificate monitoring/alerting
- [ ] Test certificate renewal process

### 5.2 mTLS Rollout

- [ ] Start with permissive mode (accept plain + mTLS)
- [ ] Verify all services have valid certificates
- [ ] Monitor for plaintext connections
- [ ] Gradually migrate to strict mode per namespace
- [ ] Enable strict mode cluster-wide
- [ ] Verify no plaintext traffic allowed
- [ ] Document exceptions (if any)

### 5.3 mTLS Verification

- [ ] Check certificate status:
  ```bash
  # Istio
  istioctl proxy-config secret <pod>
  # Linkerd
  linkerd viz edges
  ```
- [ ] Verify encryption in transit (tcpdump if needed)
- [ ] Test certificate expiry handling
- [ ] Verify SPIFFE identity format
- [ ] Document troubleshooting procedures

## Phase 6: Traffic Management

### 6.1 Basic Routing

- [ ] Define VirtualService/HTTPRoute for services
- [ ] Configure destination rules
- [ ] Set up service subsets (versions)
- [ ] Test basic routing works
- [ ] Configure default timeouts
- [ ] Set up header-based routing (if needed)

### 6.2 Resilience Patterns

- [ ] Configure retry policies:
  - [ ] Retry count (2-3 typical)
  - [ ] Retry timeout
  - [ ] Retry conditions (5xx, reset)
- [ ] Set up circuit breakers:
  - [ ] Consecutive errors threshold
  - [ ] Ejection time
  - [ ] Max ejection percentage
- [ ] Configure timeouts per route
- [ ] Test failure scenarios
- [ ] Document resilience configuration

### 6.3 Advanced Traffic Patterns

- [ ] Set up canary deployments:
  - [ ] Weight-based routing (90/10)
  - [ ] Flagger integration (optional)
- [ ] Configure blue-green deployments
- [ ] Set up A/B testing (header routing)
- [ ] Configure traffic mirroring (shadow traffic)
- [ ] Test rollback procedures
- [ ] Document deployment processes

## Phase 7: Observability Setup

### 7.1 Metrics Configuration

- [ ] Verify Prometheus scraping mesh metrics
- [ ] Configure key dashboards:
  - [ ] Service health overview
  - [ ] Latency percentiles (p50, p95, p99)
  - [ ] Error rates by service
  - [ ] Request volume
- [ ] Set up SLO-based alerting
- [ ] Configure alert routing (PagerDuty, Slack)

### 7.2 Distributed Tracing

- [ ] Configure trace sampling rate
- [ ] Verify trace propagation headers
- [ ] Set up Jaeger/Tempo dashboards
- [ ] Test end-to-end trace visibility
- [ ] Configure trace retention
- [ ] Document trace debugging procedures

### 7.3 Service Topology

- [ ] Install topology visualization (Kiali)
- [ ] Verify service graph accuracy
- [ ] Set up traffic animation
- [ ] Configure security view
- [ ] Test service dependency analysis

## Phase 8: Security Hardening

### 8.1 Authorization Policies

- [ ] Define default-deny policy (recommended):
  ```yaml
  apiVersion: security.istio.io/v1
  kind: AuthorizationPolicy
  metadata:
    name: deny-all
    namespace: production
  spec: {}
  ```
- [ ] Create allow policies for each service
- [ ] Test service-to-service authorization
- [ ] Verify external access controls
- [ ] Document policy structure

### 8.2 Network Policies

- [ ] Define ingress/egress rules
- [ ] Restrict cross-namespace communication
- [ ] Allow only mesh traffic
- [ ] Test policy enforcement
- [ ] Document network boundaries

### 8.3 Security Monitoring

- [ ] Set up security event alerting
- [ ] Monitor failed authentication attempts
- [ ] Track policy violations
- [ ] Configure audit logging
- [ ] Test incident response procedures

## Phase 9: Performance Tuning

### 9.1 Resource Optimization

- [ ] Right-size sidecar resources:
  - [ ] CPU: 100m-500m typical
  - [ ] Memory: 128Mi-256Mi typical
- [ ] Configure proxy concurrency
- [ ] Tune connection pooling
- [ ] Optimize telemetry sampling
- [ ] Disable unused features

### 9.2 Performance Testing

- [ ] Establish baseline without mesh
- [ ] Benchmark with mesh enabled
- [ ] Test under expected load
- [ ] Test under peak load (2-3x)
- [ ] Measure latency overhead
- [ ] Document performance characteristics

### 9.3 Optimization Iteration

- [ ] Identify performance bottlenecks
- [ ] Tune based on metrics
- [ ] Consider ambient mode for mTLS-only
- [ ] Evaluate eBPF alternatives if needed
- [ ] Re-benchmark after changes

## Phase 10: Operations and Maintenance

### 10.1 Upgrade Planning

- [ ] Subscribe to security announcements
- [ ] Plan regular upgrade cadence (quarterly)
- [ ] Test upgrades in staging first
- [ ] Document rollback procedures
- [ ] Create upgrade runbook

### 10.2 Troubleshooting Preparation

- [ ] Create troubleshooting runbook
- [ ] Document common issues and solutions
- [ ] Set up debug tools (istioctl analyze, linkerd diagnostics)
- [ ] Train team on mesh debugging
- [ ] Create escalation procedures

### 10.3 Documentation

- [ ] Document mesh architecture
- [ ] Create operational runbooks
- [ ] Document service onboarding process
- [ ] Maintain configuration as code
- [ ] Set up change management process

## Quick Reference: Verification Commands

### Istio

```bash
# Check installation
istioctl verify-install

# Analyze configuration
istioctl analyze

# Check proxy status
istioctl proxy-status

# View proxy config
istioctl proxy-config all <pod>

# Check mTLS status
istioctl authn tls-check <pod>
```

### Linkerd

```bash
# Check installation
linkerd check

# View dashboard
linkerd viz dashboard

# Check edges (mTLS)
linkerd viz edges deployment

# View stats
linkerd viz stat deployment

# Tap traffic
linkerd viz tap deployment/<name>
```

### Cilium

```bash
# Check status
cilium status

# Connectivity test
cilium connectivity test

# View endpoints
cilium endpoint list

# Check service mesh
cilium service list
```

## Common Issues Checklist

### mTLS Not Working

- [ ] Check sidecar injection
- [ ] Verify certificates are valid
- [ ] Check PeerAuthentication policy
- [ ] Verify DestinationRule TLS settings
- [ ] Check for port naming issues

### High Latency

- [ ] Check proxy CPU usage
- [ ] Verify connection pooling settings
- [ ] Check for unnecessary retries
- [ ] Review telemetry overhead
- [ ] Consider ambient mode

### Services Not Communicating

- [ ] Verify pods have sidecars
- [ ] Check AuthorizationPolicy
- [ ] Verify NetworkPolicy
- [ ] Check VirtualService routing
- [ ] Review service port naming

---

**Total Items:** 180+
**Phases:** 10
**Est. implementation:** Varies by environment complexity
