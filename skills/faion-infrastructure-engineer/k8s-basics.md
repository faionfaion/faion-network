---
name: faion-k8s-basics
user-invocable: false
description: ""
---

# Kubernetes Basics

**Core kubectl operations, deployments, services, and fundamental concepts**

---

## Quick Reference

**Supported versions:**
- Kubernetes: 1.28+ (prefer 1.30+)
- kubectl: match cluster version
- Helm: 3.12+
- Kustomize: built into kubectl 1.14+

---

## kubectl Operations

### Resource Management

```bash
# Get resources
kubectl get pods                          # List pods
kubectl get pods -o wide                  # With node info
kubectl get pods -A                       # All namespaces
kubectl get pods -l app=myapp             # By label
kubectl get pods --field-selector=status.phase=Running

# Describe (detailed info)
kubectl describe pod <pod-name>
kubectl describe deployment <deploy-name>
kubectl describe service <svc-name>

# Create/Apply
kubectl apply -f manifest.yaml            # Apply config
kubectl apply -f ./manifests/             # Apply directory
kubectl apply -k ./kustomize/             # Apply with kustomize

# Delete
kubectl delete -f manifest.yaml
kubectl delete pod <pod-name>
kubectl delete pod <pod-name> --grace-period=0 --force  # Force delete
```

### Common Resource Types

| Resource | Short | Description |
|----------|-------|-------------|
| pods | po | Running containers |
| deployments | deploy | Manages ReplicaSets |
| services | svc | Network endpoints |
| configmaps | cm | Configuration data |
| secrets | - | Sensitive data |
| ingress | ing | HTTP routing |
| persistentvolumeclaims | pvc | Storage claims |
| namespaces | ns | Cluster partitions |
| nodes | no | Cluster nodes |
| replicasets | rs | Pod replicas |
| daemonsets | ds | Node-level pods |
| statefulsets | sts | Stateful apps |
| jobs | - | One-time tasks |
| cronjobs | cj | Scheduled tasks |

### Namespace Operations

```bash
# Namespace context
kubectl config set-context --current --namespace=<ns>
kubectl get pods -n <namespace>

# Create namespace
kubectl create namespace <name>

# Resource quotas
kubectl get resourcequotas -n <namespace>
kubectl describe resourcequota -n <namespace>
```

---

## Deployments

### Creating Deployments

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: ENV
          value: "production"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: password
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment myapp --replicas=5

# Autoscaling (HPA)
kubectl autoscale deployment myapp --min=2 --max=10 --cpu-percent=80

# Check HPA status
kubectl get hpa
kubectl describe hpa myapp
```

### Rollouts

```bash
# Update image
kubectl set image deployment/myapp myapp=myapp:2.0.0

# Rollout status
kubectl rollout status deployment/myapp

# Rollout history
kubectl rollout history deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2

# Pause/Resume
kubectl rollout pause deployment/myapp
kubectl rollout resume deployment/myapp
```

### Update Strategies

```yaml
# Rolling Update (default)
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%

# Recreate (all at once)
spec:
  strategy:
    type: Recreate
```

---

## Services

### Service Types

```yaml
# ClusterIP (internal only)
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080

# NodePort (external via node port)
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080

# LoadBalancer (cloud provider LB)
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
```

### Service Discovery

```bash
# DNS format: <service>.<namespace>.svc.cluster.local
# Example: myapp-service.default.svc.cluster.local

# Get endpoints
kubectl get endpoints myapp-service

# Test service
kubectl run curl --image=curlimages/curl -it --rm -- curl http://myapp-service:80
```

---

## ConfigMaps and Secrets

### ConfigMaps

```bash
# Create from literal
kubectl create configmap myconfig --from-literal=key1=value1 --from-literal=key2=value2

# Create from file
kubectl create configmap myconfig --from-file=config.properties

# Create from env file
kubectl create configmap myconfig --from-env-file=config.env
```

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myconfig
data:
  DATABASE_HOST: "postgres.default.svc.cluster.local"
  LOG_LEVEL: "info"
  config.json: |
    {
      "key": "value",
      "nested": {
        "key": "value"
      }
    }
```

