# Kubernetes Templates

Ready-to-use YAML templates for common Kubernetes resources.

---

## Deployment Templates

### Web Application

```yaml
# deployment-web.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{APP_NAME}}
  labels:
    app: {{APP_NAME}}
    environment: {{ENV}}
spec:
  replicas: {{REPLICAS}}
  selector:
    matchLabels:
      app: {{APP_NAME}}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
  template:
    metadata:
      labels:
        app: {{APP_NAME}}
        environment: {{ENV}}
    spec:
      serviceAccountName: {{APP_NAME}}-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: {{APP_NAME}}
        image: {{IMAGE}}:{{TAG}}
        ports:
        - containerPort: {{PORT}}
          name: http
        resources:
          requests:
            memory: "{{MEM_REQUEST}}"
            cpu: "{{CPU_REQUEST}}"
          limits:
            memory: "{{MEM_LIMIT}}"
            cpu: "{{CPU_LIMIT}}"
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
        envFrom:
        - configMapRef:
            name: {{APP_NAME}}-config
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: {{APP_NAME}}
              topologyKey: kubernetes.io/hostname
```

### Worker/Job Processor

```yaml
# deployment-worker.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{APP_NAME}}-worker
  labels:
    app: {{APP_NAME}}
    component: worker
spec:
  replicas: {{REPLICAS}}
  selector:
    matchLabels:
      app: {{APP_NAME}}
      component: worker
  template:
    metadata:
      labels:
        app: {{APP_NAME}}
        component: worker
    spec:
      serviceAccountName: {{APP_NAME}}-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: worker
        image: {{IMAGE}}:{{TAG}}
        command: ["./worker"]
        resources:
          requests:
            memory: "{{MEM_REQUEST}}"
            cpu: "{{CPU_REQUEST}}"
          limits:
            memory: "{{MEM_LIMIT}}"
        securityContext:
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - "pidof worker"
          initialDelaySeconds: 10
          periodSeconds: 30
        envFrom:
        - configMapRef:
            name: {{APP_NAME}}-config
        - secretRef:
            name: {{APP_NAME}}-secrets
```

### CronJob

```yaml
# cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {{JOB_NAME}}
spec:
  schedule: "{{CRON_SCHEDULE}}"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 3
      activeDeadlineSeconds: 3600
      template:
        spec:
          serviceAccountName: {{JOB_NAME}}-sa
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
          restartPolicy: OnFailure
          containers:
          - name: {{JOB_NAME}}
            image: {{IMAGE}}:{{TAG}}
            command: ["./job"]
            resources:
              requests:
                memory: "{{MEM_REQUEST}}"
                cpu: "{{CPU_REQUEST}}"
              limits:
                memory: "{{MEM_LIMIT}}"
            securityContext:
              readOnlyRootFilesystem: true
              allowPrivilegeEscalation: false
              capabilities:
                drop: ["ALL"]
            envFrom:
            - configMapRef:
                name: {{JOB_NAME}}-config
```

---

## Service Templates

### ClusterIP Service

```yaml
# service-clusterip.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{APP_NAME}}
  labels:
    app: {{APP_NAME}}
spec:
  type: ClusterIP
  selector:
    app: {{APP_NAME}}
  ports:
  - name: http
    port: 80
    targetPort: {{PORT}}
```

### LoadBalancer Service

```yaml
# service-lb.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{APP_NAME}}-lb
  labels:
    app: {{APP_NAME}}
  annotations:
    # AWS NLB
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    # GCP
    # cloud.google.com/load-balancer-type: "External"
spec:
  type: LoadBalancer
  selector:
    app: {{APP_NAME}}
  ports:
  - name: http
    port: 80
    targetPort: {{PORT}}
  - name: https
    port: 443
    targetPort: {{PORT_HTTPS}}
```

---

## Ingress Templates

### Nginx Ingress

```yaml
# ingress-nginx.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{APP_NAME}}
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  tls:
  - hosts:
    - {{DOMAIN}}
    secretName: {{APP_NAME}}-tls
  rules:
  - host: {{DOMAIN}}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {{APP_NAME}}
            port:
              number: 80
```

### Traefik IngressRoute

```yaml
# ingressroute-traefik.yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: {{APP_NAME}}
spec:
  entryPoints:
  - websecure
  routes:
  - match: Host(`{{DOMAIN}}`)
    kind: Rule
    services:
    - name: {{APP_NAME}}
      port: 80
  tls:
    certResolver: letsencrypt
```

---

## Autoscaling Templates

### HPA

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{APP_NAME}}-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{APP_NAME}}
  minReplicas: {{MIN_REPLICAS}}
  maxReplicas: {{MAX_REPLICAS}}
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
```

### PodDisruptionBudget

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{APP_NAME}}-pdb
spec:
  minAvailable: {{MIN_AVAILABLE}}
  selector:
    matchLabels:
      app: {{APP_NAME}}
```

