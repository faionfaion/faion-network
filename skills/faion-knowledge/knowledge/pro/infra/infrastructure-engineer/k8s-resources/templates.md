# Kubernetes Resource Management Templates

Copy-paste templates for common resource management scenarios.

---

## Deployment with Resources

### Basic Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${TAG}
        ports:
        - containerPort: ${PORT}
        resources:
          requests:
            cpu: ${CPU_REQUEST}
            memory: ${MEMORY_REQUEST}
          limits:
            cpu: ${CPU_LIMIT}
            memory: ${MEMORY_LIMIT}
        livenessProbe:
          httpGet:
            path: /health
            port: ${PORT}
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: ${PORT}
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Guaranteed QoS Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
        qos: guaranteed
    spec:
      priorityClassName: high-priority
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${TAG}
        resources:
          # requests = limits for Guaranteed QoS
          requests:
            cpu: ${CPU}
            memory: ${MEMORY}
          limits:
            cpu: ${CPU}
            memory: ${MEMORY}
```

---

## LimitRange Templates

### Standard LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: standard-limits
  namespace: ${NAMESPACE}
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
      cpu: "4"
      memory: 8Gi
```

### Development LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limits
  namespace: ${NAMESPACE}
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

### Production LimitRange (Strict)

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: prod-limits
  namespace: ${NAMESPACE}
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
      cpu: "4"
      memory: "2"
  - type: Pod
    max:
      cpu: "8"
      memory: 16Gi
```

### Storage LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: storage-limits
  namespace: ${NAMESPACE}
spec:
  limits:
  - type: PersistentVolumeClaim
    min:
      storage: 1Gi
    max:
      storage: ${MAX_STORAGE}
```

---

## ResourceQuota Templates

### Basic ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: basic-quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: ${TOTAL_CPU_REQUESTS}
    requests.memory: ${TOTAL_MEMORY_REQUESTS}
    limits.cpu: ${TOTAL_CPU_LIMITS}
    limits.memory: ${TOTAL_MEMORY_LIMITS}
    pods: ${MAX_PODS}
```

### Team ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: ${TEAM_NAMESPACE}
spec:
  hard:
    # Compute
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    # Storage
    requests.storage: 100Gi
    persistentvolumeclaims: "10"
    # Objects
    pods: "50"
    services: "10"
    secrets: "20"
    configmaps: "20"
```

### Multi-Tier Quotas

```yaml
# Tier 1: Small team
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tier1-quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"
---
# Tier 2: Medium team
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tier2-quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: "16"
    requests.memory: 32Gi
    limits.cpu: "32"
    limits.memory: 64Gi
    pods: "50"
---
# Tier 3: Large team
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tier3-quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: "64"
    requests.memory: 128Gi
    limits.cpu: "128"
    limits.memory: 256Gi
    pods: "100"
```

---

## Complete Namespace Setup

### Full Namespace Template

```yaml
# 1. Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    team: ${TEAM}
    environment: ${ENV}
---
# 2. LimitRange
apiVersion: v1
kind: LimitRange
metadata:
  name: limits
  namespace: ${NAMESPACE}
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
      cpu: "4"
      memory: 8Gi
---
# 3. ResourceQuota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: ${TOTAL_CPU_REQUESTS}
    requests.memory: ${TOTAL_MEMORY_REQUESTS}
    limits.cpu: ${TOTAL_CPU_LIMITS}
    limits.memory: ${TOTAL_MEMORY_LIMITS}
    pods: ${MAX_PODS}
    services: ${MAX_SERVICES}
    persistentvolumeclaims: ${MAX_PVCS}
    requests.storage: ${TOTAL_STORAGE}
---
# 4. Default NetworkPolicy (optional)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: ${NAMESPACE}
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

---

## PriorityClass Templates

### Priority Classes

```yaml
# Critical (highest priority)
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: critical
value: 1000000
globalDefault: false
preemptionPolicy: PreemptLowerPriority
description: "Critical system components"
---
# High priority
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high
value: 100000
globalDefault: false
preemptionPolicy: PreemptLowerPriority
description: "Important production workloads"
---
# Default priority
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: default
value: 10000
globalDefault: true
preemptionPolicy: PreemptLowerPriority
description: "Default priority for standard workloads"
---
# Low priority (batch jobs)
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low
value: 1000
globalDefault: false
preemptionPolicy: Never
description: "Low priority batch jobs"
```

---

## VPA Templates

### VPA Recommendation Mode

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ${APP_NAME}-vpa
  namespace: ${NAMESPACE}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ${APP_NAME}
  updatePolicy:
    updateMode: "Off"  # Recommendation only
  resourcePolicy:
    containerPolicies:
    - containerName: '*'
      minAllowed:
        cpu: 50m
        memory: 64Mi
      maxAllowed:
        cpu: "4"
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
```

### VPA Auto Mode

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ${APP_NAME}-vpa
  namespace: ${NAMESPACE}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ${APP_NAME}
  updatePolicy:
    updateMode: "Auto"  # Automatic updates
  resourcePolicy:
    containerPolicies:
    - containerName: '*'
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: "2"
        memory: 4Gi
```

---

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `${NAMESPACE}` | Kubernetes namespace | `production` |
| `${APP_NAME}` | Application name | `web-api` |
| `${IMAGE}` | Container image | `myapp` |
| `${TAG}` | Image tag | `v1.0.0` |
| `${PORT}` | Container port | `8080` |
| `${REPLICAS}` | Replica count | `3` |
| `${CPU_REQUEST}` | CPU request | `250m` |
| `${CPU_LIMIT}` | CPU limit | `500m` |
| `${MEMORY_REQUEST}` | Memory request | `256Mi` |
| `${MEMORY_LIMIT}` | Memory limit | `512Mi` |
| `${CPU}` | CPU (Guaranteed) | `500m` |
| `${MEMORY}` | Memory (Guaranteed) | `512Mi` |
| `${TOTAL_CPU_REQUESTS}` | Namespace CPU requests | `"10"` |
| `${TOTAL_MEMORY_REQUESTS}` | Namespace memory requests | `20Gi` |
| `${TOTAL_CPU_LIMITS}` | Namespace CPU limits | `"20"` |
| `${TOTAL_MEMORY_LIMITS}` | Namespace memory limits | `40Gi` |
| `${MAX_PODS}` | Max pods in namespace | `"50"` |
| `${MAX_SERVICES}` | Max services | `"10"` |
| `${MAX_PVCS}` | Max PVCs | `"10"` |
| `${TOTAL_STORAGE}` | Total storage | `100Gi` |
| `${MAX_STORAGE}` | Max PVC size | `50Gi` |
| `${TEAM}` | Team name | `backend` |
| `${ENV}` | Environment | `production` |

---

*k8s-resources/templates.md | Copy-Paste Templates*