### Secrets

```bash
# Create generic secret
kubectl create secret generic mysecret --from-literal=password=s3cr3t

# Create TLS secret
kubectl create secret tls mytls --cert=tls.crt --key=tls.key

# Create docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=user \
  --docker-password=password
```

```yaml
# secret.yaml (values must be base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  password: cGFzc3dvcmQ=    # base64 of "password"
  api-key: YXBpLWtleQ==    # base64 of "api-key"
```

### Using ConfigMaps/Secrets in Pods

```yaml
spec:
  containers:
  - name: myapp
    # As environment variables
    env:
    - name: DATABASE_HOST
      valueFrom:
        configMapKeyRef:
          name: myconfig
          key: DATABASE_HOST
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: mysecret
          key: password
    # All keys as env vars
    envFrom:
    - configMapRef:
        name: myconfig
    - secretRef:
        name: mysecret
    # As volume mount
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: myconfig
```

---

## Debugging

### Pod Debugging

```bash
# Get pod logs
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container>    # Specific container
kubectl logs <pod-name> --previous        # Previous instance
kubectl logs <pod-name> -f                # Follow
kubectl logs <pod-name> --tail=100        # Last 100 lines

# Exec into pod
kubectl exec -it <pod-name> -- /bin/sh
kubectl exec -it <pod-name> -c <container> -- /bin/bash

# Copy files
kubectl cp <pod-name>:/path/to/file ./local-file
kubectl cp ./local-file <pod-name>:/path/to/file

# Port forward
kubectl port-forward pod/<pod-name> 8080:80
kubectl port-forward svc/<svc-name> 8080:80
```

### Debugging Pods

```bash
# Pod not starting
kubectl describe pod <pod-name>           # Check Events section
kubectl get pod <pod-name> -o yaml        # Full spec

# Common issues
# - ImagePullBackOff: Check image name, registry auth
# - CrashLoopBackOff: Check logs, resource limits
# - Pending: Check node resources, selectors
# - ContainerCreating: Check PVC, configmaps, secrets

# Debug with ephemeral container
kubectl debug <pod-name> -it --image=busybox

# Debug node
kubectl debug node/<node-name> -it --image=ubuntu
```

### Events and Status

```bash
# Cluster events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -A --field-selector type=Warning

# Resource status
kubectl get pods -o custom-columns=\
NAME:.metadata.name,\
STATUS:.status.phase,\
RESTARTS:.status.containerStatuses[0].restartCount

# API resources
kubectl api-resources
kubectl explain deployment.spec.strategy
```

### Network Debugging

```bash
# Test DNS
kubectl run dnsutils --image=tutum/dnsutils -it --rm -- nslookup kubernetes

# Test connectivity
kubectl run curl --image=curlimages/curl -it --rm -- curl -v http://service:port

# Check endpoints
kubectl get endpoints <service-name>

# Check network policies
kubectl get networkpolicies
kubectl describe networkpolicy <name>
```

### Resource Troubleshooting

```bash
# Node resources
kubectl top nodes
kubectl describe node <node-name>

# Pod resources
kubectl top pods
kubectl top pods --containers

# Resource quotas
kubectl describe resourcequota -n <namespace>
kubectl describe limitrange -n <namespace>
```

---

## Best Practices

### Resource Requests/Limits

```yaml
resources:
  requests:           # Guaranteed resources
    memory: "64Mi"
    cpu: "250m"
  limits:             # Maximum allowed
    memory: "128Mi"
    cpu: "500m"
```

### Health Checks

```yaml
# Liveness: Restart container if fails
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

# Readiness: Remove from service if fails
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5

# Startup: Wait for slow starting containers
startupProbe:
  httpGet:
    path: /health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

### Security Context

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
```

### Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  # or: maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

---

## References

- [Kubernetes Docs](https://kubernetes.io/docs/home/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

## Sources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/setup/best-practices/)
- [Kubernetes Patterns](https://www.oreilly.com/library/view/kubernetes-patterns/9781492050278/)
