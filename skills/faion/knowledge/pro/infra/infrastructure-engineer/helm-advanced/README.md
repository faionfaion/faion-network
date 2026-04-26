# Helm Advanced Patterns

Advanced Helm templating techniques including library charts, hooks, tests, umbrella charts, and production-ready patterns.

## Overview

| Topic | Description |
|-------|-------------|
| Library Charts | Reusable templates and functions shared across charts |
| Hooks | Lifecycle intervention points for pre/post operations |
| Tests | Job-based validation of deployed charts |
| Umbrella Charts | Multi-chart composition for complex applications |
| Template Helpers | Named templates and helper functions |

## Chart Types

| Type | Purpose | Deploys Resources |
|------|---------|-------------------|
| Application | Complete deployable solution | Yes |
| Library | Shared templates and definitions | No |
| Umbrella | Composition of multiple charts | Yes (via dependencies) |

## Library Charts

Library charts define reusable primitives shared across other charts.

### Characteristics

- Set `type: library` in Chart.yaml
- Cannot be installed standalone
- No release artifacts rendered
- Dependent charts access parent context

### Creating Library Chart

```bash
helm create mylibchart
rm -rf mylibchart/templates/*.yaml
rm mylibchart/values.yaml
```

**Chart.yaml:**
```yaml
apiVersion: v2
name: mylibchart
version: 0.1.0
type: library
description: Common templates for microservices
```

### Library Template Pattern

**templates/_configmap.tpl:**
```yaml
{{- define "mylibchart.configmap.tpl" -}}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mylibchart.fullname" . }}
  labels:
    {{- include "mylibchart.labels" . | nindent 4 }}
data: {}
{{- end -}}

{{- define "mylibchart.configmap" -}}
{{- include "mylibchart.util.merge" (append . "mylibchart.configmap.tpl") -}}
{{- end -}}
```

### Using as Dependency

```yaml
# Chart.yaml
dependencies:
  - name: mylibchart
    version: 0.1.0
    repository: file://../mylibchart
```

```bash
helm dependency update
```

## Hooks

Hooks execute at strategic points in release lifecycle.

### Hook Types

| Hook | Trigger Point |
|------|---------------|
| `pre-install` | After templates render, before resource creation |
| `post-install` | After all resources loaded into K8s |
| `pre-upgrade` | After templates render, before resource update |
| `post-upgrade` | After all resources upgraded |
| `pre-delete` | Before any resources deleted |
| `post-delete` | After all release resources deleted |
| `pre-rollback` | After templates render, before rollback |
| `post-rollback` | After all resources rolled back |
| `test` | When `helm test` invoked |

### Hook Annotations

```yaml
annotations:
  "helm.sh/hook": pre-install,pre-upgrade
  "helm.sh/hook-weight": "5"
  "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
```

### Deletion Policies

| Policy | Behavior |
|--------|----------|
| `before-hook-creation` | Delete previous before new hook (default) |
| `hook-succeeded` | Delete after successful execution |
| `hook-failed` | Delete if hook failed |

### Weight Ordering

- Weights sorted ascending (negative to positive)
- Default weight: 0
- Lower weight executes first

## Tests

Chart tests validate deployed releases.

### Test Structure

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
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "myapp.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

### Running Tests

```bash
helm install myrelease ./mychart
# Wait for pods to be ready
helm test myrelease
```

### Test Conventions

- Store in `templates/tests/` directory
- Exit code 0 = success
- Use `helm.sh/hook-weight` for ordering
- Add `tests/` to `.helmignore`

## Umbrella Charts

Umbrella charts compose multiple subcharts into single deployable unit.

### Structure

```
umbrella-chart/
  Chart.yaml
  values.yaml
  charts/
    frontend/
    backend/
    database/
```

### Dependencies

```yaml
# Chart.yaml
dependencies:
  - name: frontend
    version: "1.0.0"
    repository: "file://charts/frontend"
  - name: backend
    version: "1.0.0"
    repository: "file://charts/backend"
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

### Value Scoping

```yaml
# values.yaml
global:
  imageRegistry: myregistry.io
  imagePullSecrets:
    - name: regcred

frontend:
  replicaCount: 3

backend:
  replicaCount: 2

postgresql:
  enabled: true
  auth:
    postgresPassword: secret
```

### When to Use

| Use Case | Recommended |
|----------|-------------|
| Related components (app + DB + cache) | Yes |
| Shared deployment lifecycle | Yes |
| Deeply nested dependencies (3+ levels) | No |
| Independent release cycles needed | No |

## Template Helpers

### _helpers.tpl Patterns

```yaml
{{/*
Expand chart name.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Fully qualified app name.
*/}}
{{- define "myapp.fullname" -}}
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
Common labels.
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels.
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## Advanced Techniques

### Checksum for Config Changes

```yaml
annotations:
  checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
  checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
```

### Required Values

```yaml
{{ required "database.host is required" .Values.database.host }}
```

### Template Evaluation

```yaml
# Evaluate string as template
{{ tpl .Values.config.template . }}
```

### Resource Protection

```yaml
annotations:
  "helm.sh/resource-policy": keep
```

## Best Practices

| Practice | Description |
|----------|-------------|
| DRY | Use library charts for shared patterns |
| YAGNI | Avoid over-templatization |
| Versioning | Track chart and app versions independently |
| Testing | Validate with lint, template, and test hooks |
| Documentation | Include NOTES.txt for post-install guidance |

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Production examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompt patterns |

## References

- [Helm Library Charts](https://helm.sh/docs/topics/library_charts/)
- [Helm Hooks](https://helm.sh/docs/topics/charts_hooks/)
- [Helm Chart Tests](https://helm.sh/docs/topics/chart_tests/)
- [Chart Tips and Tricks](https://helm.sh/docs/howto/charts_tips_and_tricks/)
- [Best Practices Guide](https://helm.sh/docs/chart_best_practices/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Library chart design | opus | Architecture decision |
| Helm hooks implementation | sonnet | Hook pattern expertise |
| Umbrella chart composition | sonnet | Chart orchestration |
| Helm test framework setup | sonnet | Testing pattern |
