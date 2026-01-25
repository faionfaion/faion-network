---
name: faion-k8s-resources
user-invocable: false
description: ""
---

# Kubernetes Advanced Resources

**Ingress, NetworkPolicies, Helm, Kustomize, and monitoring**

---

## Ingress

### Basic Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### TLS Ingress

```yaml
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### Common Annotations (nginx-ingress)

```yaml
annotations:
  # Rate limiting
  nginx.ingress.kubernetes.io/limit-rps: "10"

  # SSL redirect
  nginx.ingress.kubernetes.io/ssl-redirect: "true"

  # Proxy settings
  nginx.ingress.kubernetes.io/proxy-body-size: "10m"
  nginx.ingress.kubernetes.io/proxy-read-timeout: "60"

  # CORS
  nginx.ingress.kubernetes.io/enable-cors: "true"
  nginx.ingress.kubernetes.io/cors-allow-origin: "https://example.com"
```

---

## NetworkPolicies

### Default Deny All

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow Specific Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-myapp
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
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
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

---

## Helm

### Chart Management

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search charts
helm search repo nginx
helm search hub postgres

# Install chart
helm install myrelease bitnami/nginx
helm install myrelease bitnami/nginx -f values.yaml
helm install myrelease bitnami/nginx --set service.type=LoadBalancer

# Upgrade
helm upgrade myrelease bitnami/nginx -f values.yaml
helm upgrade --install myrelease bitnami/nginx  # Install or upgrade

# Rollback
helm rollback myrelease 1

# Uninstall
helm uninstall myrelease

# List releases
helm list
helm list -A  # All namespaces

# Show chart info
helm show values bitnami/nginx
helm show chart bitnami/nginx
```

### Creating Charts

```bash
# Create new chart
helm create mychart
```

**Chart Structure:**

```
mychart/
  Chart.yaml          # Chart metadata
  values.yaml         # Default values
  charts/             # Dependencies
  templates/          # Kubernetes manifests
    deployment.yaml
    service.yaml
    ingress.yaml
    configmap.yaml
    _helpers.tpl      # Template helpers
    NOTES.txt         # Post-install notes
```

### Chart.yaml

```yaml
apiVersion: v2
name: mychart
description: ""
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
- name: postgresql
  version: "12.x.x"
  repository: https://charts.bitnami.com/bitnami
  condition: postgresql.enabled
```

### values.yaml

```yaml
replicaCount: 3

image:
  repository: myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
  - host: myapp.example.com
    paths:
    - path: /
      pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 128Mi
  requests:
    cpu: 250m
    memory: 64Mi

postgresql:
  enabled: true
  auth:
    database: myapp
```

### Template Helpers (_helpers.tpl)

```yaml
{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "mychart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

### Template Usage

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        {{- if .Values.resources }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        {{- end }}
```

---

## Kustomize

### Basic Structure

```
base/
  deployment.yaml
  service.yaml
  kustomization.yaml
overlays/
  development/
    kustomization.yaml
  production/
    kustomization.yaml
    replica-patch.yaml
```

### base/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

commonLabels:
  app: myapp

images:
- name: myapp
  newTag: latest
```

### overlays/production/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
- ../../base

namePrefix: prod-

commonLabels:
  environment: production

images:
- name: myapp
  newTag: v1.0.0

patches:
- path: replica-patch.yaml
```

### Patches

```yaml
# Strategic merge patch
# replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5

# JSON patch
patches:
- target:
    kind: Deployment
    name: myapp
  patch: |-
    - op: replace
      path: /spec/replicas
      value: 5
```

### Apply Kustomize

```bash
# Preview
kubectl kustomize overlays/production

# Apply
kubectl apply -k overlays/production
```

---

## Monitoring (Prometheus)

### ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-monitor
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### PrometheusRule

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
  labels:
    release: prometheus
spec:
  groups:
  - name: myapp
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: High error rate on {{ $labels.instance }}
```

### Common PromQL Queries

```promql
# Container CPU usage
rate(container_cpu_usage_seconds_total{container!=""}[5m])

# Container memory usage
container_memory_usage_bytes{container!=""}

# Pod restart count
kube_pod_container_status_restarts_total

# HTTP request rate
rate(http_requests_total[5m])

# HTTP error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

---

## References

- [Helm Docs](https://helm.sh/docs/)
- [Kustomize Docs](https://kustomize.io/)
- [Prometheus Operator](https://prometheus-operator.dev/)

## Sources

- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [Workload Resources](https://kubernetes.io/docs/concepts/workloads/)
- [Service Resources](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Storage Resources](https://kubernetes.io/docs/concepts/storage/)
- [Configuration Resources](https://kubernetes.io/docs/concepts/configuration/)
