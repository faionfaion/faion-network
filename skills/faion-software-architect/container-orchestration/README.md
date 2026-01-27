# Container Orchestration

Kubernetes architecture patterns, pod design, deployment strategies, and operational best practices.

## Overview

Container orchestration automates the deployment, management, scaling, and networking of containers. Kubernetes has become the de facto standard, adopted by 93% of organizations for production workloads.

**Core Value Proposition:**
- **Declarative Configuration** - Define desired state, K8s maintains it
- **Self-Healing** - Auto-restart failed containers, replace unhealthy pods
- **Horizontal Scaling** - Scale workloads based on metrics or events
- **Service Discovery** - Built-in DNS and load balancing
- **Rolling Updates** - Zero-downtime deployments
- **Secret Management** - Secure handling of sensitive data

## Kubernetes Architecture

### Control Plane Components

| Component | Purpose |
|-----------|---------|
| **API Server** | Front door for all cluster operations, validates and processes requests |
| **etcd** | Distributed key-value store for cluster state |
| **Scheduler** | Assigns pods to nodes based on resources, affinity, taints |
| **Controller Manager** | Runs controllers (replication, node, endpoint, service account) |
| **Cloud Controller** | Integrates with cloud provider APIs |

### Worker Node Components

| Component | Purpose |
|-----------|---------|
| **kubelet** | Agent ensuring containers run in pods |
| **kube-proxy** | Network proxy maintaining network rules |
| **Container Runtime** | containerd, CRI-O, or other CRI-compliant runtime |

### Resource Hierarchy

```
Cluster
  └── Namespace (isolation boundary)
        └── Deployment / StatefulSet / DaemonSet
              └── ReplicaSet
                    └── Pod
                          └── Container(s)
```

## Pod Design Patterns

### Sidecar Pattern

Extends main container functionality without modification.

**Use Cases:**
- Log collection (Fluentd, Fluent Bit)
- Service mesh proxy (Envoy, Linkerd-proxy)
- Secrets injection (Vault Agent)
- File synchronization (git-sync)

**Native Sidecar Support (K8s 1.33+):**
Init containers with `restartPolicy: Always` are treated as native sidecars:
- Start before main containers
- Run throughout pod lifecycle
- Terminate after main containers exit

### Ambassador Pattern

Proxy for accessing external services, hiding complexity from the main container.

**Use Cases:**
- Database connection pooling
- API gateway for external services
- Protocol translation
- Rate limiting to external APIs

### Adapter Pattern

Standardizes output from the main container.

**Use Cases:**
- Log format normalization (different apps to unified format)
- Metrics conversion (custom format to Prometheus)
- Protocol adaptation

### Init Containers

Run to completion before app containers start.

**Use Cases:**
- Database schema migration
- Configuration file generation
- Waiting for dependencies
- Downloading assets

## Resource Management

### CPU and Memory

```yaml
resources:
  requests:    # Guaranteed resources (scheduling)
    memory: "256Mi"
    cpu: "250m"
  limits:      # Maximum allowed
    memory: "512Mi"
    cpu: "500m"
```

**Best Practices:**
- Always set both requests and limits
- Set requests close to actual usage for efficient scheduling
- Memory limits prevent OOM kills from affecting other pods
- CPU limits prevent noisy neighbors
- Use VPA (Vertical Pod Autoscaler) for tuning

### Quality of Service Classes

| QoS Class | Condition | Eviction Priority |
|-----------|-----------|-------------------|
| **Guaranteed** | requests = limits for all containers | Lowest (last evicted) |
| **Burstable** | requests < limits | Medium |
| **BestEffort** | No requests or limits | Highest (first evicted) |

### Resource Quotas

