# Container Orchestration Templates

Copy-paste Kubernetes configurations for common patterns.

## Basic Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
    version: ${VERSION}
spec:
  replicas: ${REPLICAS}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
        version: ${VERSION}
    spec:
      serviceAccountName: ${APP_NAME}-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${VERSION}
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: ${PORT}
        resources:
          requests:
            memory: "${MEMORY_REQUEST}"
            cpu: "${CPU_REQUEST}"
          limits:
            memory: "${MEMORY_LIMIT}"
            cpu: "${CPU_LIMIT}"
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
        envFrom:
        - configMapRef:
            name: ${APP_NAME}-config
        - secretRef:
            name: ${APP_NAME}-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 15
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}
```

---

## Service Templates

### ClusterIP Service (Internal)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app: ${APP_NAME}
spec:
  type: ClusterIP
  selector:
    app: ${APP_NAME}
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
```

### Headless Service (StatefulSet)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  clusterIP: None
  selector:
    app: ${APP_NAME}
  ports:
  - name: ${PROTOCOL}
    port: ${PORT}
    targetPort: ${PORT}
```

### LoadBalancer Service (External)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}-lb
  namespace: ${NAMESPACE}
  annotations:
    # AWS NLB
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
    # GCP
    # cloud.google.com/load-balancer-type: "External"
spec:
  type: LoadBalancer
  selector:
    app: ${APP_NAME}
  ports:
  - name: https
    port: 443
    targetPort: http
```

---

## Ingress Templates

### NGINX Ingress with TLS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}-ingress
  namespace: ${NAMESPACE}
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
spec:
  ingressClassName: nginx
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

### Ingress with Rate Limiting

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}-ingress
  namespace: ${NAMESPACE}
  annotations:
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/rate-limit-connections: "50"
    nginx.ingress.kubernetes.io/limit-rps: "10"
    nginx.ingress.kubernetes.io/limit-rpm: "100"
spec:
  ingressClassName: nginx
  rules:
  - host: ${DOMAIN}
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: ${APP_NAME}
            port:
              number: 80
```

---

## ConfigMap and Secret Templates

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-config
  namespace: ${NAMESPACE}
data:
  LOG_LEVEL: "info"
  API_TIMEOUT: "30s"
  CACHE_TTL: "3600"
  FEATURE_FLAGS: |
    {
      "new_dashboard": true,
      "beta_api": false
    }
```

### Secret (base64 encoded)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
type: Opaque
data:
  # echo -n 'value' | base64
  DATABASE_URL: cG9zdGdyZXM6Ly91c2VyOnBhc3NAaG9zdC9kYg==
  API_KEY: c3VwZXItc2VjcmV0LWtleQ==
```

### External Secrets (AWS Secrets Manager)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: ${APP_NAME}-secrets
    creationPolicy: Owner
  data:
  - secretKey: DATABASE_URL
    remoteRef:
      key: ${ENVIRONMENT}/${APP_NAME}/database
      property: url
  - secretKey: API_KEY
    remoteRef:
      key: ${ENVIRONMENT}/${APP_NAME}/api
      property: key
```

### Sealed Secret (GitOps)

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
spec:
  encryptedData:
    DATABASE_URL: AgBy8BZ3x...encrypted...
    API_KEY: AgA4nV2kP...encrypted...
  template:
    metadata:
      name: ${APP_NAME}-secrets
      namespace: ${NAMESPACE}
    type: Opaque
```

---

## HPA Templates

### Basic CPU/Memory HPA

```yaml
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
  minReplicas: ${MIN_REPLICAS}
  maxReplicas: ${MAX_REPLICAS}
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

### HPA with Custom Metrics

```yaml
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
  minReplicas: 2
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
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

---

## KEDA Templates

### RabbitMQ Scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: ${APP_NAME}-scaler
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    name: ${APP_NAME}
  pollingInterval: 15
  cooldownPeriod: 60
  minReplicaCount: 0
  maxReplicaCount: 50
  triggers:
  - type: rabbitmq
    metadata:
      protocol: amqp
      queueName: ${QUEUE_NAME}
      mode: QueueLength
      value: "10"
    authenticationRef:
      name: rabbitmq-auth
---
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: rabbitmq-auth
  namespace: ${NAMESPACE}
spec:
  secretTargetRef:
  - parameter: host
    name: rabbitmq-secrets
    key: connection-string
```

