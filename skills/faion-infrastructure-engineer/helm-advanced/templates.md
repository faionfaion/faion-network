# Helm Advanced Templates

Copy-paste templates for library charts, hooks, tests, and umbrella charts.

## Library Chart Templates

### Chart.yaml (Library)

```yaml
apiVersion: v2
name: common-lib
version: 1.0.0
type: library
description: Shared templates for microservices
keywords:
  - library
  - common
  - templates
maintainers:
  - name: Platform Team
    email: platform@example.com
```

### _helpers.tpl (Standard)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "CHARTNAME.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "CHARTNAME.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "CHARTNAME.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels.
*/}}
{{- define "CHARTNAME.labels" -}}
helm.sh/chart: {{ include "CHARTNAME.chart" . }}
{{ include "CHARTNAME.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels.
*/}}
{{- define "CHARTNAME.selectorLabels" -}}
app.kubernetes.io/name: {{ include "CHARTNAME.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use.
*/}}
{{- define "CHARTNAME.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "CHARTNAME.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Return the proper image name.
*/}}
{{- define "CHARTNAME.image" -}}
{{- $registryName := .Values.global.imageRegistry | default "" -}}
{{- $repositoryName := .Values.image.repository -}}
{{- $tag := .Values.image.tag | default .Chart.AppVersion -}}
{{- if $registryName }}
{{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- else }}
{{- printf "%s:%s" $repositoryName $tag -}}
{{- end }}
{{- end }}
```

### _util.tpl (Merge Utility)

```yaml
{{/*
Merge utility for template inheritance.
Merges override template with base template.
Usage: {{ include "common-lib.util.merge" (append . "common-lib.deployment.tpl") }}
*/}}
{{- define "common-lib.util.merge" -}}
{{- $top := first . -}}
{{- $overrides := fromYaml (include (index . 1) $top) | default (dict ) -}}
{{- $tpl := fromYaml (include (index . 2) $top) | default (dict ) -}}
{{- toYaml (merge $overrides $tpl) -}}
{{- end -}}

{{/*
Deep merge with lists.
*/}}
{{- define "common-lib.util.deepMerge" -}}
{{- $dest := index . 0 -}}
{{- $source := index . 1 -}}
{{- range $key, $value := $source }}
  {{- if hasKey $dest $key }}
    {{- $destValue := index $dest $key -}}
    {{- if and (kindIs "map" $destValue) (kindIs "map" $value) }}
      {{- include "common-lib.util.deepMerge" (list $destValue $value) }}
    {{- else }}
      {{- $_ := set $dest $key $value -}}
    {{- end }}
  {{- else }}
    {{- $_ := set $dest $key $value -}}
  {{- end }}
{{- end }}
{{- toYaml $dest -}}
{{- end -}}
```

---

## Hook Templates

### Pre-Install/Upgrade Migration Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "CHARTNAME.fullname" . }}-migrate"
  labels:
    {{- include "CHARTNAME.labels" . | nindent 4 }}
    app.kubernetes.io/component: migration
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
        {{- include "CHARTNAME.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: migration
    spec:
      restartPolicy: Never
      {{- with .Values.global.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
        - name: migrate
          image: {{ include "CHARTNAME.image" . }}
          command: ["MIGRATION_COMMAND"]
          args: ["MIGRATION_ARGS"]
          env:
            {{- with .Values.env }}
            {{- toYaml . | nindent 12 }}
            {{- end }}
          envFrom:
            - secretRef:
                name: {{ include "CHARTNAME.fullname" . }}-secret
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

### Post-Install Notification Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "CHARTNAME.fullname" . }}-notify"
  labels:
    {{- include "CHARTNAME.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": post-install,post-upgrade
    "helm.sh/hook-weight": "10"
    "helm.sh/hook-delete-policy": hook-succeeded,hook-failed
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
                -d '{
                  "release": "{{ .Release.Name }}",
                  "namespace": "{{ .Release.Namespace }}",
                  "version": "{{ .Chart.Version }}",
                  "appVersion": "{{ .Chart.AppVersion }}"
                }' \
                {{ .Values.notifications.webhookUrl }}
```