Limit total resources per namespace:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "50"
```

## Deployment Strategies

### Rolling Update (Default)

Gradual replacement of old pods with new ones.

| Parameter | Purpose |
|-----------|---------|
| `maxSurge` | Extra pods during update (absolute or %) |
| `maxUnavailable` | Pods that can be unavailable (absolute or %) |

**Best For:** Standard deployments, minimal resource overhead.

### Blue-Green Deployment

Two identical environments, instant traffic switch.

**Pros:**
- Instant rollback
- No mixed versions
- Full testing before switch

**Cons:**
- Double infrastructure cost during deployment
- Database schema changes need careful handling

**Best For:** Critical applications requiring instant rollback capability.

### Canary Deployment

Gradual traffic shift to new version (2% -> 25% -> 75% -> 100%).

**Pros:**
- Lowest risk
- Real production testing
- Metrics-based progression

**Cons:**
- Requires sophisticated traffic management
- Longer deployment time
- Application must support multiple versions

**Tools:** Argo Rollouts, Flagger, Istio, Linkerd

**Best For:** Applications where risk minimization is critical.

### Recreate Strategy

Terminate all pods, then create new ones.

**Best For:** Development environments, non-critical workloads, when old/new versions cannot coexist.

## Autoscaling

### Horizontal Pod Autoscaler (HPA)

Scale based on CPU, memory, or custom metrics:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: External
    external:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

### KEDA (Kubernetes Event-Driven Autoscaling)

Scale based on external events (queue depth, Kafka lag, HTTP requests):

**Key Features:**
- Scale to zero (HPA requires min 1 replica)
- 60+ scalers (Kafka, RabbitMQ, SQS, Prometheus, PostgreSQL, etc.)
- Cron-based scaling
- Custom metrics

**When to Use KEDA vs HPA:**
| Scenario | Use |
|----------|-----|
| CPU/Memory scaling | HPA |
| Queue-based workloads | KEDA |
| Scale to zero needed | KEDA |
| Event-driven processing | KEDA |
| Simple web services | HPA |

### Vertical Pod Autoscaler (VPA)

Automatically adjust resource requests/limits based on usage.

**Modes:**
- **Off**: Recommendations only
- **Initial**: Set at pod creation
- **Auto**: Update running pods (requires restart)

## Persistent Storage

### Storage Class

Define storage types available in cluster:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "10000"
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
```

### Access Modes

| Mode | Abbreviation | Description |
|------|--------------|-------------|
| ReadWriteOnce | RWO | Single node read-write |
| ReadOnlyMany | ROX | Multiple nodes read-only |
| ReadWriteMany | RWX | Multiple nodes read-write |
| ReadWriteOncePod | RWOP | Single pod read-write (K8s 1.27+) |

### Best Practices

- Use CSI drivers (not FlexVolume or in-tree drivers)
- Dynamic provisioning over static
- WaitForFirstConsumer for multi-zone clusters
- Enable volume expansion for growth
- VolumeSnapshots for backups
- Velero for disaster recovery

## Security

### RBAC (Role-Based Access Control)

```yaml
# Role: what actions are allowed
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
# RoleBinding: who gets the role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
subjects:
- kind: ServiceAccount
  name: app-sa
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**Best Practices:**
- Principle of least privilege
- Dedicated service accounts per workload
- Disable automounting when not needed
- Use namespaces for isolation
- Audit RBAC regularly

### Network Policies

Default: all pods can communicate. Network policies restrict this.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-ingress
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend
    - podSelector:
        matchLabels:
          app: web
    ports:
    - port: 8080
```

### Pod Security Standards

| Profile | Description |
|---------|-------------|
| **Privileged** | Unrestricted |
| **Baseline** | Minimal restrictions, prevent known escalations |
| **Restricted** | Hardened, security best practices |

### Security Best Practices 2025

- Use distroless or minimal base images
- Scan images with Trivy, Snyk, or Grype
- Sign images with cosign/Sigstore
- Enable SBOM generation
- Use eBPF-based runtime security (Falco, Tetragon)
- Implement Zero Trust with service mesh mTLS
- Encrypt secrets at rest (Sealed Secrets, External Secrets, Vault)

## ConfigMaps and Secrets

### ConfigMap Usage

```yaml
# As environment variables
envFrom:
- configMapRef:
    name: app-config

# As files
volumes:
- name: config
  configMap:
    name: app-config
```

### Secrets Best Practices

- Never commit secrets to Git
- Use External Secrets Operator for cloud secrets
- Sealed Secrets for GitOps workflows
- HashiCorp Vault for dynamic secrets
- Enable encryption at rest in etcd
- Rotate secrets regularly

