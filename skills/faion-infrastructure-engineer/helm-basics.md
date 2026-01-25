---
id: helm-basics
name: "Helm Basics"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Helm Basics

## Overview

Helm is the package manager for Kubernetes, enabling templating, versioning, and sharing of Kubernetes manifests. Charts bundle related resources into reusable, configurable packages with dependency management and release lifecycle control.

## When to Use

- Deploying complex applications with many Kubernetes resources
- Managing multiple environments (dev, staging, prod) with different configurations
- Creating reusable deployment packages
- Implementing GitOps workflows
- Sharing applications across teams or organizations

## Key Concepts

| Concept | Description |
|---------|-------------|
| Chart | Package containing Kubernetes resource templates |
| Release | Instance of a chart running in cluster |
| Values | Configuration parameters for customizing charts |
| Template | Go template files generating Kubernetes manifests |
| Repository | Collection of published charts |
| Hook | Actions at specific release lifecycle points |

### Chart Structure

```
mychart/
├── Chart.yaml          # Chart metadata
├── Chart.lock          # Dependency lock file
├── values.yaml         # Default configuration
├── values.schema.json  # JSON Schema for values validation
├── templates/          # Kubernetes manifest templates
│   ├── NOTES.txt       # Post-install notes
│   ├── _helpers.tpl    # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── tests/
│       └── test-connection.yaml
├── charts/             # Dependency charts
└── crds/               # Custom Resource Definitions
```

## Basic Files

### Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp application
type: application
version: 1.0.0
appVersion: "2.0.0"

keywords:
  - myapp
  - backend
  - api

home: https://github.com/example/myapp
sources:
  - https://github.com/example/myapp

maintainers:
  - name: DevOps Team
    email: devops@example.com
    url: https://example.com

dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled

annotations:
  artifacthub.io/changes: |
    - kind: added
      description: Initial release
  artifacthub.io/license: MIT
```

### values.yaml

```yaml
# Default values for myapp

# Global settings
global:
  imageRegistry: ""
  imagePullSecrets: []

# Replica configuration
replicaCount: 3

# Image configuration
image:
  repository: myapp
  tag: ""  # Defaults to Chart.appVersion
  pullPolicy: IfNotPresent

# Service account
serviceAccount:
  create: true
  annotations: {}
  name: ""

# Pod security context
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# Container security context
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8000
  annotations: {}

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

# Resource limits
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

# Autoscaling
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

# Probes
livenessProbe:
  httpGet:
    path: /health/live
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health/ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

startupProbe:
  httpGet:
    path: /health/live
    port: http
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 30

# Environment variables
env: []
  # - name: LOG_LEVEL
  #   value: info

# Environment from ConfigMap/Secret
envFrom: []
  # - configMapRef:
  #     name: myapp-config
  # - secretRef:
  #     name: myapp-secrets

# ConfigMap data
config:
  LOG_LEVEL: info
  DATABASE_HOST: postgresql
  REDIS_HOST: redis-master

# Secrets (use external secrets in production)
secrets: {}
  # DATABASE_PASSWORD: ""
  # SECRET_KEY: ""

# Persistence
persistence:
  enabled: false
  storageClass: ""
  accessMode: ReadWriteOnce
  size: 10Gi
  annotations: {}

# Node selection
nodeSelector: {}

# Tolerations
tolerations: []

# Affinity
affinity: {}

# Pod disruption budget
podDisruptionBudget:
  enabled: true
  minAvailable: 2
  # maxUnavailable: 1

# Network policy
networkPolicy:
  enabled: true

# PostgreSQL subchart
postgresql:
  enabled: true
  auth:
    username: myapp
    database: myapp
    existingSecret: myapp-postgresql
  primary:
    persistence:
      size: 20Gi

# Redis subchart
redis:
  enabled: true
  architecture: standalone
  auth:
    enabled: false
```

## Essential Commands

```bash
# Create new chart
helm create mychart

# Lint chart
helm lint ./mychart

# Template locally (dry-run)
helm template myrelease ./mychart -f values-prod.yaml

# Install chart
helm install myrelease ./mychart \
  --namespace myapp \
  --create-namespace \
  -f values-prod.yaml

# Upgrade release
helm upgrade myrelease ./mychart \
  --namespace myapp \
  -f values-prod.yaml \
  --atomic \
  --timeout 5m

# Install or upgrade
helm upgrade --install myrelease ./mychart \
  --namespace myapp \
  --create-namespace \
  -f values-prod.yaml

# Rollback
helm rollback myrelease 1 --namespace myapp

# List releases
helm list --namespace myapp

# Get release history
helm history myrelease --namespace myapp

# Uninstall
helm uninstall myrelease --namespace myapp

# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search charts
helm search repo postgresql

# Update dependencies
helm dependency update ./mychart

# Package chart
helm package ./mychart --version 1.0.0

# Push to OCI registry
helm push mychart-1.0.0.tgz oci://registry.example.com/charts
```

## Best Practices

1. **Use helpers** - Define reusable template functions in _helpers.tpl
2. **Validate values** - Create values.schema.json for input validation
3. **Set sensible defaults** - Make charts work out-of-box with minimal config
4. **Use conditions** - Enable/disable features with boolean flags
5. **Version properly** - Increment chart version for manifest changes, appVersion for app changes
6. **Document values** - Comment every value in values.yaml
7. **Include NOTES.txt** - Provide post-install instructions
8. **Test charts** - Include test pods in templates/tests/
9. **Use atomic upgrades** - Rollback automatically on failure
10. **Checksum configs** - Trigger pod restart on ConfigMap/Secret changes

## Common Pitfalls

1. **Hardcoded values in templates** - Always use values.yaml for configuration. Hardcoded values prevent customization.

2. **Missing resource limits** - Charts should always define default resource requests and limits.

3. **Not updating dependencies** - Forgetting `helm dependency update` leads to missing subcharts.

4. **Secrets in values** - Never commit secrets to values files. Use external secrets operators.

5. **Breaking schema changes** - Changing values structure breaks existing deployments. Use deprecation and migration paths.

6. **No atomic upgrades** - Without --atomic, failed upgrades leave partial releases. Always use --atomic.

## References

- [Helm Documentation](https://helm.sh/docs/)
- [Chart Development Guide](https://helm.sh/docs/topics/charts/)
- [Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Artifact Hub](https://artifacthub.io/)

## Sources

- [Helm Documentation](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Charts Guide](https://helm.sh/docs/topics/charts/)
- [Helm Template Guide](https://helm.sh/docs/chart_template_guide/)
- [Artifact Hub](https://artifacthub.io/)
