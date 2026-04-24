# ArgoCD Templates

Copy-paste templates for common ArgoCD configurations.

## Application Templates

### Basic Kustomize Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: APP_NAME
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: REPO_URL
    targetRevision: main
    path: PATH_TO_KUSTOMIZE
  destination:
    server: https://kubernetes.default.svc
    namespace: TARGET_NAMESPACE
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Basic Helm Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: APP_NAME
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: HELM_REPO_URL
    chart: CHART_NAME
    targetRevision: CHART_VERSION
    helm:
      releaseName: RELEASE_NAME
      valuesObject:
        key: value
  destination:
    server: https://kubernetes.default.svc
    namespace: TARGET_NAMESPACE
  syncPolicy:
    automated:
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Production Application (Manual Sync)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: APP_NAME-production
  namespace: argocd
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: CHANNEL
    notifications.argoproj.io/subscribe.on-sync-failed.slack: CHANNEL
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: PROJECT_NAME
  source:
    repoURL: REPO_URL
    targetRevision: main
    path: apps/APP_NAME/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
      - ApplyOutOfSyncOnly=true
    retry:
      limit: 3
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 1m
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
  revisionHistoryLimit: 10
```

## AppProject Templates

### Team Project

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: TEAM_NAME
  namespace: argocd
spec:
  description: TEAM_NAME applications

  sourceRepos:
    - 'https://github.com/ORG/TEAM_NAME-*'

  destinations:
    - namespace: 'TEAM_NAME-*'
      server: https://kubernetes.default.svc

  clusterResourceWhitelist:
    - group: ''
      kind: Namespace

  roles:
    - name: developer
      description: Developer access
      policies:
        - p, proj:TEAM_NAME:developer, applications, get, TEAM_NAME/*, allow
        - p, proj:TEAM_NAME:developer, applications, sync, TEAM_NAME/*, allow
      groups:
        - TEAM_NAME-developers

    - name: admin
      description: Admin access
      policies:
        - p, proj:TEAM_NAME:admin, applications, *, TEAM_NAME/*, allow
      groups:
        - TEAM_NAME-admins
```

### Infrastructure Project

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: infrastructure
  namespace: argocd
