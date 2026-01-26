# Kubernetes Resource Management Examples

## Resource Requests and Limits

### Basic Container Resources

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-api
  template:
    metadata:
      labels:
        app: web-api
    spec:
      containers:
      - name: api
        image: myapp:1.0.0
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

### Guaranteed QoS (Critical Service)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
  labels:
    qos: guaranteed
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgres
        image: postgres:15
        resources:
          # requests = limits → Guaranteed QoS
          requests:
            cpu: "2"
            memory: 4Gi
          limits:
            cpu: "2"
            memory: 4Gi
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
```

### Burstable QoS (Standard Workload)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker
  labels:
    qos: burstable
spec:
  replicas: 5
  selector:
    matchLabels:
      app: worker
  template:
    metadata:
      labels:
        app: worker
    spec:
      containers:
      - name: worker
        image: worker:2.0.0
        resources:
          # requests < limits → Burstable QoS
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 1000m      # Can burst to 1 CPU
            memory: 1Gi     # Can burst to 1Gi
```

### JVM Application Resources

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: java-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: java-service
  template:
    metadata:
      labels:
        app: java-service
    spec:
      containers:
      - name: app
        image: java-service:1.0.0
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: "2"
            memory: 2Gi
        env:
        # JVM memory settings aligned with container limits
        - name: JAVA_OPTS
          value: "-Xms512m -Xmx1536m -XX:MaxMetaspaceSize=256m"
```

### Multi-Container Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-with-sidecar
spec:
  containers:
  # Main container
  - name: web
    image: nginx:1.25
    resources:
      requests:
        cpu: 200m
        memory: 256Mi
      limits:
        cpu: 500m
        memory: 512Mi
  # Sidecar container (logging)
  - name: fluentbit
    image: fluent/fluent-bit:2.2
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 100m
        memory: 128Mi
  # Init container
  initContainers:
  - name: init-db
    image: busybox:1.36
    command: ['sh', '-c', 'until nc -z db 5432; do sleep 2; done']
    resources:
      requests:
        cpu: 10m
        memory: 16Mi
      limits:
        cpu: 50m
        memory: 32Mi
```

---

## LimitRange Examples

### Standard LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
  # Container defaults and bounds
  - type: Container
    default:
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    min:
      cpu: 50m
      memory: 64Mi
    max:
      cpu: "4"
      memory: 8Gi
    maxLimitRequestRatio:
      cpu: "10"
      memory: "4"
```

### Pod-Level LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: pod-limits
  namespace: production
spec:
  limits:
  # Pod-level aggregate limits
  - type: Pod
    max:
      cpu: "8"
      memory: 16Gi
    min:
      cpu: 100m
      memory: 128Mi
```

### Storage LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: storage-limits
  namespace: production
spec:
  limits:
  - type: PersistentVolumeClaim
    min:
      storage: 1Gi
    max:
      storage: 100Gi
```

### Development Namespace (Relaxed)

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limits
  namespace: development
spec:
  limits:
  - type: Container
    default:
      cpu: 200m
      memory: 256Mi
    defaultRequest:
      cpu: 50m
      memory: 64Mi
    max:
      cpu: "2"
      memory: 4Gi
```

### Production Namespace (Strict)

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: prod-limits
  namespace: production
spec:
  limits:
  - type: Container
    default:
      cpu: "1"
      memory: 1Gi
    defaultRequest:
      cpu: 250m
      memory: 256Mi
    min:
      cpu: 100m
      memory: 128Mi
    max:
      cpu: "4"
      memory: 8Gi
    maxLimitRequestRatio:
      cpu: "4"      # Limit cannot exceed 4x request
      memory: "2"   # Limit cannot exceed 2x request
```

---

## ResourceQuota Examples

### Basic ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    # Compute resources
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    # Object counts
    pods: "50"
    services: "10"
    secrets: "20"
    configmaps: "20"
```

### Comprehensive ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: full-quota
  namespace: team-alpha
