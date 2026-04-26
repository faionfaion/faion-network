# Helm Advanced Examples

## Library Chart Example

### Directory Structure

```
common-lib/
  Chart.yaml
  templates/
    _helpers.tpl
    _configmap.tpl
    _deployment.tpl
    _service.tpl
    _util.tpl
```

### Chart.yaml

```yaml
apiVersion: v2
name: common-lib
version: 1.0.0
type: library
description: Common templates for microservices
maintainers:
  - name: Platform Team
    email: platform@example.com
```

### templates/_util.tpl

```yaml
{{/*
Merge utility for template composition.
Usage: {{ include "common-lib.util.merge" (append . "common-lib.deployment.tpl") }}
*/}}
{{- define "common-lib.util.merge" -}}
{{- $top := first . -}}
{{- $overrides := fromYaml (include (index . 1) $top) | default (dict ) -}}
{{- $tpl := fromYaml (include (index . 2) $top) | default (dict ) -}}
{{- toYaml (merge $overrides $tpl) -}}
{{- end -}}
```

### templates/_deployment.tpl

```yaml
{{- define "common-lib.deployment.tpl" -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "common-lib.fullname" . }}
  labels:
    {{- include "common-lib.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount | default 1 }}
  selector:
    matchLabels:
      {{- include "common-lib.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "common-lib.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy | default "IfNotPresent" }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort | default 8080 }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
{{- end -}}

{{- define "common-lib.deployment" -}}
{{- include "common-lib.util.merge" (append . "common-lib.deployment.tpl") -}}
{{- end -}}
```

### Consumer Chart Usage

```yaml
# mychart/Chart.yaml
apiVersion: v2
name: myapp
version: 1.0.0
dependencies:
  - name: common-lib
    version: "1.x.x"
    repository: "https://charts.example.com"
```

```yaml
# mychart/templates/deployment.yaml
{{- include "common-lib.deployment" (list . "myapp.deployment") }}

{{- define "myapp.deployment" -}}
spec:
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          env:
            - name: APP_ENV
              value: {{ .Values.env | default "production" }}
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
{{- end -}}
```

---

## Hook Examples

### Database Migration Hook

```yaml
# templates/hooks/db-migrate.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "myapp.fullname" . }}-db-migrate"
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  backoffLimit: 3
  ttlSecondsAfterFinished: 300
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: migration
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command:
            - /bin/sh
            - -c
            - |
              echo "Running database migrations..."
              python manage.py migrate --noinput
              echo "Migrations completed."
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "myapp.fullname" . }}-secret
                  key: database-url
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

### Post-Install Notification Hook

```yaml
# templates/hooks/notify.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "myapp.fullname" . }}-notify"
  annotations:
    "helm.sh/hook": post-install,post-upgrade
    "helm.sh/hook-weight": "10"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  backoffLimit: 1
  ttlSecondsAfterFinished: 60
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: notify
          image: curlimages/curl:latest
          command:
            - /bin/sh
            - -c
            - |
              curl -X POST \
                -H "Content-Type: application/json" \
                -d '{"text": "{{ .Release.Name }} deployed to {{ .Release.Namespace }}"}' \
                {{ .Values.slackWebhookUrl }}
```

### Pre-Delete Cleanup Hook

```yaml
# templates/hooks/cleanup.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "myapp.fullname" . }}-cleanup"
  annotations:
    "helm.sh/hook": pre-delete
    "helm.sh/hook-weight": "0"
    "helm.sh/hook-delete-policy": hook-succeeded,hook-failed
spec:
  backoffLimit: 1
  template:
    spec:
      restartPolicy: Never
      serviceAccountName: {{ include "myapp.serviceAccountName" . }}
      containers:
        - name: cleanup
          image: bitnami/kubectl:latest
          command:
            - /bin/sh
            - -c
            - |
              echo "Cleaning up external resources..."
              # Delete PVCs if needed
              kubectl delete pvc -l app.kubernetes.io/instance={{ .Release.Name }} --ignore-not-found
              # Clean up external resources via API
              curl -X DELETE {{ .Values.externalResourceUrl }}/{{ .Release.Name }}
              echo "Cleanup completed."
```

---

## Test Examples

### Connection Test

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "myapp.fullname" . }}-test-connection"
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-delete-policy": before-hook-creation
spec:
  containers:
    - name: wget
      image: busybox:1.36
      command:
        - /bin/sh
        - -c
        - |
          echo "Testing connection to {{ include "myapp.fullname" . }}..."
          wget --spider --timeout=5 http://{{ include "myapp.fullname" . }}:{{ .Values.service.port }}/health
          echo "Connection test passed!"
  restartPolicy: Never
```

### Comprehensive API Test

```yaml
# templates/tests/test-api.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "myapp.fullname" . }}-test-api"
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "1"
spec:
  containers:
    - name: test
      image: curlimages/curl:latest
      command:
        - /bin/sh
        - -c
        - |
          set -e
          BASE_URL="http://{{ include "myapp.fullname" . }}:{{ .Values.service.port }}"

          echo "Test 1: Health endpoint"
          curl -sf "$BASE_URL/health" || exit 1

          echo "Test 2: Ready endpoint"
          curl -sf "$BASE_URL/ready" || exit 1

          echo "Test 3: API version"
          VERSION=$(curl -sf "$BASE_URL/api/version" | jq -r '.version')
          if [ "$VERSION" != "{{ .Chart.AppVersion }}" ]; then
            echo "Version mismatch: expected {{ .Chart.AppVersion }}, got $VERSION"
            exit 1
          fi

          echo "All tests passed!"
  restartPolicy: Never
```

### Database Connectivity Test

