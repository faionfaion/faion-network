# Kubernetes Deployment

**Production-Grade Container Orchestration (2025-2026)**

---

## Overview

Kubernetes (K8s) orchestrates containerized applications across clusters, providing automated deployment, scaling, and management. This skill covers production-grade deployment patterns: Deployments, StatefulSets, rolling updates, canary deployments, and progressive delivery.

---

## Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Production readiness and deployment checklists |
| [examples.md](examples.md) | Deployments, StatefulSets, rolling updates, canary patterns |
| [templates.md](templates.md) | Production YAML templates for common workloads |
| [llm-prompts.md](llm-prompts.md) | AI prompts for Kubernetes deployment tasks |

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Pod** | Smallest deployable unit, one or more containers |
| **Deployment** | Manages ReplicaSets, enables declarative updates |
| **StatefulSet** | Ordered, stable pods for stateful workloads |
| **ReplicaSet** | Maintains a stable set of replica pods |
| **Service** | Stable network endpoint for pods |
| **ConfigMap** | Non-sensitive configuration data |
| **Secret** | Sensitive data (passwords, tokens) |
| **Ingress** | External HTTP/HTTPS routing |
| **PDB** | Pod Disruption Budget for availability |
| **HPA** | Horizontal Pod Autoscaler for scaling |

---

## Deployment vs StatefulSet

| Feature | Deployment | StatefulSet |
|---------|------------|-------------|
| Pod identity | Random, interchangeable | Stable, persistent |
| Pod naming | `{name}-{random}` | `{name}-{ordinal}` (0, 1, 2...) |
| Storage | Shared volumes | Persistent volume per pod |
| Scaling | Parallel, any order | Ordered (scale up: 0,1,2; down: 2,1,0) |
| Updates | Parallel possible | One at a time, ordered |
| Use case | Stateless apps, APIs | Databases, distributed systems |

### When to Use What

| Workload Type | Resource | Reason |
|---------------|----------|--------|
| Web API | Deployment | Stateless, scale horizontally |
| Worker queue | Deployment | Stateless, parallel processing |
| PostgreSQL | StatefulSet | Persistent identity and storage |
| Redis cluster | StatefulSet | Ordered startup, stable network IDs |
| Elasticsearch | StatefulSet | Each node needs unique identity |
| Frontend/Next.js | Deployment | Stateless, fast rollouts |
| Kafka | StatefulSet | Broker IDs must be stable |

---

## Deployment Strategies (2025-2026)

### Strategy Comparison

| Strategy | Zero Downtime | Rollback | Traffic Control | Complexity |
|----------|---------------|----------|-----------------|------------|
| **Rolling Update** | Yes | kubectl rollout undo | No | Low |
| **Recreate** | No | Manual | No | Low |
| **Blue-Green** | Yes | Instant switch | Binary | Medium |
| **Canary** | Yes | Gradual | Percentage-based | High |
| **A/B Testing** | Yes | Gradual | Header/cookie-based | High |

### Rolling Update (Default)

Standard Kubernetes strategy. Gradually replaces old pods with new ones.

```
Old: [Pod1] [Pod2] [Pod3]
     [Pod1] [Pod2] [NewPod3]    <- New pod starts
     [Pod1] [NewPod2] [NewPod3] <- Another new pod
     [NewPod1] [NewPod2] [NewPod3] <- Complete
```

**Best for:** Most production workloads, stateless services.

### Recreate

Terminates all old pods before creating new ones. Causes downtime.

```
Old: [Pod1] [Pod2] [Pod3]
     [    ] [    ] [    ]       <- All terminated
     [NewPod1] [NewPod2] [NewPod3] <- New pods created
```

**Best for:** Development, when you cannot run two versions simultaneously.

### Blue-Green

Run two identical environments, switch traffic atomically.

```
Blue (current):  [Pod1] [Pod2] [Pod3] <- Live traffic
Green (new):     [NewPod1] [NewPod2] [NewPod3] <- Waiting

Service selector change:

Blue:            [Pod1] [Pod2] [Pod3] <- No traffic
Green:           [NewPod1] [NewPod2] [NewPod3] <- Live traffic
```