## Health Checks

### Probe Types

| Probe | Purpose | Action on Failure |
|-------|---------|-------------------|
| **livenessProbe** | Is container alive? | Restart container |
| **readinessProbe** | Is container ready for traffic? | Remove from Service |
| **startupProbe** | Has container started? | Disable other probes until success |

### Probe Methods

- **httpGet**: HTTP GET request
- **tcpSocket**: TCP connection
- **exec**: Execute command
- **grpc**: gRPC health check (K8s 1.27+)

### Configuration Parameters

| Parameter | Description | Recommended |
|-----------|-------------|-------------|
| `initialDelaySeconds` | Delay before first probe | Based on app startup |
| `periodSeconds` | Probe interval | 10-30s |
| `timeoutSeconds` | Probe timeout | 1-5s |
| `failureThreshold` | Failures before action | 3 |
| `successThreshold` | Successes to recover | 1 |

## Observability

### Metrics

- **Prometheus** + **Grafana** for metrics and dashboards
- **kube-state-metrics** for K8s object states
- **metrics-server** for HPA

### Logging

- **Fluentd/Fluent Bit** for log collection
- **Loki** or **Elasticsearch** for storage
- Structured JSON logging recommended

### Tracing

- **OpenTelemetry** as the standard
- **Jaeger** or **Tempo** for storage
- Trace context propagation in services

## LLM-Assisted Container Design

### Effective Prompts

1. **Architecture Review**: "Review this Kubernetes deployment for production readiness"
2. **Security Audit**: "Identify security issues in this pod specification"
3. **Resource Tuning**: "Suggest resource requests/limits for a Node.js API with 1000 RPS"
4. **Migration**: "Convert this Docker Compose to Kubernetes manifests"

### What LLMs Excel At

- Generating boilerplate YAML
- Explaining Kubernetes concepts
- Reviewing configurations for issues
- Converting between formats
- Suggesting best practices

### What Requires Human Judgment

- Capacity planning numbers
- Business-specific requirements
- Cost vs performance tradeoffs
- Organizational security policies

## Quick Reference

### Key Commands

```bash
# Apply configuration
kubectl apply -f manifest.yaml

# Check deployment status
kubectl rollout status deployment/app

# View pod logs
kubectl logs -f pod/app-xxx

# Debug pod
kubectl exec -it pod/app-xxx -- /bin/sh

# Scale deployment
kubectl scale deployment app --replicas=5

# Rollback deployment
kubectl rollout undo deployment/app
```

### Common Issues

| Issue | Check |
|-------|-------|
| Pod not starting | `kubectl describe pod`, events section |
| CrashLoopBackOff | Container logs, liveness probe config |
| ImagePullBackOff | Image name, registry credentials |
| Pending pods | Node resources, scheduling constraints |
| Service not working | Selector labels, endpoint pods |

## Related Methodologies

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step orchestration design checklist |
| [examples.md](examples.md) | Real-world orchestration configurations |
| [templates.md](templates.md) | Copy-paste Kubernetes configurations |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted design |

## External Resources

### Official Documentation
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

### Tools
- [KEDA - Event-driven Autoscaling](https://keda.sh/)
- [Argo Rollouts - Progressive Delivery](https://argoproj.github.io/rollouts/)
- [Velero - Backup and Disaster Recovery](https://velero.io/)
- [External Secrets Operator](https://external-secrets.io/)

### Learning
- [KodeKloud - Kubernetes Best Practices 2025](https://kodekloud.com/blog/kubernetes-best-practices-2025/)
- [Plural - Kubernetes Basics Guide](https://www.plural.sh/blog/kubernetes-basics-guide/)

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [microservices-architecture](../microservices-architecture/) | Service design for K8s |
| [cloud-architecture](../cloud-architecture/) | Cloud provider K8s services |
| [observability-architecture](../observability-architecture/) | Monitoring K8s workloads |
| [security-architecture](../security-architecture/) | K8s security patterns |
| [service-mesh](../service-mesh/) | Advanced networking |