spec:
  hard:
    # Compute requests
    requests.cpu: "10"
    requests.memory: 20Gi
    # Compute limits
    limits.cpu: "20"
    limits.memory: 40Gi
    # Storage
    requests.storage: 100Gi
    persistentvolumeclaims: "10"
    # Object counts
    pods: "30"
    services: "5"
    services.loadbalancers: "1"
    services.nodeports: "2"
    secrets: "15"
    configmaps: "15"
    replicationcontrollers: "5"
    # Ephemeral storage
    requests.ephemeral-storage: 20Gi
    limits.ephemeral-storage: 50Gi
```

### Scoped ResourceQuota (Best-Effort)

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: besteffort-quota
  namespace: batch-jobs
spec:
  hard:
    pods: "100"
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values:
      - low
    - operator: In
      scopeName: BestEffort
      values:
      - "true"
```

### Scoped ResourceQuota (Not Best-Effort)

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: not-besteffort-quota
  namespace: production
spec:
  hard:
    pods: "20"
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
  scopeSelector:
    matchExpressions:
    - operator: NotIn
      scopeName: BestEffort
      values:
      - "true"
```

### Priority-Based Quota

```yaml
# PriorityClass for critical workloads
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: critical
value: 1000000
globalDefault: false
description: "Critical workloads that should not be evicted"
---
# Quota for critical priority
apiVersion: v1
kind: ResourceQuota
metadata:
  name: critical-quota
  namespace: production
spec:
  hard:
    pods: "10"
    requests.cpu: "20"
    requests.memory: 40Gi
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values:
      - critical
```

---

## Combined LimitRange + ResourceQuota

### Complete Namespace Setup

```yaml
# 1. LimitRange: Per-container governance
apiVersion: v1
kind: LimitRange
metadata:
  name: container-limits
  namespace: team-backend
spec:
  limits:
  - type: Container
    default:
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    min:
      cpu: 50m
      memory: 64Mi
    max:
      cpu: "2"
      memory: 4Gi
---
# 2. ResourceQuota: Namespace-wide caps
apiVersion: v1
kind: ResourceQuota
metadata:
  name: namespace-quota
  namespace: team-backend
spec:
  hard:
    requests.cpu: "8"
    requests.memory: 16Gi
    limits.cpu: "16"
    limits.memory: 32Gi
    pods: "25"
    services: "8"
    persistentvolumeclaims: "5"
    requests.storage: 50Gi
---
# 3. Default NetworkPolicy (optional but recommended)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: team-backend
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

---

## Observability Examples

### Prometheus Alerts for Resources

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: resource-alerts
  namespace: monitoring
spec:
  groups:
  - name: kubernetes-resources
    rules:
    # CPU Throttling Alert
    - alert: ContainerCPUThrottling
      expr: |
        rate(container_cpu_cfs_throttled_seconds_total{container!=""}[5m]) > 0.1
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Container {{ $labels.container }} is being CPU throttled"
        description: "Container {{ $labels.container }} in pod {{ $labels.pod }} is being throttled"

    # Memory Near Limit
    - alert: ContainerMemoryNearLimit
      expr: |
        (container_memory_usage_bytes / container_spec_memory_limit_bytes) > 0.85
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Container {{ $labels.container }} memory usage above 85%"

    # OOMKill
    - alert: ContainerOOMKilled
      expr: |
        increase(kube_pod_container_status_restarts_total[1h]) > 0
        and
        kube_pod_container_status_last_terminated_reason{reason="OOMKilled"} == 1
      labels:
        severity: critical
      annotations:
        summary: "Container {{ $labels.container }} was OOMKilled"

    # Quota Exhaustion
    - alert: NamespaceQuotaExhausted
      expr: |
        kube_resourcequota{type="used"} / kube_resourcequota{type="hard"} > 0.9
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Namespace {{ $labels.namespace }} quota {{ $labels.resource }} above 90%"
```

---

*k8s-resources/examples.md | Real-World Examples*
