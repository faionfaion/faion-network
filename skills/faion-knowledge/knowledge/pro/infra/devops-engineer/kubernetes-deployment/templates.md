# Kubernetes Deployment Templates

## Rolling Update Template

```yaml
# rolling-update-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ APP_NAME }}
  namespace: {{ NAMESPACE }}
  labels:
    app.kubernetes.io/name: {{ APP_NAME }}
    app.kubernetes.io/version: "{{ VERSION }}"
    app.kubernetes.io/component: {{ COMPONENT }}
spec:
  replicas: {{ REPLICAS | default: 3 }}
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ APP_NAME }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ APP_NAME }}
        app.kubernetes.io/version: "{{ VERSION }}"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "{{ PORT }}"
    spec:
      serviceAccountName: {{ APP_NAME }}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: {{ APP_NAME }}
          image: {{ REGISTRY }}/{{ APP_NAME }}:{{ VERSION }}
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: {{ PORT }}
          envFrom:
            - configMapRef:
                name: {{ APP_NAME }}-config
            - secretRef:
                name: {{ APP_NAME }}-secrets
          resources:
            requests:
              cpu: "{{ CPU_REQUEST | default: 100m }}"
              memory: "{{ MEM_REQUEST | default: 256Mi }}"
            limits:
              cpu: "{{ CPU_LIMIT | default: 500m }}"
              memory: "{{ MEM_LIMIT | default: 512Mi }}"
          livenessProbe:
            httpGet:
              path: {{ HEALTH_PATH | default: /health/live }}
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: {{ READY_PATH | default: /health/ready }}
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: {{ HEALTH_PATH | default: /health/live }}
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30
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
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: {{ APP_NAME }}
                topologyKey: kubernetes.io/hostname
```

---

## Blue-Green Rollout Template

```yaml
# blue-green-rollout.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: {{ APP_NAME }}
  namespace: {{ NAMESPACE }}
spec:
  replicas: {{ REPLICAS | default: 3 }}
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: {{ APP_NAME }}
  template:
    metadata:
      labels:
        app: {{ APP_NAME }}
        version: "{{ VERSION }}"
    spec:
      containers:
        - name: {{ APP_NAME }}
          image: {{ REGISTRY }}/{{ APP_NAME }}:{{ VERSION }}
          ports:
            - containerPort: {{ PORT }}
          resources:
            requests:
              cpu: "{{ CPU_REQUEST | default: 100m }}"
              memory: "{{ MEM_REQUEST | default: 256Mi }}"
            limits:
              cpu: "{{ CPU_LIMIT | default: 500m }}"
              memory: "{{ MEM_LIMIT | default: 512Mi }}"
          livenessProbe:
            httpGet:
              path: {{ HEALTH_PATH | default: /health/live }}
              port: {{ PORT }}
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: {{ READY_PATH | default: /health/ready }}
              port: {{ PORT }}
            initialDelaySeconds: 5
            periodSeconds: 5
  strategy:
    blueGreen:
      activeService: {{ APP_NAME }}-active
      previewService: {{ APP_NAME }}-preview
      autoPromotionEnabled: {{ AUTO_PROMOTE | default: false }}
      autoPromotionSeconds: {{ AUTO_PROMOTE_DELAY | default: 30 }}
      scaleDownDelaySeconds: {{ SCALE_DOWN_DELAY | default: 30 }}
      previewReplicaCount: {{ PREVIEW_REPLICAS | default: 1 }}
      # Optional: Add analysis
      # prePromotionAnalysis:
      #   templates:
      #     - templateName: smoke-tests
      # postPromotionAnalysis:
      #   templates:
      #     - templateName: success-rate
---
apiVersion: v1
kind: Service
metadata:
  name: {{ APP_NAME }}-active
  namespace: {{ NAMESPACE }}
spec:
  selector:
    app: {{ APP_NAME }}
  ports:
    - port: 80
      targetPort: {{ PORT }}
---
apiVersion: v1
kind: Service
metadata:
  name: {{ APP_NAME }}-preview
  namespace: {{ NAMESPACE }}
spec:
  selector:
    app: {{ APP_NAME }}
  ports:
    - port: 80
      targetPort: {{ PORT }}
```