```yaml
# templates/tests/test-database.yaml
{{- if .Values.database.enabled }}
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "myapp.fullname" . }}-test-db"
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "2"
spec:
  containers:
    - name: test
      image: postgres:15-alpine
      command:
        - /bin/sh
        - -c
        - |
          echo "Testing database connection..."
          pg_isready -h {{ .Values.database.host }} -p {{ .Values.database.port }} -U {{ .Values.database.user }}
          echo "Database connection successful!"
      env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ include "myapp.fullname" . }}-secret
              key: db-password
  restartPolicy: Never
{{- end }}
```

---

## Umbrella Chart Example

### Directory Structure

```
platform/
  Chart.yaml
  values.yaml
  values-dev.yaml
  values-prod.yaml
  charts/
    api/
    worker/
    scheduler/
```

### Chart.yaml

```yaml
apiVersion: v2
name: platform
version: 2.0.0
appVersion: "2.0.0"
description: Platform umbrella chart
type: application

dependencies:
  - name: api
    version: "1.x.x"
    repository: "file://charts/api"

  - name: worker
    version: "1.x.x"
    repository: "file://charts/worker"
    condition: worker.enabled

  - name: scheduler
    version: "1.x.x"
    repository: "file://charts/scheduler"
    condition: scheduler.enabled

  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled

  - name: redis
    version: "17.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
```

### values.yaml

```yaml
global:
  imageRegistry: ""
  imagePullSecrets: []
  storageClass: ""

  # Shared configuration
  environment: production
  logLevel: info

  # Database connection (used by all components)
  database:
    host: "{{ .Release.Name }}-postgresql"
    port: 5432
    name: platform

  # Redis connection
  redis:
    host: "{{ .Release.Name }}-redis-master"
    port: 6379

# API component
api:
  replicaCount: 3
  image:
    repository: myregistry/platform-api
    tag: "2.0.0"
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
  ingress:
    enabled: true
    hosts:
      - host: api.example.com
        paths:
          - path: /
            pathType: Prefix

# Worker component
worker:
  enabled: true
  replicaCount: 2
  image:
    repository: myregistry/platform-worker
    tag: "2.0.0"
  resources:
    requests:
      cpu: 200m
      memory: 512Mi

# Scheduler component
scheduler:
  enabled: true
  replicaCount: 1
  image:
    repository: myregistry/platform-scheduler
    tag: "2.0.0"

# PostgreSQL subchart
postgresql:
  enabled: true
  auth:
    postgresPassword: ""
    database: platform
  primary:
    persistence:
      size: 20Gi

# Redis subchart
redis:
  enabled: true
  auth:
    enabled: false
  master:
    persistence:
      size: 5Gi
```

### values-dev.yaml

```yaml
global:
  environment: development
  logLevel: debug

api:
  replicaCount: 1
  ingress:
    enabled: false

worker:
  replicaCount: 1

scheduler:
  enabled: false

postgresql:
  primary:
    persistence:
      size: 1Gi

redis:
  master:
    persistence:
      size: 1Gi
```

### values-prod.yaml

```yaml
global:
  environment: production
  logLevel: warn
  imagePullSecrets:
    - name: registry-credentials

api:
  replicaCount: 5
  resources:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 2
      memory: 2Gi
  autoscaling:
    enabled: true
    minReplicas: 5
    maxReplicas: 20

worker:
  replicaCount: 10
  autoscaling:
    enabled: true
    minReplicas: 10
    maxReplicas: 50

postgresql:
  primary:
    persistence:
      size: 100Gi
  readReplicas:
    replicaCount: 2
```

---

## NOTES.txt Example

```
{{- $fullName := include "myapp.fullname" . -}}

================================================================================
  {{ .Chart.Name }} {{ .Chart.Version }} has been deployed!
================================================================================

{{- if .Values.ingress.enabled }}
Application URLs:
{{- range $host := .Values.ingress.hosts }}
  {{- range .paths }}
  - http{{ if $.Values.ingress.tls }}s{{ end }}://{{ $host.host }}{{ .path }}
  {{- end }}
{{- end }}
{{- else if contains "NodePort" .Values.service.type }}
Get the application URL:
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ $fullName }})
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
{{- else if contains "LoadBalancer" .Values.service.type }}
Get the application URL (may take a few minutes for the LoadBalancer IP):
  export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ $fullName }} --template "{{"{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"}}")
  echo http://$SERVICE_IP:{{ .Values.service.port }}
{{- else if contains "ClusterIP" .Values.service.type }}
Access the application via port-forward:
  kubectl --namespace {{ .Release.Namespace }} port-forward svc/{{ $fullName }} 8080:{{ .Values.service.port }}
  Then visit: http://localhost:8080
{{- end }}

Useful Commands:
  # Check deployment status
  kubectl --namespace {{ .Release.Namespace }} get pods -l "app.kubernetes.io/instance={{ .Release.Name }}"

  # View logs
  kubectl --namespace {{ .Release.Namespace }} logs -l "app.kubernetes.io/instance={{ .Release.Name }}" -f

  # Run tests
  helm test {{ .Release.Name }} --namespace {{ .Release.Namespace }}

{{- if .Values.postgresql.enabled }}

PostgreSQL Connection:
  Host: {{ .Release.Name }}-postgresql.{{ .Release.Namespace }}.svc.cluster.local
  Port: 5432
  Database: {{ .Values.postgresql.auth.database }}
{{- end }}

{{- if .Values.redis.enabled }}

Redis Connection:
  Host: {{ .Release.Name }}-redis-master.{{ .Release.Namespace }}.svc.cluster.local
  Port: 6379
{{- end }}
```
