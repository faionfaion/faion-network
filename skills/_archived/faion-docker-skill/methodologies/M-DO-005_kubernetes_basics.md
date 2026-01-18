# M-DO-005: Kubernetes Basics

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #kubernetes, #k8s, #containers, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Docker Compose doesn't scale for production. Managing containers across multiple hosts, handling failures, and scaling requires more sophisticated orchestration.

## Promise

After this methodology, you will deploy and manage applications on Kubernetes. Your apps will be scalable, self-healing, and production-ready.

## Overview

Kubernetes (K8s) orchestrates containerized applications across clusters. It handles deployment, scaling, networking, and self-healing automatically.

---

## Framework

### Step 1: Kubernetes Concepts

```
Cluster
├── Nodes (machines)
│   ├── Control Plane (master)
│   └── Worker Nodes
└── Resources
    ├── Pods (smallest unit)
    ├── Deployments (manage pods)
    ├── Services (networking)
    ├── ConfigMaps (configuration)
    ├── Secrets (sensitive data)
    └── Ingress (external access)
```

### Step 2: kubectl Basics

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/

# Configure context
kubectl config get-contexts
kubectl config use-context my-cluster

# Get resources
kubectl get pods
kubectl get pods -A                    # All namespaces
kubectl get pods -o wide               # More details
kubectl get deploy,svc,pods            # Multiple resources

# Describe resources
kubectl describe pod my-pod
kubectl describe deploy my-deployment

# Logs
kubectl logs my-pod
kubectl logs -f my-pod                 # Follow
kubectl logs my-pod -c container-name  # Specific container

# Execute commands
kubectl exec -it my-pod -- sh
kubectl exec my-pod -- cat /etc/hosts

# Apply and delete
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
kubectl delete pod my-pod
```

### Step 3: Pod Definition

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
    environment: development
spec:
  containers:
    - name: app
      image: myapp:1.0.0
      ports:
        - containerPort: 3000
      env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
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
          port: 3000
        initialDelaySeconds: 10
        periodSeconds: 10
      readinessProbe:
        httpGet:
          path: /ready
          port: 3000
        initialDelaySeconds: 5
        periodSeconds: 5
```

### Step 4: Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: app
          image: myapp:1.0.0
          ports:
            - containerPort: 3000
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secrets
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
              port: 3000
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### Step 5: Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP  # Internal only

---
# NodePort (development)
apiVersion: v1
kind: Service
metadata:
  name: my-app-nodeport
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 3000
      nodePort: 30080
  type: NodePort

---
# LoadBalancer (cloud)
apiVersion: v1
kind: Service
metadata:
  name: my-app-lb
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 3000
  type: LoadBalancer
```

### Step 6: ConfigMap and Secrets

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  API_URL: "https://api.example.com"

---
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgres://user:pass@db:5432/mydb"
  API_KEY: "secret-api-key"

# Or base64 encoded
data:
  DATABASE_URL: cG9zdGdyZXM6Ly91c2VyOnBhc3NAZGI6NTQzMi9teWRi
```

---

## Templates

### Complete Application

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-app

---
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: my-app
data:
  NODE_ENV: "production"

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: my-app
type: Opaque
stringData:
  DATABASE_URL: "postgres://user:pass@db:5432/mydb"

---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: app
          image: myapp:1.0.0
          ports:
            - containerPort: 3000
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secrets
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
              port: 3000
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
  namespace: my-app
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 3000

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app
  namespace: my-app
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app
                port:
                  number: 80
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

---

## Examples

### Persistent Volume

```yaml
# persistentvolumeclaim.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard

---
# Use in deployment
spec:
  containers:
    - name: app
      volumeMounts:
        - name: data
          mountPath: /app/data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data-pvc
```

### CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: backup-tool:latest
              command: ["/bin/sh", "-c", "./backup.sh"]
          restartPolicy: OnFailure
```

---

## Common Mistakes

1. **No resource limits** - Pods consume all node resources
2. **Missing health checks** - Bad pods receive traffic
3. **Secrets in ConfigMaps** - Use Secrets for sensitive data
4. **No namespaces** - Everything in default namespace
5. **Latest tag** - Use specific image versions

---

## Checklist

- [ ] Namespace per application
- [ ] Resource requests and limits
- [ ] Liveness and readiness probes
- [ ] ConfigMaps for configuration
- [ ] Secrets for sensitive data
- [ ] Rolling update strategy
- [ ] Horizontal Pod Autoscaler
- [ ] Ingress for external access

---

## Next Steps

- M-DO-006: Helm Charts
- M-DO-009: Terraform Basics
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-005 v1.0*