---

## Canary Rollout Template (Basic)

```yaml
# canary-rollout-basic.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: {{ APP_NAME }}
  namespace: {{ NAMESPACE }}
spec:
  replicas: {{ REPLICAS | default: 5 }}
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: {{ APP_NAME }}
  template:
    metadata:
      labels:
        app: {{ APP_NAME }}
        version: "{{ VERSION }}"
    spec:
      containers:
        - name: {{ APP_NAME }}
          image: {{ REGISTRY }}/{{ APP_NAME }}:{{ VERSION }}
          ports:
            - containerPort: {{ PORT }}
          resources:
            requests:
              cpu: "{{ CPU_REQUEST | default: 100m }}"
              memory: "{{ MEM_REQUEST | default: 256Mi }}"
            limits:
              cpu: "{{ CPU_LIMIT | default: 500m }}"
              memory: "{{ MEM_LIMIT | default: 512Mi }}"
          livenessProbe:
            httpGet:
              path: {{ HEALTH_PATH | default: /health/live }}
              port: {{ PORT }}
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: {{ READY_PATH | default: /health/ready }}
              port: {{ PORT }}
            initialDelaySeconds: 5
            periodSeconds: 5
  strategy:
    canary:
      maxSurge: "25%"
      maxUnavailable: 0
      steps:
        - setWeight: 5
        - pause: { duration: {{ STEP1_PAUSE | default: 5m }} }
        - setWeight: 25
        - pause: { duration: {{ STEP2_PAUSE | default: 10m }} }
        - setWeight: 50
        - pause: { duration: {{ STEP3_PAUSE | default: 10m }} }
        - setWeight: 75
        - pause: { duration: {{ STEP4_PAUSE | default: 5m }} }
```

---

## Canary Rollout Template (Istio)

```yaml
# canary-rollout-istio.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: {{ APP_NAME }}
  namespace: {{ NAMESPACE }}
spec:
  replicas: {{ REPLICAS | default: 5 }}
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: {{ APP_NAME }}
  template:
    metadata:
      labels:
        app: {{ APP_NAME }}
        version: "{{ VERSION }}"
    spec:
      containers:
        - name: {{ APP_NAME }}
          image: {{ REGISTRY }}/{{ APP_NAME }}:{{ VERSION }}
          ports:
            - containerPort: {{ PORT }}
          resources:
            requests:
              cpu: "{{ CPU_REQUEST | default: 100m }}"
              memory: "{{ MEM_REQUEST | default: 256Mi }}"
            limits:
              cpu: "{{ CPU_LIMIT | default: 500m }}"
              memory: "{{ MEM_LIMIT | default: 512Mi }}"
  strategy:
    canary:
      canaryService: {{ APP_NAME }}-canary
      stableService: {{ APP_NAME }}-stable
      trafficRouting:
        istio:
          virtualServices:
            - name: {{ APP_NAME }}-vsvc
              routes:
                - primary
      analysis:
        templates:
          - templateName: {{ ANALYSIS_TEMPLATE | default: success-rate }}
        startingStep: 2
        args:
          - name: service-name
            value: {{ APP_NAME }}-canary
      steps:
        - setWeight: 5
        - pause: { duration: 2m }
        - setWeight: 10
        - pause: { duration: 5m }
        - setWeight: 25
        - pause: { duration: 10m }
        - setWeight: 50
        - pause: { duration: 10m }
        - setWeight: 75
        - pause: { duration: 5m }
---
apiVersion: v1
kind: Service
metadata:
  name: {{ APP_NAME }}-stable
  namespace: {{ NAMESPACE }}
spec:
  selector:
    app: {{ APP_NAME }}
  ports:
    - port: 80
      targetPort: {{ PORT }}
---
apiVersion: v1
kind: Service
metadata:
  name: {{ APP_NAME }}-canary
  namespace: {{ NAMESPACE }}
spec:
  selector:
    app: {{ APP_NAME }}
  ports:
    - port: 80
      targetPort: {{ PORT }}
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: {{ APP_NAME }}-vsvc
  namespace: {{ NAMESPACE }}
spec:
  hosts:
    - {{ HOST }}
  gateways:
    - {{ GATEWAY | default: default-gateway }}
  http:
    - name: primary
      route:
        - destination:
            host: {{ APP_NAME }}-stable
          weight: 100
        - destination:
            host: {{ APP_NAME }}-canary
          weight: 0
```

