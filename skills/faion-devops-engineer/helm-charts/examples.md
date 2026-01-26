# Helm Charts Examples

Production-ready examples for Helm charts.

## Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp application
type: application
version: 1.0.0
appVersion: "2.0.0"
kubeVersion: ">=1.25.0"

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
  artifacthub.io/prerelease: "false"
```

## values.yaml

```yaml
# Default values for myapp
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

# -- Global settings shared across subcharts
global:
  imageRegistry: ""
  imagePullSecrets: []

# -- Number of replicas (ignored if autoscaling.enabled=true)
replicaCount: 3

# -- Image configuration
image:
  # -- Container image repository
  repository: myapp
  # -- Image tag (defaults to Chart.appVersion)
  tag: ""
  # -- Image pull policy
  pullPolicy: IfNotPresent

# -- Service account configuration
serviceAccount:
  # -- Create service account
  create: true
  # -- Annotations for service account
  annotations: {}
  # -- Service account name (auto-generated if empty)
  name: ""

# -- Pod security context
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault

# -- Container security context
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop:
      - ALL

# -- Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8000
  annotations: {}

# -- Ingress configuration
ingress:
  # -- Enable ingress
  enabled: true
  # -- Ingress class name
  className: nginx
  # -- Ingress annotations
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  # -- Ingress hosts
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  # -- TLS configuration
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

# -- Resource requests and limits
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

# -- Horizontal Pod Autoscaler configuration
autoscaling:
  # -- Enable HPA
  enabled: true
  # -- Minimum replicas
  minReplicas: 3
  # -- Maximum replicas
  maxReplicas: 10
  # -- Target CPU utilization percentage
  targetCPUUtilizationPercentage: 70
  # -- Target memory utilization percentage
  targetMemoryUtilizationPercentage: 80

# -- Liveness probe configuration
livenessProbe:
  httpGet:
    path: /health/live
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

# -- Readiness probe configuration
readinessProbe:
  httpGet:
    path: /health/ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

# -- Startup probe configuration (for slow-starting apps)
startupProbe:
  httpGet:
    path: /health/live
    port: http
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 30

# -- Environment variables
env: []
  # - name: LOG_LEVEL
  #   value: info

# -- Environment from ConfigMap/Secret
envFrom: []
  # - configMapRef:
  #     name: myapp-config
  # - secretRef:
  #     name: myapp-secrets

# -- ConfigMap data
config:
  LOG_LEVEL: info
  DATABASE_HOST: postgresql
  REDIS_HOST: redis-master

# -- Secrets (use external secrets in production!)
secrets: {}

# -- Persistence configuration
persistence:
  enabled: false
  storageClass: ""
  accessMode: ReadWriteOnce
  size: 10Gi
  annotations: {}

# -- Node selector
nodeSelector: {}

# -- Tolerations
tolerations: []

# -- Affinity configuration
affinity: {}

# -- Pod anti-affinity for HA
podAntiAffinity:
  # -- Enable pod anti-affinity
  enabled: true
  # -- Anti-affinity type: soft or hard
  type: soft

# -- Topology spread constraints
topologySpreadConstraints: []

# -- Pod Disruption Budget configuration
podDisruptionBudget:
  # -- Enable PDB
  enabled: true
  # -- Minimum available pods
  minAvailable: 2
  # maxUnavailable: 1

# -- Network Policy configuration
networkPolicy:
  # -- Enable network policy
  enabled: true
  # -- Ingress rules
  ingress: []
  # -- Egress rules
  egress: []

# -- PostgreSQL subchart configuration
postgresql:
  enabled: true
  auth:
    username: myapp
    database: myapp
    existingSecret: myapp-postgresql
  primary:
    persistence:
      size: 20Gi

# -- Redis subchart configuration
redis:
  enabled: true
  architecture: standalone
  auth:
    enabled: false
```

## Environment-Specific Values

### values-dev.yaml

```yaml
replicaCount: 1

autoscaling:
  enabled: false

resources:
  requests:
    cpu: 50m
    memory: 128Mi
  limits:
    cpu: 200m
    memory: 256Mi

ingress:
  hosts:
    - host: myapp-dev.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-dev-tls
      hosts:
        - myapp-dev.example.com

podDisruptionBudget:
  enabled: false

postgresql:
  primary:
    persistence:
      size: 5Gi
```

### values-prod.yaml

```yaml
replicaCount: 3

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20

resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi

ingress:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

podDisruptionBudget:
  enabled: true
  minAvailable: 2

podAntiAffinity:
  enabled: true
  type: hard

postgresql:
  primary:
    persistence:
      size: 100Gi
    resources:
      requests:
        cpu: 1000m
        memory: 2Gi
```

## values.schema.json

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["replicaCount", "image"],
  "properties": {
    "replicaCount": {
      "type": "integer",
      "minimum": 1,
      "description": "Number of replicas"
    },
    "image": {
      "type": "object",
      "required": ["repository"],
      "properties": {
        "repository": {
          "type": "string",
          "description": "Container image repository"
        },
        "tag": {
          "type": "string",
          "description": "Image tag"
        },
        "pullPolicy": {
          "type": "string",
          "enum": ["Always", "IfNotPresent", "Never"],
          "description": "Image pull policy"
        }
      }
    },
    "resources": {
      "type": "object",
      "properties": {
        "requests": {
          "type": "object",
          "properties": {
            "cpu": { "type": "string" },
            "memory": { "type": "string" }
          }
        },
        "limits": {
          "type": "object",
          "properties": {
            "cpu": { "type": "string" },
            "memory": { "type": "string" }
          }
        }
      }
    },
    "autoscaling": {
      "type": "object",
      "properties": {
        "enabled": { "type": "boolean" },
        "minReplicas": {
          "type": "integer",
          "minimum": 1
        },
        "maxReplicas": {
          "type": "integer",
          "minimum": 1
        }
      }
    }
  }
}
```
