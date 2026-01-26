# Kubernetes Deployment Examples

**Production Patterns: Deployments, StatefulSets, Rolling Updates, Canary (2025-2026)**

---

## Deployment Examples

### Production Web API Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: production
  labels:
    app.kubernetes.io/name: api
    app.kubernetes.io/version: "1.2.3"
    app.kubernetes.io/component: backend
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0      # Zero-downtime: no pods down during update
      maxSurge: 1            # One extra pod during update
  selector:
    matchLabels:
      app.kubernetes.io/name: api
  template:
    metadata:
      labels:
        app.kubernetes.io/name: api
        app.kubernetes.io/version: "1.2.3"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: api
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
        - name: api
          image: registry.example.com/api:1.2.3@sha256:abc123...
          imagePullPolicy: IfNotPresent

          ports:
            - name: http
              containerPort: 8000
              protocol: TCP

          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url

          envFrom:
            - configMapRef:
                name: api-config

          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"

          # Startup probe: Allow up to 5 minutes for slow starts
          startupProbe:
            httpGet:
              path: /health/live
              port: http
            periodSeconds: 5
            failureThreshold: 60    # 60 * 5s = 5 minutes

          # Liveness probe: Restart if unhealthy
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          # Readiness probe: Remove from service if not ready
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/cache

      volumes:
        - name: tmp
          emptyDir:
            sizeLimit: 100Mi
        - name: cache
          emptyDir:
            sizeLimit: 500Mi

      # Spread pods across nodes
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: api
                topologyKey: kubernetes.io/hostname

      # Spread across availability zones
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: api

      # Graceful termination
      terminationGracePeriodSeconds: 30
```

### Worker Deployment with Queue Processing

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker
  namespace: production
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: worker
  template:
    metadata:
      labels:
        app.kubernetes.io/name: worker
    spec:
      serviceAccountName: worker

      containers:
        - name: worker
          image: registry.example.com/worker:1.0.0
          command: ["celery", "-A", "app", "worker", "-l", "info"]

          env:
            - name: CELERY_BROKER_URL
              valueFrom:
                secretKeyRef:
                  name: worker-secrets
                  key: broker-url

          resources:
            requests:
              cpu: "200m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"

          # Workers don't serve HTTP, use exec probe
          livenessProbe:
            exec:
              command:
                - celery
                - -A
                - app
                - inspect
                - ping
                - -d
                - celery@$(POD_NAME)
            periodSeconds: 30
            timeoutSeconds: 10
            failureThreshold: 3

          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            allowPrivilegeEscalation: false

      # Allow graceful task completion
      terminationGracePeriodSeconds: 300
```

---

## StatefulSet Examples

### PostgreSQL Primary-Replica

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: database
spec:
  clusterIP: None          # Headless service for StatefulSet
  selector:
    app.kubernetes.io/name: postgres
  ports:
    - name: postgres
      port: 5432
      targetPort: postgres
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: database
spec:
  serviceName: postgres    # Must match headless service name
  replicas: 3
  podManagementPolicy: OrderedReady    # Sequential startup (0, 1, 2)
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0         # Update all pods (set > 0 for staged rollout)
  selector:
    matchLabels:
      app.kubernetes.io/name: postgres
  template:
    metadata:
      labels:
        app.kubernetes.io/name: postgres
    spec:
      serviceAccountName: postgres
      securityContext:
        fsGroup: 999

      initContainers:
        - name: init-permissions
          image: busybox:1.36
          command: ['sh', '-c', 'chown -R 999:999 /var/lib/postgresql/data']
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data

      containers:
        - name: postgres
          image: postgres:16-alpine
          ports:
            - name: postgres
              containerPort: 5432

          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name

          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "2"
              memory: "4Gi"

          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - $(POSTGRES_USER)
            periodSeconds: 10
            timeoutSeconds: 5

          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - $(POSTGRES_USER)
            periodSeconds: 30
            timeoutSeconds: 5
            failureThreshold: 3

          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data

      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app.kubernetes.io/name: postgres
              topologyKey: kubernetes.io/hostname

      terminationGracePeriodSeconds: 60

  # PVC per pod (postgres-0, postgres-1, postgres-2)
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 100Gi
```

### Redis Cluster StatefulSet

```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: cache
spec:
  clusterIP: None
  selector:
    app.kubernetes.io/name: redis
  ports:
    - name: redis
      port: 6379
    - name: cluster-bus
      port: 16379
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: cache
spec:
  serviceName: redis
  replicas: 6    # 3 masters + 3 replicas
  podManagementPolicy: Parallel    # All pods can start simultaneously
  selector:
    matchLabels:
      app.kubernetes.io/name: redis
  template:
    metadata:
      labels:
        app.kubernetes.io/name: redis
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          command:
            - redis-server
            - /conf/redis.conf
            - --cluster-enabled
            - "yes"
            - --cluster-config-file
            - /data/nodes.conf

          ports:
            - name: redis
              containerPort: 6379
            - name: cluster-bus
              containerPort: 16379

          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"

          readinessProbe:
            exec:
              command: ["redis-cli", "ping"]
            periodSeconds: 5

          livenessProbe:
            exec:
              command: ["redis-cli", "ping"]
            periodSeconds: 10

          volumeMounts:
            - name: data
              mountPath: /data
            - name: config
              mountPath: /conf

      volumes:
        - name: config
          configMap:
            name: redis-config

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: redis
                topologyKey: kubernetes.io/hostname

  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: standard
        resources:
          requests:
            storage: 10Gi