### Pre-Delete Cleanup Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "CHARTNAME.fullname" . }}-cleanup"
  labels:
    {{- include "CHARTNAME.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-delete
    "helm.sh/hook-weight": "0"
    "helm.sh/hook-delete-policy": hook-succeeded,hook-failed
spec:
  backoffLimit: 1
  template:
    spec:
      restartPolicy: Never
      serviceAccountName: {{ include "CHARTNAME.serviceAccountName" . }}
      containers:
        - name: cleanup
          image: bitnami/kubectl:latest
          command:
            - /bin/sh
            - -c
            - |
              set -e
              echo "Starting cleanup for {{ .Release.Name }}..."

              # Delete PVCs
              kubectl delete pvc -l app.kubernetes.io/instance={{ .Release.Name }} \
                --namespace {{ .Release.Namespace }} --ignore-not-found

              # Clean up any finalizers if stuck
              # kubectl patch pvc <name> -p '{"metadata":{"finalizers":null}}'

              echo "Cleanup completed."
```

### Init Container Hook (Alternative Pattern)

```yaml
# templates/deployment.yaml (relevant section)
spec:
  template:
    spec:
      initContainers:
        - name: wait-for-db
          image: busybox:1.36
          command:
            - /bin/sh
            - -c
            - |
              until nc -z {{ .Values.database.host }} {{ .Values.database.port }}; do
                echo "Waiting for database..."
                sleep 2
              done
              echo "Database is available!"
        {{- if .Values.migrations.enabled }}
        - name: migrate
          image: {{ include "CHARTNAME.image" . }}
          command: ["python", "manage.py", "migrate", "--noinput"]
          envFrom:
            - secretRef:
                name: {{ include "CHARTNAME.fullname" . }}-secret
        {{- end }}
```

---

## Test Templates

### Basic Connection Test

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "CHARTNAME.fullname" . }}-test-connection"
  labels:
    {{- include "CHARTNAME.labels" . | nindent 4 }}
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
          set -e
          echo "Testing connection to {{ include "CHARTNAME.fullname" . }}:{{ .Values.service.port }}..."
          wget --spider --timeout=10 http://{{ include "CHARTNAME.fullname" . }}:{{ .Values.service.port }}/health
          echo "Connection test PASSED"
  restartPolicy: Never
```

### Comprehensive API Test

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "CHARTNAME.fullname" . }}-test-api"
  labels:
    {{- include "CHARTNAME.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": before-hook-creation
spec:
  containers:
    - name: test
      image: curlimages/curl:latest
      command:
        - /bin/sh
        - -c
        - |
          set -e
          BASE_URL="http://{{ include "CHARTNAME.fullname" . }}:{{ .Values.service.port }}"

          echo "=== Test 1: Health Check ==="
          HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health")
          if [ "$HTTP_CODE" != "200" ]; then
            echo "FAILED: Health check returned $HTTP_CODE"
            exit 1
          fi
          echo "PASSED: Health check returned 200"

          echo "=== Test 2: Ready Check ==="
          HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/ready")
          if [ "$HTTP_CODE" != "200" ]; then
            echo "FAILED: Ready check returned $HTTP_CODE"
            exit 1
          fi
          echo "PASSED: Ready check returned 200"

          echo "=== Test 3: API Version ==="
          RESPONSE=$(curl -sf "$BASE_URL/api/version")
          echo "API Response: $RESPONSE"

          echo ""
          echo "=== ALL TESTS PASSED ==="
  restartPolicy: Never
```

### Database Test

```yaml
{{- if .Values.database.testEnabled }}
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "CHARTNAME.fullname" . }}-test-db"
  labels:
    {{- include "CHARTNAME.labels" . | nindent 4 }}
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
          set -e
          echo "Testing PostgreSQL connection..."
          pg_isready \
            -h {{ .Values.database.host }} \
            -p {{ .Values.database.port | default 5432 }} \
            -U {{ .Values.database.user }}

          echo "Running test query..."
          psql -h {{ .Values.database.host }} \
               -p {{ .Values.database.port | default 5432 }} \
               -U {{ .Values.database.user }} \
               -d {{ .Values.database.name }} \
               -c "SELECT 1 as test;"

          echo "Database test PASSED"
      env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ include "CHARTNAME.fullname" . }}-secret
              key: database-password
  restartPolicy: Never
{{- end }}
```

### Redis Test

```yaml
{{- if .Values.redis.testEnabled }}
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "CHARTNAME.fullname" . }}-test-redis"
  labels:
    {{- include "CHARTNAME.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "3"
spec:
  containers:
    - name: test
      image: redis:7-alpine
      command:
        - /bin/sh
        - -c
        - |
          set -e
          echo "Testing Redis connection..."
          redis-cli -h {{ .Values.redis.host }} -p {{ .Values.redis.port | default 6379 }} ping

          echo "Testing Redis write/read..."
          redis-cli -h {{ .Values.redis.host }} SET helm-test-key "test-value"
          VALUE=$(redis-cli -h {{ .Values.redis.host }} GET helm-test-key)
          redis-cli -h {{ .Values.redis.host }} DEL helm-test-key

          if [ "$VALUE" = "test-value" ]; then
            echo "Redis test PASSED"
          else
            echo "Redis test FAILED: expected 'test-value', got '$VALUE'"
            exit 1
          fi
  restartPolicy: Never
{{- end }}
```

---

## Umbrella Chart Templates

### Chart.yaml (Umbrella)

```yaml
apiVersion: v2
name: platform
version: 1.0.0
appVersion: "1.0.0"
description: Platform umbrella chart
type: application
keywords:
  - platform
  - umbrella
maintainers:
  - name: Platform Team
    email: platform@example.com

dependencies:
  # Internal subcharts
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

  # External dependencies
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
    alias: db

  - name: redis
    version: "17.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
    alias: cache
```

### values.yaml (Umbrella)

```yaml
# Global values shared by all subcharts
global:
  imageRegistry: ""
  imagePullSecrets: []
  storageClass: ""

  # Application settings
  environment: production
  logLevel: info

  # Shared secrets reference
  existingSecret: ""

  # Database connection (for subcharts)
  database:
    host: ""
    port: 5432
    name: platform
    user: platform

  # Redis connection (for subcharts)
  redis:
    host: ""
    port: 6379

# API subchart values
api:
  enabled: true
  replicaCount: 2
  image:
    repository: myregistry/api
    tag: ""
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 80
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

# Worker subchart values
worker:
  enabled: true
  replicaCount: 1
  image:
    repository: myregistry/worker
    tag: ""
  resources:
    requests:
      cpu: 100m
      memory: 256Mi

# Scheduler subchart values
scheduler:
  enabled: false
  image:
    repository: myregistry/scheduler
    tag: ""

# PostgreSQL subchart values
postgresql:
  enabled: true
  auth:
    postgresPassword: ""
    database: platform
    username: platform
    password: ""
  primary:
    persistence:
      enabled: true
      size: 10Gi

# Redis subchart values
redis:
  enabled: true
  auth:
    enabled: false
  master:
    persistence:
      enabled: true
      size: 1Gi
```

### Environment Override (values-prod.yaml)

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
      cpu: 2000m
      memory: 2Gi
  autoscaling:
    enabled: true
    minReplicas: 5
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70

worker:
  replicaCount: 10
  autoscaling:
    enabled: true
    minReplicas: 10
    maxReplicas: 50

scheduler:
  enabled: true

postgresql:
  primary:
    persistence:
      size: 100Gi
  readReplicas:
    replicaCount: 2

redis:
  master:
    persistence:
      size: 10Gi
  replica:
    replicaCount: 3
```

---

## Advanced Helper Templates

### Image Pull Secret Generator

```yaml
{{/*
Generate docker-registry secret data.
*/}}
{{- define "CHARTNAME.imagePullSecret" }}
{{- $registry := .Values.imageCredentials.registry -}}
{{- $username := .Values.imageCredentials.username -}}
{{- $password := .Values.imageCredentials.password -}}
{{- printf "{\"auths\":{\"%s\":{\"username\":\"%s\",\"password\":\"%s\",\"auth\":\"%s\"}}}" $registry $username $password (printf "%s:%s" $username $password | b64enc) | b64enc }}
{{- end }}
```

### Checksum Annotations

```yaml
{{/*
Generate checksum annotations for config reload.
*/}}
{{- define "CHARTNAME.checksumAnnotations" -}}
checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
{{- if .Values.extraConfigMaps }}
checksum/extra-config: {{ .Values.extraConfigMaps | toYaml | sha256sum }}
{{- end }}
{{- end -}}
```

### Resource Requirements

```yaml
{{/*
Generate resource requirements with defaults.
*/}}
{{- define "CHARTNAME.resources" -}}
{{- $defaults := dict "requests" (dict "cpu" "100m" "memory" "128Mi") "limits" (dict "cpu" "500m" "memory" "512Mi") -}}
{{- $resources := .Values.resources | default dict -}}
{{- toYaml (merge $resources $defaults) -}}
{{- end -}}
```

### Pod Affinity Helper

```yaml
{{/*
Generate pod anti-affinity for HA.
*/}}
{{- define "CHARTNAME.podAntiAffinity" -}}
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            {{- include "CHARTNAME.selectorLabels" . | nindent 12 }}
        topologyKey: kubernetes.io/hostname
    - weight: 50
      podAffinityTerm:
        labelSelector:
          matchLabels:
            {{- include "CHARTNAME.selectorLabels" . | nindent 12 }}
        topologyKey: topology.kubernetes.io/zone
{{- end -}}
```