### Kafka Scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: ${APP_NAME}-scaler
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    name: ${APP_NAME}
  minReplicaCount: 0
  maxReplicaCount: 100
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: ${KAFKA_BROKERS}
      consumerGroup: ${CONSUMER_GROUP}
      topic: ${TOPIC}
      lagThreshold: "100"
      offsetResetPolicy: earliest
```

### Prometheus Scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: ${APP_NAME}-scaler
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    name: ${APP_NAME}
  minReplicaCount: 1
  maxReplicaCount: 30
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus.monitoring.svc:9090
      metricName: http_requests_total
      threshold: "100"
      query: sum(rate(http_requests_total{service="${APP_NAME}"}[2m]))
```

### Cron Scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: ${APP_NAME}-cron-scaler
  namespace: ${NAMESPACE}
spec:
  scaleTargetRef:
    name: ${APP_NAME}
  minReplicaCount: 1
  maxReplicaCount: 20
  triggers:
  - type: cron
    metadata:
      timezone: Europe/Kyiv
      start: 0 8 * * 1-5    # 8 AM weekdays
      end: 0 20 * * 1-5     # 8 PM weekdays
      desiredReplicas: "10"
  - type: cron
    metadata:
      timezone: Europe/Kyiv
      start: 0 20 * * 1-5   # 8 PM weekdays
      end: 0 8 * * 1-5      # 8 AM weekdays
      desiredReplicas: "2"
```

---

## StatefulSet Template

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  serviceName: ${APP_NAME}
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      serviceAccountName: ${APP_NAME}-sa
      securityContext:
        fsGroup: 1000
        runAsUser: 1000
        runAsNonRoot: true
      terminationGracePeriodSeconds: 30
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${VERSION}
        ports:
        - containerPort: ${PORT}
          name: ${PROTOCOL}
        resources:
          requests:
            memory: "${MEMORY_REQUEST}"
            cpu: "${CPU_REQUEST}"
          limits:
            memory: "${MEMORY_LIMIT}"
            cpu: "${CPU_LIMIT}"
        volumeMounts:
        - name: data
          mountPath: /data
        livenessProbe:
          tcpSocket:
            port: ${PORT}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          tcpSocket:
            port: ${PORT}
          initialDelaySeconds: 10
          periodSeconds: 5
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: ${STORAGE_CLASS}
      resources:
        requests:
          storage: ${STORAGE_SIZE}
```

---

## Storage Templates

### StorageClass (AWS EBS)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "10000"
  throughput: "500"
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain
allowVolumeExpansion: true
```

### StorageClass (GCP PD)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain
allowVolumeExpansion: true
```

### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ${APP_NAME}-data
  namespace: ${NAMESPACE}
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: ${STORAGE_SIZE}
```

### VolumeSnapshot

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: ${APP_NAME}-snapshot-${DATE}
  namespace: ${NAMESPACE}
spec:
  volumeSnapshotClassName: csi-snapclass
  source:
    persistentVolumeClaimName: ${APP_NAME}-data
```

---

## Network Policy Templates

### Default Deny All

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: ${NAMESPACE}
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow DNS

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: ${NAMESPACE}
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

### Allow Ingress from Specific Namespace

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ${APP_NAME}-ingress
  namespace: ${NAMESPACE}
spec:
  podSelector:
    matchLabels:
      app: ${APP_NAME}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: ${SOURCE_NAMESPACE}
    - podSelector:
        matchLabels:
          app: ${SOURCE_APP}
    ports:
    - protocol: TCP
      port: ${PORT}
```

### Allow Egress to Specific Service

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ${APP_NAME}-egress
  namespace: ${NAMESPACE}
spec:
  podSelector:
    matchLabels:
      app: ${APP_NAME}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: ${TARGET_NAMESPACE}
      podSelector:
        matchLabels:
          app: ${TARGET_APP}
    ports:
    - protocol: TCP
      port: ${TARGET_PORT}
```

---

## RBAC Templates

### ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ${APP_NAME}-sa
  namespace: ${NAMESPACE}
automountServiceAccountToken: false
```

### Role (Namespace-scoped)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ${APP_NAME}-role
  namespace: ${NAMESPACE}
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["${APP_NAME}-config"]
  verbs: ["get", "watch"]
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["${APP_NAME}-secrets"]
  verbs: ["get"]
```

### RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${APP_NAME}-binding
  namespace: ${NAMESPACE}