**Best for:** High-risk deployments requiring instant rollback.

### Canary

Gradually shift traffic to new version, monitor, then proceed.

```
Stable:  [Pod1] [Pod2] [Pod3] <- 90% traffic
Canary:  [NewPod1]            <- 10% traffic

Monitor metrics...

Stable:  [Pod1] [Pod2]        <- 70% traffic
Canary:  [NewPod1] [NewPod2]  <- 30% traffic

Continue until 100% on new version
```

**Best for:** Production releases with progressive confidence building.

### Progressive Delivery with Argo Rollouts (2025-2026 Standard)

```
Analysis: Prometheus metrics, web hooks, experiments
          |
Strategy: Canary 10% -> 30% -> 50% -> 100%
          |
Pause:    Automatic analysis between steps
          |
Rollback: Automatic on failure
```

**Best for:** Enterprise deployments, GitOps workflows.

---

## Key Principles (2025-2026)

### 1. GitOps as Standard

- Git is the single source of truth
- All changes via pull requests
- Automated reconciliation (Argo CD, Flux)
- Audit trail for all deployments

### 2. Progressive Delivery

- Use Argo Rollouts or Flagger for canary
- Automated analysis with Prometheus/Datadog
- Traffic shifting with service mesh or Ingress
- Automatic rollback on metric degradation

### 3. Policy-Driven Security

Enable policy engines from day one:

| Tool | Type | Features |
|------|------|----------|
| **Kyverno** | K8s-native | YAML policies, generate resources |
| **OPA Gatekeeper** | Rego-based | Complex policies, admission control |
| **Polaris** | Best practices | Built-in checks, dashboard |

### 4. Resource Management

- Always set requests AND limits
- Use HPA for automatic scaling
- Define PodDisruptionBudget for availability
- Use VerticalPodAutoscaler for right-sizing

### 5. Zero Trust Security

- NetworkPolicies for pod-to-pod communication
- mTLS via service mesh (Istio, Linkerd)
- RBAC with least privilege
- Pod Security Standards (baseline/restricted)

---

## Production Best Practices (2025-2026)

### Deployment Configuration

| Practice | Description |
|----------|-------------|
| Resource limits | Always set CPU/memory requests and limits |
| All three probes | Liveness, readiness, and startup probes |
| PDB defined | Minimum available pods during disruptions |
| HPA configured | Auto-scale based on CPU/memory/custom metrics |
| Topology spread | Distribute pods across zones/nodes |
| Pod anti-affinity | Avoid co-locating same app pods |
| Revision history | Keep `revisionHistoryLimit: 5` for rollbacks |

### StatefulSet Configuration

| Practice | Description |
|----------|-------------|
| Headless service | Required for stable network identity |
| PVC per pod | volumeClaimTemplates for data persistence |
| Ordered deployment | podManagementPolicy: OrderedReady (default) |
| Graceful termination | terminationGracePeriodSeconds appropriate for cleanup |
| Anti-affinity | Spread across nodes for HA |

### Rolling Update Tuning

| Parameter | Default | Recommended | Description |
|-----------|---------|-------------|-------------|
| maxUnavailable | 25% | 1 or 0 | Pods that can be unavailable |
| maxSurge | 25% | 1 or 25% | Extra pods during update |

**Zero-downtime config:**
```yaml
maxUnavailable: 0
maxSurge: 1
```

**Fast rollout config:**
```yaml
maxUnavailable: 25%
maxSurge: 25%
```

### Health Probes

| Probe | Purpose | Action on Failure |
|-------|---------|-------------------|
| **Startup** | Wait for app initialization | Block liveness/readiness |
| **Liveness** | Check if app is running | Restart container |
| **Readiness** | Check if app can receive traffic | Remove from service |

**Probe timing guidelines:**

| Setting | Startup | Liveness | Readiness |
|---------|---------|----------|-----------|
| initialDelaySeconds | 0 | 0 | 0 |
| periodSeconds | 5-10 | 10-30 | 5-10 |
| timeoutSeconds | 5 | 5 | 3 |
| failureThreshold | 30 | 3 | 3 |
| successThreshold | 1 | 1 | 1 |

