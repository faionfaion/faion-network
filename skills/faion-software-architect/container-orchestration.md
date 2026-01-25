# Container Orchestration

Kubernetes architecture patterns and best practices.

## Why Kubernetes?

- **Declarative** - Describe desired state
- **Self-healing** - Auto-restart failed containers
- **Scaling** - Horizontal pod autoscaling
- **Load balancing** - Service discovery built-in
- **Rolling updates** - Zero-downtime deployments

## Core Concepts

```
┌─────────────────────────────────────────────────┐
│                   CLUSTER                        │
│  ┌─────────────────────────────────────────┐    │
│  │              NAMESPACE                   │    │
│  │  ┌─────────────────────────────────┐    │    │
│  │  │          DEPLOYMENT             │    │    │
│  │  │  ┌───────┐  ┌───────┐          │    │    │
│  │  │  │ Pod   │  │ Pod   │  (replicas)    │    │
│  │  │  │┌─────┐│  │┌─────┐│          │    │    │
│  │  │  ││Cont.││  ││Cont.││          │    │    │
│  │  │  │└─────┘│  │└─────┘│          │    │    │
│  │  │  └───────┘  └───────┘          │    │    │
│  │  └─────────────────────────────────┘    │    │
│  │                 │                        │    │
│  │                 ▼                        │    │
│  │  ┌─────────────────────────────────┐    │    │
│  │  │           SERVICE               │    │    │
│  │  │    (load balances to pods)      │    │    │
│  │  └─────────────────────────────────┘    │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## Resource Types

| Resource | Purpose |
|----------|---------|
| Pod | Smallest unit, one or more containers |
| Deployment | Manages ReplicaSets, rolling updates |
| Service | Stable endpoint for pods |
| Ingress | HTTP routing, SSL termination |
| ConfigMap | Configuration data |
| Secret | Sensitive data (encrypted) |
| PersistentVolumeClaim | Storage request |

## Deployment Patterns

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP  # or LoadBalancer, NodePort
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api
            port:
              number: 80
```

## Scaling

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Configuration Management

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "postgres.default.svc"
  LOG_LEVEL: "info"
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DATABASE_PASSWORD: cGFzc3dvcmQ=  # base64 encoded
```

### Using in Deployment

```yaml
spec:
  containers:
  - name: api
    envFrom:
    - configMapRef:
        name: app-config
    - secretRef:
        name: app-secrets
```

## Deployment Strategies

### Rolling Update (default)
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Extra pods during update
      maxUnavailable: 0  # Always maintain capacity
```

### Blue-Green
Deploy new version alongside old, switch traffic.

### Canary
Route small percentage to new version, gradually increase.

## Namespace Strategy

```
namespaces/
├── production
├── staging
├── development
└── monitoring
```

**Best practices:**
- Separate environments
- Resource quotas per namespace
- Network policies between namespaces

## Health Checks

```yaml
livenessProbe:    # Restart if fails
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5

readinessProbe:   # Remove from service if fails
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Resource Management

```yaml
resources:
  requests:      # Guaranteed resources
    memory: "128Mi"
    cpu: "100m"
  limits:        # Maximum resources
    memory: "256Mi"
    cpu: "500m"
```

**Best practice:** Always set both requests and limits.

## Related

- [cloud-architecture.md](cloud-architecture.md) - Cloud context
- [microservices-architecture.md](microservices-architecture.md) - Service design