spec:
  description: Cluster infrastructure components

  sourceRepos:
    - '*'

  destinations:
    - namespace: '*'
      server: https://kubernetes.default.svc

  clusterResourceWhitelist:
    - group: '*'
      kind: '*'

  namespaceResourceWhitelist:
    - group: '*'
      kind: '*'

  roles:
    - name: admin
      policies:
        - p, proj:infrastructure:admin, applications, *, infrastructure/*, allow
      groups:
        - platform-admins
```

## ApplicationSet Templates

### Multi-Environment (Staging + Production)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: APP_NAME-environments
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: staging
            namespace: staging
            autoSync: "true"
          - env: production
            namespace: production
            autoSync: "false"

  template:
    metadata:
      name: 'APP_NAME-{{env}}'
    spec:
      project: default
      source:
        repoURL: REPO_URL
        targetRevision: main
        path: 'apps/APP_NAME/overlays/{{env}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: '{{autoSync}}'
          selfHeal: '{{autoSync}}'
        syncOptions:
          - CreateNamespace=true
```

### Multi-Cluster Deployment

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: APP_NAME-clusters
  namespace: argocd
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production

  template:
    metadata:
      name: 'APP_NAME-{{name}}'
    spec:
      project: default
      source:
        repoURL: REPO_URL
        targetRevision: main
        path: apps/APP_NAME/overlays/production
        helm:
          values: |
            clusterName: {{name}}
      destination:
        server: '{{server}}'
        namespace: APP_NAMESPACE
      syncPolicy:
        automated:
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### Git Directory Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: apps-directory
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: REPO_URL
        revision: HEAD
        directories:
          - path: 'apps/*'

  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: REPO_URL
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          selfHeal: true
          prune: true
        syncOptions:
          - CreateNamespace=true
```

### PR Preview Environments

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: previews
  namespace: argocd
spec:
  generators:
    - pullRequest:
        github:
          owner: ORG_NAME
          repo: REPO_NAME
          tokenRef:
            secretName: github-token
            key: token
          labels:
            - preview
        requeueAfterSeconds: 60

  template:
    metadata:
      name: 'preview-{{number}}'
    spec:
      project: previews
      source:
        repoURL: 'https://github.com/ORG_NAME/REPO_NAME'
        targetRevision: '{{head_sha}}'
        path: deploy/preview
        kustomize:
          nameSuffix: '-{{number}}'
          images:
            - 'APP_IMAGE=REGISTRY/APP:pr-{{number}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: 'preview-{{number}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

## Kustomize Templates

### Base Kustomization

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app.kubernetes.io/name: APP_NAME
  app.kubernetes.io/managed-by: argocd

images:
  - name: APP_NAME
    newName: REGISTRY/APP_NAME
    newTag: latest
```

### Environment Overlay

```yaml
# overlays/ENV/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ENV

resources:
  - ../../base

patches:
  - path: patch-replicas.yaml
  - path: patch-resources.yaml

images:
  - name: APP_NAME
    newName: REGISTRY/APP_NAME
    newTag: VERSION

configMapGenerator:
  - name: APP_NAME-config
    behavior: merge
    literals:
      - LOG_LEVEL=info
      - ENVIRONMENT=ENV
```

## Sync Wave Templates

### Standard Wave Ordering

```yaml
# Wave -1: Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: APP_NAMESPACE
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
# Wave 0: ConfigMaps and Secrets
apiVersion: v1
kind: ConfigMap
metadata:
  name: APP_NAME-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"
data:
  KEY: VALUE
---
# Wave 1: Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: APP_NAME
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  # ...
---
# Wave 2: Service
apiVersion: v1
kind: Service
metadata:
  name: APP_NAME
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  # ...
```

## Hook Templates

### PreSync Migration Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: APP_NAME-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: migration
          image: REGISTRY/APP_NAME:VERSION
          command: ['MIGRATION_COMMAND']
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: APP_NAME-secrets
                  key: database-url
      restartPolicy: Never
  backoffLimit: 3
```

### PostSync Notification

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: notify-deployment
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: notify
          image: curlimages/curl:latest
          command:
            - /bin/sh
            - -c
            - |
              curl -X POST "$WEBHOOK_URL" \
                -H "Content-Type: application/json" \
                -d '{"text": "APP_NAME deployed successfully"}'
          env:
            - name: WEBHOOK_URL
              valueFrom:
                secretKeyRef:
                  name: notification-secrets
                  key: webhook-url
      restartPolicy: Never
  backoffLimit: 1
```

## Notification Templates

### Slack Notification Config

```yaml
# In ArgoCD ConfigMap or Helm values
notifications:
  notifiers:
    service.slack: |
      token: $slack-token

  triggers:
    trigger.on-sync-succeeded: |
      - send: [app-sync-succeeded]
        when: app.status.sync.status == 'Synced'
    trigger.on-sync-failed: |
      - send: [app-sync-failed]
        when: app.status.operationState.phase == 'Failed'
    trigger.on-health-degraded: |
      - send: [app-health-degraded]
        when: app.status.health.status == 'Degraded'

  templates:
    template.app-sync-succeeded: |
      slack:
        attachments: |
          [{
            "color": "good",
            "title": "{{.app.metadata.name}} Synced",
            "text": "Application synced successfully",
            "fields": [
              {"title": "Environment", "value": "{{.app.spec.destination.namespace}}", "short": true},
              {"title": "Revision", "value": "{{.app.status.sync.revision}}", "short": true}
            ]
          }]
    template.app-sync-failed: |
      slack:
        attachments: |
          [{
            "color": "danger",
            "title": "{{.app.metadata.name}} Sync Failed",
            "text": "{{.app.status.operationState.message}}"
          }]
```

## Cluster Registration

### Cluster Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: CLUSTER_NAME-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
    env: ENVIRONMENT
    region: REGION
type: Opaque
stringData:
  name: CLUSTER_NAME
  server: CLUSTER_API_URL
  config: |
    {
      "bearerToken": "SERVICE_ACCOUNT_TOKEN",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "BASE64_CA_CERT"
      }
    }
```

## Sync Window Template

```yaml
# In AppProject spec
syncWindows:
  # Allow sync during business hours on weekdays
  - kind: allow
    schedule: '0 9-17 * * 1-5'
    duration: 8h
    applications:
      - '*'
  # Deny sync on weekends
  - kind: deny
    schedule: '0 0 * * 0,6'
    duration: 24h
    applications:
      - '*-production'
  # Maintenance window
  - kind: deny
    schedule: '0 2 * * *'
    duration: 2h
    applications:
      - '*'
```