---

## Security Templates

### ServiceAccount

```yaml
# serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{APP_NAME}}-sa
  annotations:
    # AWS IRSA
    eks.amazonaws.com/role-arn: arn:aws:iam::{{ACCOUNT_ID}}:role/{{ROLE_NAME}}
    # GCP Workload Identity
    # iam.gke.io/gcp-service-account: {{GSA_NAME}}@{{PROJECT_ID}}.iam.gserviceaccount.com
```

### NetworkPolicy (Default Deny + Allow)

```yaml
# networkpolicy.yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: {{NAMESPACE}}
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{APP_NAME}}-netpol
  namespace: {{NAMESPACE}}
spec:
  podSelector:
    matchLabels:
      app: {{APP_NAME}}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: {{ALLOWED_APP}}
    ports:
    - protocol: TCP
      port: {{PORT}}
  egress:
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
  - to:
    - podSelector:
        matchLabels:
          app: {{DB_APP}}
    ports:
    - protocol: TCP
      port: {{DB_PORT}}
```

### ResourceQuota

```yaml
# resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: {{NAMESPACE}}-quota
  namespace: {{NAMESPACE}}
spec:
  hard:
    requests.cpu: "{{CPU_REQUEST_TOTAL}}"
    requests.memory: "{{MEM_REQUEST_TOTAL}}"
    limits.cpu: "{{CPU_LIMIT_TOTAL}}"
    limits.memory: "{{MEM_LIMIT_TOTAL}}"
    pods: "{{MAX_PODS}}"
    services: "{{MAX_SERVICES}}"
    secrets: "{{MAX_SECRETS}}"
    configmaps: "{{MAX_CONFIGMAPS}}"
```

### LimitRange

```yaml
# limitrange.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: {{NAMESPACE}}-limits
  namespace: {{NAMESPACE}}
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
```

---

## Config Templates

### ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{APP_NAME}}-config
data:
  APP_ENV: "{{ENV}}"
  LOG_LEVEL: "{{LOG_LEVEL}}"
  DATABASE_HOST: "{{DB_HOST}}"
  REDIS_HOST: "{{REDIS_HOST}}"
```

### External Secret (ESO)

```yaml
# external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{APP_NAME}}-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: {{SECRET_STORE}}
    kind: ClusterSecretStore
  target:
    name: {{APP_NAME}}-secrets
    creationPolicy: Owner
  data:
  - secretKey: DATABASE_PASSWORD
    remoteRef:
      key: {{SECRET_PATH}}
      property: database_password
  - secretKey: API_KEY
    remoteRef:
      key: {{SECRET_PATH}}
      property: api_key
```

---

## Complete Application Stack

```yaml
# app-stack.yaml
---
# Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: {{NAMESPACE}}
  labels:
    pod-security.kubernetes.io/enforce: restricted
---
# ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{APP_NAME}}-sa
  namespace: {{NAMESPACE}}
---
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{APP_NAME}}-config
  namespace: {{NAMESPACE}}
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
---
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{APP_NAME}}
  namespace: {{NAMESPACE}}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {{APP_NAME}}
  template:
    metadata:
      labels:
        app: {{APP_NAME}}
    spec:
      serviceAccountName: {{APP_NAME}}-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: {{APP_NAME}}
        image: {{IMAGE}}:{{TAG}}
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
        securityContext:
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
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
        envFrom:
        - configMapRef:
            name: {{APP_NAME}}-config
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}
---
# Service
apiVersion: v1
kind: Service
metadata:
  name: {{APP_NAME}}
  namespace: {{NAMESPACE}}
spec:
  selector:
    app: {{APP_NAME}}
  ports:
  - port: 80
    targetPort: 8080
---
# HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{APP_NAME}}-hpa
  namespace: {{NAMESPACE}}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{APP_NAME}}
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
# PDB
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{APP_NAME}}-pdb
  namespace: {{NAMESPACE}}
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: {{APP_NAME}}
```

---

## Template Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{{APP_NAME}}` | Application name | myapp |
| `{{NAMESPACE}}` | Kubernetes namespace | production |
| `{{ENV}}` | Environment | production, staging |
| `{{IMAGE}}` | Container image | myregistry/myapp |
| `{{TAG}}` | Image tag | v1.0.0 |
| `{{PORT}}` | Container port | 8080 |
| `{{REPLICAS}}` | Number of replicas | 3 |
| `{{MEM_REQUEST}}` | Memory request | 256Mi |
| `{{MEM_LIMIT}}` | Memory limit | 512Mi |
| `{{CPU_REQUEST}}` | CPU request | 250m |
| `{{CPU_LIMIT}}` | CPU limit | 500m |
| `{{DOMAIN}}` | Domain name | app.example.com |
| `{{MIN_REPLICAS}}` | HPA min replicas | 2 |
| `{{MAX_REPLICAS}}` | HPA max replicas | 10 |
