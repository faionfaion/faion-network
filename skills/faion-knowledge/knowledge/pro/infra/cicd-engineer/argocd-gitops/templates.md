# ArgoCD GitOps Templates

Copy-paste templates for common ArgoCD configurations.

## Application Templates

### Minimal Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: APP_NAME
  namespace: argocd
spec:
  project: default
  source:
    repoURL: REPO_URL
    targetRevision: main
    path: PATH_TO_MANIFESTS
  destination:
    server: https://kubernetes.default.svc
    namespace: TARGET_NAMESPACE
```

### Standard Application (Kustomize)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: APP_NAME
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
    path: apps/APP_NAME/overlays/ENVIRONMENT
    kustomize:
      images:
        - APP_NAME=REGISTRY/APP_NAME:VERSION

  destination:
    server: https://kubernetes.default.svc
    namespace: NAMESPACE

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
      - ApplyOutOfSyncOnly=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  revisionHistoryLimit: 10
```

### Standard Application (Helm)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: APP_NAME
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: PROJECT_NAME

  source:
    repoURL: HELM_REPO_URL
    chart: CHART_NAME
    targetRevision: CHART_VERSION
    helm:
      releaseName: RELEASE_NAME
      valueFiles:
        - values.yaml
        - values-ENVIRONMENT.yaml
      values: |
        # Inline values override
        key: value

  destination:
    server: https://kubernetes.default.svc
    namespace: NAMESPACE

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
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
    - 'https://charts.example.com'

  destinations:
    - namespace: 'TEAM_NAME-*'
      server: https://kubernetes.default.svc

  clusterResourceWhitelist:
    - group: ''
      kind: Namespace

  roles:
    - name: developer
      policies:
        - p, proj:TEAM_NAME:developer, applications, get, TEAM_NAME/*, allow
        - p, proj:TEAM_NAME:developer, applications, sync, TEAM_NAME/*-staging, allow
      groups:
        - TEAM_NAME-developers

    - name: admin
      policies:
        - p, proj:TEAM_NAME:admin, applications, *, TEAM_NAME/*, allow
      groups:
        - TEAM_NAME-admins

  syncWindows:
    - kind: deny
      schedule: '0 0 * * 6,0'
      duration: 48h
      applications:
        - '*-production'
```

## ApplicationSet Templates

### Multi-Environment (List Generator)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: APP_NAME
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: staging
            namespace: APP_NAME-staging
            cluster: https://kubernetes.default.svc
          - env: production
            namespace: APP_NAME-production
            cluster: https://kubernetes.default.svc

  template:
    metadata:
      name: 'APP_NAME-{{env}}'
    spec:
      project: PROJECT_NAME
      source:
        repoURL: REPO_URL
        targetRevision: main
        path: 'apps/APP_NAME/overlays/{{env}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### Microservices (Git Directory Generator)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: microservices-ENVIRONMENT
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: REPO_URL
        revision: HEAD
        directories:
          - path: 'services/*'

  template:
    metadata:
      name: '{{path.basename}}-ENVIRONMENT'
      labels:
        app: '{{path.basename}}'
        env: ENVIRONMENT
    spec:
      project: microservices
      source:
        repoURL: REPO_URL
        targetRevision: HEAD
        path: '{{path}}/overlays/ENVIRONMENT'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### Preview Environments (Pull Request Generator)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: APP_NAME-preview
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
            - 'APP_NAME=REGISTRY/APP_NAME:pr-{{number}}'
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

### Matrix Generator (Envs x Services)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: microservices-all
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          - list:
              elements:
                - env: staging
                  cluster: https://staging.k8s.example.com
                - env: production
                  cluster: https://prod.k8s.example.com
          - git:
              repoURL: REPO_URL
              revision: HEAD
              directories:
                - path: 'services/*'

  template:
    metadata:
      name: '{{path.basename}}-{{env}}'
    spec:
      project: microservices
      source:
        repoURL: REPO_URL
        targetRevision: HEAD
        path: '{{path}}/overlays/{{env}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Sync Wave Templates

### Standard Wave Order

```yaml
# Wave -2: CRDs
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
---
# Wave -1: Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: NAMESPACE
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
# Wave 0: ConfigMaps, Secrets, ServiceAccounts
apiVersion: v1
kind: ConfigMap
metadata:
  name: APP_NAME-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"
---
# Wave 1: PVCs, StatefulSets (databases)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: APP_NAME-db
  annotations:
    argocd.argoproj.io/sync-wave: "1"
---
# Wave 2: Deployments
apiVersion: apps/v1
kind: Deployment
metadata:
  name: APP_NAME
  annotations:
    argocd.argoproj.io/sync-wave: "2"
---
# Wave 3: Services, Ingress
apiVersion: v1
kind: Service
metadata:
  name: APP_NAME
  annotations:
    argocd.argoproj.io/sync-wave: "3"
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

### PostSync Smoke Test

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: APP_NAME-smoke-test
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: smoke-test
          image: curlimages/curl:latest
          command:
            - /bin/sh
            - -c
            - |
              curl -f http://APP_NAME:PORT/health || exit 1
              echo "Smoke test passed"
      restartPolicy: Never
  backoffLimit: 1
```

## Kustomize Templates

### Base kustomization.yaml

```yaml
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

### Overlay kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: NAMESPACE

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
      - ENVIRONMENT=ENVIRONMENT
```

## Notification Templates

### Slack Notification Config

```yaml
# In argocd-notifications-cm ConfigMap or Helm values
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
          "fields": [
            {"title": "Revision", "value": "{{.app.status.sync.revision | trunc 7}}", "short": true},
            {"title": "Health", "value": "{{.app.status.health.status}}", "short": true}
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

---

*ArgoCD GitOps Templates | faion-cicd-engineer*
