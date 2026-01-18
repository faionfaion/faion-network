# M-DO-006: Helm Charts

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #kubernetes, #helm, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Raw Kubernetes manifests are verbose and repetitive. Managing configuration for multiple environments requires duplicating files and manual changes.

## Promise

After this methodology, you will package Kubernetes applications with Helm. Charts will be reusable, version-controlled, and environment-configurable.

## Overview

Helm is the package manager for Kubernetes. Charts are packages of pre-configured Kubernetes resources with templating and dependency management.

---

## Framework

### Step 1: Helm Installation

```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Or via package manager
brew install helm          # macOS
apt install helm           # Ubuntu
choco install kubernetes-helm  # Windows

# Verify
helm version

# Add common repositories
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

### Step 2: Chart Structure

```
my-chart/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default values
├── values-staging.yaml  # Environment overrides
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl     # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── hpa.yaml
├── charts/              # Dependencies
└── .helmignore
```

### Step 3: Chart.yaml

```yaml
# Chart.yaml
apiVersion: v2
name: my-app
description: My Application Helm Chart
type: application
version: 1.0.0        # Chart version
appVersion: "2.1.0"   # Application version

keywords:
  - web
  - api

maintainers:
  - name: Team
    email: team@example.com

dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

### Step 4: Values File

```yaml
# values.yaml
replicaCount: 2

image:
  repository: myapp
  tag: "latest"
  pullPolicy: IfNotPresent

imagePullSecrets: []

service:
  type: ClusterIP
  port: 80
  targetPort: 3000

ingress:
  enabled: false
  className: nginx
  annotations: {}
  hosts:
    - host: app.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

env:
  NODE_ENV: production
  LOG_LEVEL: info

secrets:
  DATABASE_URL: ""
  API_KEY: ""

postgresql:
  enabled: true
  auth:
    database: mydb
    username: user

redis:
  enabled: true
```

### Step 5: Template Files

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.targetPort }}
          envFrom:
            - configMapRef:
                name: {{ include "my-app.fullname" . }}-config
            - secretRef:
                name: {{ include "my-app.fullname" . }}-secrets
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /health
              port: {{ .Values.service.targetPort }}
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: {{ .Values.service.targetPort }}
            initialDelaySeconds: 5
```

```yaml
# templates/_helpers.tpl
{{/*
Expand the name of the chart.
*/}}
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "my-app.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{ include "my-app.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "my-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### Step 6: Helm Commands

```bash
# Create new chart
helm create my-chart

# Install chart
helm install my-release ./my-chart
helm install my-release ./my-chart -f values-prod.yaml
helm install my-release ./my-chart --set image.tag=v1.2.3

# Upgrade
helm upgrade my-release ./my-chart
helm upgrade --install my-release ./my-chart  # Install or upgrade

# Rollback
helm rollback my-release 1  # Rollback to revision 1

# Uninstall
helm uninstall my-release

# Debug
helm template my-release ./my-chart         # Render templates
helm install --dry-run --debug my-release ./my-chart

# List releases
helm list
helm list -A  # All namespaces

# History
helm history my-release
```

---

## Templates

### Service

```yaml
# templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: http
  selector:
    {{- include "my-app.selectorLabels" . | nindent 4 }}
```

### Ingress

```yaml
# templates/ingress.yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "my-app.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
```

### ConfigMap and Secret

```yaml
# templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "my-app.fullname" . }}-config
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
data:
  {{- range $key, $value := .Values.env }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}

---
# templates/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "my-app.fullname" . }}-secrets
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
type: Opaque
stringData:
  {{- range $key, $value := .Values.secrets }}
  {{- if $value }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
  {{- end }}
```

---

## Examples

### Multi-Environment

```yaml
# values-staging.yaml
replicaCount: 1

image:
  tag: "staging"

ingress:
  enabled: true
  hosts:
    - host: staging.example.com
      paths:
        - path: /
          pathType: Prefix

autoscaling:
  enabled: false

postgresql:
  auth:
    database: mydb_staging
```

```yaml
# values-prod.yaml
replicaCount: 3

image:
  tag: "v1.2.3"

ingress:
  enabled: true
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls
      hosts:
        - app.example.com

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
```

```bash
# Deploy to staging
helm upgrade --install my-app ./my-chart \
  -f values-staging.yaml \
  -n staging

# Deploy to production
helm upgrade --install my-app ./my-chart \
  -f values-prod.yaml \
  -n production \
  --set secrets.DATABASE_URL="$DATABASE_URL"
```

---

## Common Mistakes

1. **No default values** - Templates fail without values
2. **Hardcoded names** - Use helpers for names
3. **Missing labels** - Break kubectl and helm tracking
4. **Secrets in values.yaml** - Use external secrets manager
5. **No NOTES.txt** - Users don't know how to access app

---

## Checklist

- [ ] Chart.yaml with versions
- [ ] Default values.yaml
- [ ] Environment-specific values files
- [ ] _helpers.tpl for names and labels
- [ ] All resources use fullname
- [ ] Ingress with TLS option
- [ ] Resource limits in values
- [ ] NOTES.txt for post-install info

---

## Next Steps

- M-DO-005: Kubernetes Basics
- M-DO-009: Terraform Basics
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-006 v1.0*
