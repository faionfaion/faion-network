# Kubernetes Deployment Templates

**Ready-to-Use YAML Templates for Production Workloads (2025-2026)**

---

## Deployment Templates

### Production API Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/version: "${VERSION}"
    app.kubernetes.io/component: backend
    app.kubernetes.io/managed-by: kubectl
spec:
  replicas: ${REPLICAS:-3}
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${APP_NAME}
        app.kubernetes.io/version: "${VERSION}"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "${PORT:-8000}"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: ${APP_NAME}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
        - name: ${APP_NAME}
          image: ${REGISTRY}/${APP_NAME}:${VERSION}
          imagePullPolicy: IfNotPresent

          ports:
            - name: http
              containerPort: ${PORT:-8000}
              protocol: TCP

          envFrom:
            - configMapRef:
                name: ${APP_NAME}-config
            - secretRef:
                name: ${APP_NAME}-secrets

          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP

          resources:
            requests:
              cpu: "${CPU_REQUEST:-100m}"
              memory: "${MEMORY_REQUEST:-256Mi}"
            limits:
              cpu: "${CPU_LIMIT:-500m}"
              memory: "${MEMORY_LIMIT:-512Mi}"

          startupProbe:
            httpGet:
              path: /health/live
              port: http
            periodSeconds: 5
            failureThreshold: 60

          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

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

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: ${APP_NAME}
                topologyKey: kubernetes.io/hostname

      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: ${APP_NAME}

      terminationGracePeriodSeconds: 30
```

### Frontend/Next.js Deployment

```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}-frontend
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS:-2}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}-frontend
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${APP_NAME}-frontend
    spec:
      serviceAccountName: ${APP_NAME}-frontend
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001

      containers:
        - name: frontend
          image: ${REGISTRY}/${APP_NAME}-frontend:${VERSION}
          ports:
            - name: http
              containerPort: 3000

          env:
            - name: NODE_ENV
              value: production
            - name: NEXT_TELEMETRY_DISABLED
              value: "1"
            - name: API_URL
              value: "http://${APP_NAME}-api:80"

          envFrom:
            - configMapRef:
                name: ${APP_NAME}-frontend-config

          resources:
            requests:
              cpu: "50m"
              memory: "128Mi"
            limits:
              cpu: "200m"
              memory: "256Mi"

          startupProbe:
            httpGet:
              path: /api/health
              port: http
            periodSeconds: 5
            failureThreshold: 30

          livenessProbe:
            httpGet:
              path: /api/health
              port: http
            periodSeconds: 15
            timeoutSeconds: 5

          readinessProbe:
            httpGet:
              path: /api/health
              port: http
            periodSeconds: 5
            timeoutSeconds: 3

          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: nextjs-cache
              mountPath: /app/.next/cache

      volumes:
        - name: tmp
          emptyDir: {}
        - name: nextjs-cache
          emptyDir:
            sizeLimit: 1Gi

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: ${APP_NAME}-frontend
                topologyKey: kubernetes.io/hostname
```

### Worker/Background Job Deployment

```yaml
# worker-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}-worker
  namespace: ${NAMESPACE}
spec:
  replicas: ${WORKER_REPLICAS:-3}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}-worker
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${APP_NAME}-worker
    spec:
      serviceAccountName: ${APP_NAME}-worker
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000

      containers:
        - name: worker
          image: ${REGISTRY}/${APP_NAME}:${VERSION}
          command: ["celery", "-A", "app", "worker", "-l", "info", "-c", "4"]

          envFrom:
            - configMapRef:
                name: ${APP_NAME}-config
            - secretRef:
                name: ${APP_NAME}-secrets

          resources:
            requests:
              cpu: "200m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"

          livenessProbe:
            exec:
              command:
                - sh
                - -c
                - celery -A app inspect ping -d celery@$HOSTNAME
            periodSeconds: 30
            timeoutSeconds: 10
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

      volumes:
        - name: tmp
          emptyDir: {}

      # Workers can tolerate longer termination for task completion
      terminationGracePeriodSeconds: 300