---

## 2025-2026 Trends

### Platform Engineering

- Internal Developer Platforms (IDPs) on K8s
- Self-service deployment via Backstage/Port
- Golden paths with pre-configured templates
- Reduced cognitive load for developers

### FinOps for Kubernetes

- Cost visibility with Kubecost/OpenCost
- Right-sizing with VPA recommendations
- Spot/preemptible node pools for non-critical
- Namespace-level resource quotas

### AI/ML Workloads

- GPU scheduling with device plugins
- Kubeflow for ML pipelines
- KEDA for event-driven scaling
- Volcano for batch/AI workloads

### Security Evolution

- Pod Security Standards (PSS) replace PSP
- Sigstore for supply chain security
- eBPF-based runtime security (Cilium, Falco)
- Zero-trust with service mesh

### Multi-Cluster Management

- Cluster API for lifecycle management
- Federation with Liqo/Admiralty
- GitOps for multi-cluster (Argo CD ApplicationSets)
- Service mesh spanning clusters

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| No resource limits | OOM kills, noisy neighbors | Always set requests and limits |
| Missing probes | Traffic to unready pods, stuck pods | Configure all three probes |
| No PDB | All pods evicted during drain | Define minAvailable or maxUnavailable |
| Using `latest` tag | Unpredictable deployments | Use specific versions with digest |
| Secrets in ConfigMaps | Security risk | Use Secrets, external vault |
| No anti-affinity | All pods on one node | Configure podAntiAffinity |
| Ignoring RBAC | Over-privileged workloads | Least privilege service accounts |
| No NetworkPolicy | Unrestricted pod communication | Default deny, explicit allow |

---

## Tools (2025-2026)

| Tool | Purpose |
|------|---------|
| [Argo Rollouts](https://argoproj.github.io/rollouts/) | Progressive delivery, canary, blue-green |
| [Flagger](https://flagger.app/) | Progressive delivery with service mesh |
| [Argo CD](https://argoproj.github.io/cd/) | GitOps continuous delivery |
| [Flux](https://fluxcd.io/) | GitOps toolkit |
| [Kyverno](https://kyverno.io/) | Kubernetes-native policy engine |
| [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/) | Policy enforcement |
| [Polaris](https://www.fairwinds.com/polaris) | Best practices validation |
| [Kubecost](https://kubecost.com/) | Cost monitoring and optimization |
| [KEDA](https://keda.sh/) | Event-driven autoscaling |
| [k9s](https://k9scli.io/) | Terminal UI for K8s |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Deployment manifest creation | sonnet | K8s pattern application |
| Rolling update strategy | sonnet | Availability trade-offs |
| Resource requests/limits | sonnet | Capacity planning |
| Health probe configuration | haiku | Simple rule application |

## Sources

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kubernetes Deployment Strategies 2025](https://octopus.com/devops/kubernetes-deployments/)
- [14 Kubernetes Best Practices 2025](https://komodor.com/learn/14-kubernetes-best-practices-you-must-know-in-2025/)
- [kubectl rollout Best Practices 2025](https://scaleops.com/blog/kubectl-rollout-7-best-practices-for-production-2025/)
- [Kubernetes Configuration Good Practices](https://kubernetes.io/blog/2025/11/25/configuration-good-practices/)
- [Top 5 Kubernetes Management Lessons - CNCF](https://www.cncf.io/blog/2025/11/18/top-5-hard-earned-lessons-from-the-experts-on-managing-kubernetes/)
- [Kubernetes Production Best Practices](https://learnkube.com/production-best-practices)
- [Kubernetes 2025 Review & 2026 Forecast](https://www.arcfra.com/blog/kubernetes_2025_review_2026_forecast)
- [Top 8 Kubernetes Mistakes to Avoid in 2026](https://cpluz.com/blog/2025s-top-8-kubernetes-deployment-mistakes-to-avoid-in-2026/)
- [17 Kubernetes Best Practices - Spacelift](https://spacelift.io/blog/kubernetes-best-practices)

---

*Kubernetes Deployment | faion-infrastructure-engineer*
