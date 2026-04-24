# Kubernetes Examples

Practical examples for common Kubernetes operations and patterns.

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

### Production Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
  template:
    metadata:
      labels:
        app: myapp
        version: v1.0.0
    spec:
      serviceAccountName: myapp-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: myapp
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
          name: http
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        securityContext:
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /health
            port: http
          failureThreshold: 30
          periodSeconds: 10
        env:
        - name: ENV
          value: "production"
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: password
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: config
          mountPath: /etc/config
          readOnly: true
      volumes:
      - name: tmp
        emptyDir: {}
      - name: config
        configMap:
          name: myapp-config
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: myapp
              topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app: myapp
```

### Rollout Operations

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

# Pause/Resume (for batch updates)
kubectl rollout pause deployment/myapp
kubectl rollout resume deployment/myapp
```

---

## Services

### ClusterIP (Internal)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8080
```

### LoadBalancer (External)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
  annotations:
    # AWS-specific
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: https
    port: 443
    targetPort: 8443
```

### Headless Service (StatefulSet)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app: myapp
  ports:
  - port: 8080
```

---

## Autoscaling

### Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

### Vertical Pod Autoscaler (VPA)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto"  # Off, Initial, Auto
  resourcePolicy:
    containerPolicies:
    - containerName: myapp
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2
        memory: 4Gi
      controlledResources: ["cpu", "memory"]
```

### KEDA ScaledObject

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: myapp-keda
spec:
  scaleTargetRef:
    name: myapp
  pollingInterval: 30
  cooldownPeriod: 300
  minReplicaCount: 1
  maxReplicaCount: 20
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: http_requests_total
      query: sum(rate(http_requests_total{app="myapp"}[2m]))
      threshold: "100"
```

---

## Security

### NetworkPolicy (Default Deny)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### NetworkPolicy (Allow Specific)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-netpol
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: production
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

### PodDisruptionBudget

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

### ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
    services: "10"
    secrets: "20"
    configmaps: "20"
    persistentvolumeclaims: "10"
```

### LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: production-limits
  namespace: production
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
      cpu: 2
      memory: 4Gi
  - type: Pod
    max:
      cpu: 4
      memory: 8Gi
```

---

## ConfigMaps and Secrets

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
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

### External Secret (with External Secrets Operator)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: myapp-secrets
  data:
  - secretKey: password
    remoteRef:
      key: secret/myapp
      property: password
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

# Debug with ephemeral container
kubectl debug <pod-name> -it --image=busybox

# Debug node
kubectl debug node/<node-name> -it --image=ubuntu

# Port forward
kubectl port-forward pod/<pod-name> 8080:80
kubectl port-forward svc/<svc-name> 8080:80

# Copy files
kubectl cp <pod-name>:/path/to/file ./local-file
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

# Events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -A --field-selector type=Warning

# API resources
kubectl api-resources
kubectl explain deployment.spec.strategy
```

---

## Sources

- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [8 Kubernetes Deployment Strategies](https://www.groundcover.com/blog/kubernetes-deployment-strategies)
- [kubectl rollout Best Practices 2025](https://scaleops.com/blog/kubectl-rollout-7-best-practices-for-production-2025/)