```

---

## Rolling Update Examples

### Zero-Downtime Rolling Update

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0    # Never reduce below desired replicas
      maxSurge: 1          # Add one pod at a time
  minReadySeconds: 10      # Wait 10s before considering pod ready
  # ... rest of spec
```

**Update sequence:**

```
Initial:  [v1-pod1] [v1-pod2] [v1-pod3]
Step 1:   [v1-pod1] [v1-pod2] [v1-pod3] [v2-pod4]  <- Surge: +1
Step 2:   [v1-pod1] [v1-pod2] [v2-pod4]             <- v1-pod3 terminated
Step 3:   [v1-pod1] [v1-pod2] [v2-pod4] [v2-pod5]  <- New pod
Step 4:   [v1-pod1] [v2-pod4] [v2-pod5]             <- v1-pod2 terminated
Step 5:   [v1-pod1] [v2-pod4] [v2-pod5] [v2-pod6]  <- New pod
Step 6:   [v2-pod4] [v2-pod5] [v2-pod6]             <- Complete
```

### Fast Rolling Update

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 2    # Allow 2 pods down
      maxSurge: 3          # Allow 3 extra pods
  minReadySeconds: 5
  # ... rest of spec
```

### Rolling Update Commands

```bash
# Trigger update by changing image
kubectl set image deployment/web web=registry.example.com/web:2.0.0

# Or apply updated manifest
kubectl apply -f deployment.yaml

# Watch rollout progress
kubectl rollout status deployment/web

# Pause rollout (for investigation)
kubectl rollout pause deployment/web

# Resume rollout
kubectl rollout resume deployment/web

# View rollout history
kubectl rollout history deployment/web

# Rollback to previous version
kubectl rollout undo deployment/web

# Rollback to specific revision
kubectl rollout undo deployment/web --to-revision=3
```

---

## Canary Deployment Examples

### Manual Canary with Two Deployments

```yaml
# Stable deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-stable
  labels:
    app: api
    version: stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: api
      version: stable
  template:
    metadata:
      labels:
        app: api
        version: stable
    spec:
      containers:
        - name: api
          image: registry.example.com/api:1.0.0
---
# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-canary
  labels:
    app: api
    version: canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
      version: canary
  template:
    metadata:
      labels:
        app: api
        version: canary
    spec:
      containers:
        - name: api
          image: registry.example.com/api:2.0.0
---
# Service routes to both (weighted by replica count)
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api    # Matches both stable and canary
  ports:
    - port: 80
      targetPort: 8000
```

### Canary with Nginx Ingress (Annotations)

```yaml
# Stable Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-stable
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-stable
                port:
                  number: 80
---
# Canary Ingress with weight
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-canary
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"    # 10% traffic
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-canary
                port:
                  number: 80
```

**Progression: Update canary-weight annotation**

```bash
# Increase to 30%
kubectl annotate ingress api-canary \
  nginx.ingress.kubernetes.io/canary-weight="30" --overwrite

# Increase to 50%
kubectl annotate ingress api-canary \
  nginx.ingress.kubernetes.io/canary-weight="50" --overwrite

# Promote: Delete canary ingress, update stable deployment
kubectl delete ingress api-canary
kubectl set image deployment/api-stable api=registry.example.com/api:2.0.0
```

### Canary with Header-Based Routing

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-canary-header
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-header: "X-Canary"
    nginx.ingress.kubernetes.io/canary-by-header-value: "true"
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-canary
                port:
                  number: 80
```

**Testing canary:**

```bash
# Regular request goes to stable
curl https://api.example.com/

# Request with header goes to canary
curl -H "X-Canary: true" https://api.example.com/
```

---

## Argo Rollouts Examples (2025-2026)