```

---

## StatefulSet Templates

### Database StatefulSet (Generic)

```yaml
# statefulset-db.yaml
apiVersion: v1
kind: Service
metadata:
  name: ${DB_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${DB_NAME}
spec:
  clusterIP: None
  selector:
    app.kubernetes.io/name: ${DB_NAME}
  ports:
    - name: db
      port: ${DB_PORT}
      targetPort: db
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ${DB_NAME}
  namespace: ${NAMESPACE}
spec:
  serviceName: ${DB_NAME}
  replicas: ${REPLICAS:-1}
  podManagementPolicy: OrderedReady
  updateStrategy:
    type: RollingUpdate
  selector:
    matchLabels:
      app.kubernetes.io/name: ${DB_NAME}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${DB_NAME}
    spec:
      serviceAccountName: ${DB_NAME}
      securityContext:
        fsGroup: 999

      containers:
        - name: ${DB_NAME}
          image: ${DB_IMAGE}
          ports:
            - name: db
              containerPort: ${DB_PORT}

          envFrom:
            - secretRef:
                name: ${DB_NAME}-credentials

          resources:
            requests:
              cpu: "${CPU_REQUEST:-500m}"
              memory: "${MEMORY_REQUEST:-1Gi}"
            limits:
              cpu: "${CPU_LIMIT:-2}"
              memory: "${MEMORY_LIMIT:-4Gi}"

          readinessProbe:
            exec:
              command: ${READINESS_COMMAND}
            periodSeconds: 10
            timeoutSeconds: 5

          livenessProbe:
            exec:
              command: ${LIVENESS_COMMAND}
            periodSeconds: 30
            timeoutSeconds: 5
            failureThreshold: 3

          volumeMounts:
            - name: data
              mountPath: ${DATA_PATH}

      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app.kubernetes.io/name: ${DB_NAME}
              topologyKey: kubernetes.io/hostname

      terminationGracePeriodSeconds: 60

  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: ${STORAGE_CLASS:-standard}
        resources:
          requests:
            storage: ${STORAGE_SIZE:-50Gi}
```

### PostgreSQL StatefulSet

```yaml
# postgresql-statefulset.yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: ${NAMESPACE}
spec:
  clusterIP: None
  selector:
    app.kubernetes.io/name: postgres
  ports:
    - name: postgres
      port: 5432
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: ${NAMESPACE}
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: postgres
  template:
    metadata:
      labels:
        app.kubernetes.io/name: postgres
    spec:
      securityContext:
        fsGroup: 999

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
            - name: POSTGRES_DB
              value: ${DB_NAME:-app}
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata

          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "2"
              memory: "4Gi"

          readinessProbe:
            exec:
              command: ["pg_isready", "-U", "$(POSTGRES_USER)"]
            periodSeconds: 10

          livenessProbe:
            exec:
              command: ["pg_isready", "-U", "$(POSTGRES_USER)"]
            periodSeconds: 30
            failureThreshold: 3

          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data

      terminationGracePeriodSeconds: 60

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

---

## Supporting Resources Templates

### Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: ${APP_NAME}
  ports:
    - name: http
      port: 80
      targetPort: http
      protocol: TCP
```

### Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  tls:
    - hosts:
        - ${DOMAIN}
      secretName: ${APP_NAME}-tls
  rules:
    - host: ${DOMAIN}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ${APP_NAME}
                port:
                  number: 80
```

### ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-config
  namespace: ${NAMESPACE}
data:
  LOG_LEVEL: "info"
  LOG_FORMAT: "json"
  APP_ENV: "production"
  # Add application-specific config
```

### Secret (template - use sealed-secrets or external-secrets in practice)

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
type: Opaque
stringData:
  DATABASE_URL: "postgres://user:password@postgres:5432/db"
  SECRET_KEY: "your-secret-key"
  # Add application-specific secrets
```

### ServiceAccount with RBAC

```yaml
# serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
subjects:
  - kind: ServiceAccount
    name: ${APP_NAME}
    namespace: ${NAMESPACE}
roleRef:
  kind: Role
  name: ${APP_NAME}
  apiGroup: rbac.authorization.k8s.io
```

### PodDisruptionBudget

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ${APP_NAME}-pdb
  namespace: ${NAMESPACE}
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
```

### HorizontalPodAutoscaler

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ${APP_NAME}-hpa
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ${APP_NAME}
  minReplicas: ${MIN_REPLICAS:-3}
  maxReplicas: ${MAX_REPLICAS:-20}
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

### NetworkPolicy

```yaml
# networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ${APP_NAME}-network-policy
  namespace: ${NAMESPACE}
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
      ports:
        - protocol: TCP
          port: ${PORT:-8000}
  egress:
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: redis
      ports:
        - protocol: TCP
          port: 6379
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

---

## Argo Rollouts Templates

### Canary Rollout

```yaml
# rollout-canary.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS:-5}
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${APP_NAME}
    spec:
      # Same spec as Deployment template
      containers:
        - name: ${APP_NAME}
          image: ${REGISTRY}/${APP_NAME}:${VERSION}
          # ... rest of container spec

  strategy:
    canary:
      canaryService: ${APP_NAME}-canary
      stableService: ${APP_NAME}-stable
      trafficRouting:
        nginx:
          stableIngress: ${APP_NAME}-stable
      steps:
        - setWeight: 10
        - pause: {duration: 5m}
        - analysis:
            templates:
              - templateName: ${APP_NAME}-success-rate
        - setWeight: 30
        - pause: {duration: 5m}
        - setWeight: 50
        - pause: {duration: 10m}
        - setWeight: 80
        - pause: {duration: 10m}
```

### Analysis Template

```yaml
# analysis-template.yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: ${APP_NAME}-success-rate
  namespace: ${NAMESPACE}
spec:
  metrics:
    - name: success-rate
      interval: 1m
      count: 5
      successCondition: result[0] >= 0.99
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus-server.monitoring:80
          query: |
            sum(rate(http_requests_total{
              app="${APP_NAME}",
              status=~"2.."
            }[5m])) /
            sum(rate(http_requests_total{
              app="${APP_NAME}"
            }[5m]))
```

---

## Kustomization Template

### Base Kustomization

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
  - serviceaccount.yaml
  - pdb.yaml
  - hpa.yaml
  - networkpolicy.yaml

commonLabels:
  app.kubernetes.io/name: ${APP_NAME}
  app.kubernetes.io/managed-by: kustomize

images:
  - name: ${REGISTRY}/${APP_NAME}
    newTag: latest
```

### Production Overlay

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
  - ../../base
  - ingress.yaml
  - secret.yaml

images:
  - name: ${REGISTRY}/${APP_NAME}
    newTag: ${VERSION}

replicas:
  - name: ${APP_NAME}
    count: 5

patches:
  - target:
      kind: Deployment
      name: ${APP_NAME}
    patch: |
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/memory
        value: 1Gi
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/cpu
        value: "1"
```

---

## Namespace Template with PSS

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    # Pod Security Standards (2025-2026)
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest
```

---

## Resource Quota Template

```yaml
# resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ${NAMESPACE}-quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    persistentvolumeclaims: "10"
    pods: "50"
```

---

*Kubernetes Deployment Templates | faion-infrastructure-engineer*