---

## Analysis Template (Prometheus)

```yaml
# analysis-template-prometheus.yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: {{ TEMPLATE_NAME | default: success-rate }}
  namespace: {{ NAMESPACE }}
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: {{ INTERVAL | default: 1m }}
      successCondition: result[0] >= {{ SUCCESS_THRESHOLD | default: 0.99 }}
      failureLimit: {{ FAILURE_LIMIT | default: 3 }}
      provider:
        prometheus:
          address: {{ PROMETHEUS_URL | default: http://prometheus.monitoring:9090 }}
          query: |
            sum(rate(http_requests_total{
              service="{{args.service-name}}",
              status=~"2.."
            }[5m])) /
            sum(rate(http_requests_total{
              service="{{args.service-name}}"
            }[5m]))
    - name: latency-p99
      interval: {{ INTERVAL | default: 1m }}
      successCondition: result[0] < {{ LATENCY_THRESHOLD_MS | default: 500 }}
      failureLimit: {{ FAILURE_LIMIT | default: 3 }}
      provider:
        prometheus:
          address: {{ PROMETHEUS_URL | default: http://prometheus.monitoring:9090 }}
          query: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket{
                service="{{args.service-name}}"
              }[5m])) by (le)
            ) * 1000
```

---

## HPA Template

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ APP_NAME }}-hpa
  namespace: {{ NAMESPACE }}
spec:
  scaleTargetRef:
    apiVersion: {{ API_VERSION | default: apps/v1 }}
    kind: {{ KIND | default: Deployment }}
    name: {{ APP_NAME }}
  minReplicas: {{ MIN_REPLICAS | default: 3 }}
  maxReplicas: {{ MAX_REPLICAS | default: 10 }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ CPU_TARGET | default: 70 }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ MEM_TARGET | default: 80 }}
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

## PodDisruptionBudget Template

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ APP_NAME }}-pdb
  namespace: {{ NAMESPACE }}
spec:
  minAvailable: {{ MIN_AVAILABLE | default: 2 }}
  selector:
    matchLabels:
      app: {{ APP_NAME }}
```

---

## NetworkPolicy Template

```yaml
# networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ APP_NAME }}-netpol
  namespace: {{ NAMESPACE }}
spec:
  podSelector:
    matchLabels:
      app: {{ APP_NAME }}
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
          port: {{ PORT }}
  egress:
    # Allow DNS
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
    # Allow database
    - to:
        - podSelector:
            matchLabels:
              app: {{ DB_APP | default: postgres }}
      ports:
        - protocol: TCP
          port: {{ DB_PORT | default: 5432 }}
```

---

## Usage Instructions

### Variable Substitution

Replace template variables with actual values:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{ APP_NAME }}` | Application name | `myapp` |
| `{{ NAMESPACE }}` | Kubernetes namespace | `production` |
| `{{ VERSION }}` | Image version tag | `1.2.0` |
| `{{ REGISTRY }}` | Container registry | `registry.example.com` |
| `{{ PORT }}` | Container port | `8080` |
| `{{ REPLICAS }}` | Replica count | `3` |
| `{{ HOST }}` | Ingress host | `myapp.example.com` |

### Tools for Substitution

**envsubst:**
```bash
envsubst < template.yaml > output.yaml
```

**Helm:**
```bash
helm template myapp ./chart -f values.yaml
```

**Kustomize:**
```yaml
# kustomization.yaml
resources:
  - deployment.yaml
patches:
  - patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
    target:
      kind: Deployment
```