### Canary with Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api
spec:
  replicas: 5
  revisionHistoryLimit: 3
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
          image: registry.example.com/api:1.0.0
          ports:
            - containerPort: 8000

  strategy:
    canary:
      # Canary service for testing
      canaryService: api-canary
      stableService: api-stable

      # Traffic splitting via Ingress
      trafficRouting:
        nginx:
          stableIngress: api-stable
          annotationPrefix: nginx.ingress.kubernetes.io

      steps:
        # 10% for 5 minutes
        - setWeight: 10
        - pause: {duration: 5m}

        # Analysis at 10%
        - analysis:
            templates:
              - templateName: success-rate
            args:
              - name: service-name
                value: api-canary

        # 30% for 5 minutes
        - setWeight: 30
        - pause: {duration: 5m}

        # 50% for 10 minutes
        - setWeight: 50
        - pause: {duration: 10m}

        # 80% for 10 minutes
        - setWeight: 80
        - pause: {duration: 10m}

        # Full promotion
        - setWeight: 100
---
# Analysis Template for automated validation
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      count: 5
      successCondition: result[0] >= 0.99
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{
              service="{{args.service-name}}",
              status=~"2.."
            }[5m])) /
            sum(rate(http_requests_total{
              service="{{args.service-name}}"
            }[5m]))
```

### Blue-Green with Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
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
          image: registry.example.com/api:1.0.0
          ports:
            - containerPort: 8000

  strategy:
    blueGreen:
      activeService: api-active       # Production traffic
      previewService: api-preview     # Preview/test traffic
      autoPromotionEnabled: false     # Manual promotion required

      # Preview for testing before promotion
      previewReplicaCount: 1

      # Scale down old version after promotion
      scaleDownDelaySeconds: 30

      # Optional: auto promote after delay
      # autoPromotionSeconds: 600
---
apiVersion: v1
kind: Service
metadata:
  name: api-active
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: api-preview
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 8000
```

**Argo Rollouts Commands:**

```bash
# Install Argo Rollouts
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# Watch rollout
kubectl argo rollouts get rollout api -w

# Promote canary
kubectl argo rollouts promote api

# Abort rollout
kubectl argo rollouts abort api

# Retry aborted rollout
kubectl argo rollouts retry rollout api

# Dashboard
kubectl argo rollouts dashboard
```

---

## Supporting Resources Examples

### PodDisruptionBudget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  minAvailable: 2    # At least 2 pods must remain
  # OR
  # maxUnavailable: 1  # At most 1 pod can be unavailable
  selector:
    matchLabels:
      app.kubernetes.io/name: api
```

### HorizontalPodAutoscaler (2025-2026)

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
  minReplicas: 3
  maxReplicas: 20
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

  # Advanced behavior (2025-2026)
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300    # Wait 5 min before scale down
      policies:
        - type: Percent
          value: 10                       # Max 10% reduction
          periodSeconds: 60
        - type: Pods
          value: 2                        # Max 2 pods
          periodSeconds: 60
      selectPolicy: Min                   # Use most conservative

    scaleUp:
      stabilizationWindowSeconds: 0       # Scale up immediately
      policies:
        - type: Percent
          value: 100                      # Double pods
          periodSeconds: 15
        - type: Pods
          value: 4                        # Or add 4 pods
          periodSeconds: 15
      selectPolicy: Max                   # Use most aggressive
```

### NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: api
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Allow from ingress controller
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8000

    # Allow from other api pods (for health checks)
    - from:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: api
      ports:
        - protocol: TCP
          port: 8000

  egress:
    # Allow to database
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: postgres
      ports:
        - protocol: TCP
          port: 5432

    # Allow to Redis
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: redis
      ports:
        - protocol: TCP
          port: 6379

    # Allow DNS
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### Service with Session Affinity

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app.kubernetes.io/name: api
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
  ports:
    - port: 80
      targetPort: 8000
```

---

## Init Container Patterns

### Wait for Dependencies

```yaml
spec:
  initContainers:
    - name: wait-for-db
      image: busybox:1.36
      command:
        - sh
        - -c
        - |
          until nc -z postgres 5432; do
            echo "Waiting for database..."
            sleep 2
          done
          echo "Database is ready!"

    - name: wait-for-redis
      image: busybox:1.36
      command:
        - sh
        - -c
        - |
          until nc -z redis 6379; do
            echo "Waiting for Redis..."
            sleep 2
          done

  containers:
    - name: api
      # ...
```

### Database Migrations

```yaml
spec:
  initContainers:
    - name: migrate
      image: registry.example.com/api:1.0.0
      command: ["python", "manage.py", "migrate", "--noinput"]
      envFrom:
        - secretRef:
            name: api-secrets
        - configMapRef:
            name: api-config

  containers:
    - name: api
      # ...
```

---

*Kubernetes Deployment Examples | faion-infrastructure-engineer*