subjects:
- kind: ServiceAccount
  name: ${APP_NAME}-sa
  namespace: ${NAMESPACE}
roleRef:
  kind: Role
  name: ${APP_NAME}-role
  apiGroup: rbac.authorization.k8s.io
```

### ClusterRole (Cluster-scoped)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ${APP_NAME}-cluster-role
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get", "list"]
```

---

## Pod Security Templates

### Pod Security Context (Restricted)

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
```

### Pod Security Admission (Namespace)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

---

## Resource Quota Template

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ${NAMESPACE}-quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: "${CPU_REQUESTS_TOTAL}"
    requests.memory: "${MEMORY_REQUESTS_TOTAL}"
    limits.cpu: "${CPU_LIMITS_TOTAL}"
    limits.memory: "${MEMORY_LIMITS_TOTAL}"
    pods: "${MAX_PODS}"
    persistentvolumeclaims: "${MAX_PVCS}"
    services.loadbalancers: "${MAX_LBS}"
```

---

## LimitRange Template

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: ${NAMESPACE}-limits
  namespace: ${NAMESPACE}
spec:
  limits:
  - type: Container
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "2"
      memory: "4Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
  - type: PersistentVolumeClaim
    max:
      storage: "100Gi"
    min:
      storage: "1Gi"
```

---

## PodDisruptionBudget Template

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ${APP_NAME}-pdb
  namespace: ${NAMESPACE}
spec:
  minAvailable: ${MIN_AVAILABLE}  # or use maxUnavailable
  selector:
    matchLabels:
      app: ${APP_NAME}
```

---

## Monitoring Templates

### ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ${APP_NAME}-monitor
  namespace: monitoring
  labels:
    release: prometheus
spec:
  namespaceSelector:
    matchNames:
    - ${NAMESPACE}
  selector:
    matchLabels:
      app: ${APP_NAME}
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
    scheme: http
```

### PrometheusRule

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ${APP_NAME}-alerts
  namespace: monitoring
  labels:
    release: prometheus
spec:
  groups:
  - name: ${APP_NAME}.rules
    rules:
    - alert: ${APP_NAME}HighErrorRate
      expr: |
        sum(rate(http_requests_total{service="${APP_NAME}",status=~"5.."}[5m])) /
        sum(rate(http_requests_total{service="${APP_NAME}"}[5m])) > 0.01
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error rate on ${APP_NAME}"
        description: "Error rate is {{ $value | humanizePercentage }}"
```

---

## Job and CronJob Templates

### Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: ${JOB_NAME}
  namespace: ${NAMESPACE}
spec:
  backoffLimit: 3
  ttlSecondsAfterFinished: 3600
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: ${JOB_NAME}
        image: ${IMAGE}:${VERSION}
        command: ["${COMMAND}"]
        args: ["${ARGS}"]
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ${CRONJOB_NAME}
  namespace: ${NAMESPACE}
spec:
  schedule: "${CRON_SCHEDULE}"  # e.g., "0 2 * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: ${CRONJOB_NAME}
            image: ${IMAGE}:${VERSION}
            command: ["${COMMAND}"]
            resources:
              requests:
                memory: "256Mi"
                cpu: "100m"
              limits:
                memory: "512Mi"
                cpu: "500m"
```

---

## Quick Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `${APP_NAME}` | Application name | `api`, `frontend` |
| `${NAMESPACE}` | Kubernetes namespace | `production`, `staging` |
| `${VERSION}` | Application version | `v1.2.0`, `latest` |
| `${IMAGE}` | Container image | `registry.example.com/api` |
| `${PORT}` | Container port | `8080`, `3000` |
| `${REPLICAS}` | Number of replicas | `3`, `5` |
| `${DOMAIN}` | Domain name | `api.example.com` |
| `${MEMORY_REQUEST}` | Memory request | `256Mi`, `1Gi` |
| `${MEMORY_LIMIT}` | Memory limit | `512Mi`, `2Gi` |
| `${CPU_REQUEST}` | CPU request | `100m`, `500m` |
| `${CPU_LIMIT}` | CPU limit | `500m`, `1000m` |
| `${STORAGE_SIZE}` | Storage size | `10Gi`, `100Gi` |
| `${STORAGE_CLASS}` | StorageClass name | `fast-ssd`, `standard` |
| `${MIN_REPLICAS}` | HPA minimum | `2`, `3` |
| `${MAX_REPLICAS}` | HPA maximum | `10`, `50` |
