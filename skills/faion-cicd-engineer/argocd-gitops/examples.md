# ArgoCD GitOps Examples

## Installation

### Helm Installation

```bash
# Add Argo Helm repo
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Install with custom values
helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  -f values.yaml
```

### Production values.yaml

```yaml
global:
  domain: argocd.example.com

configs:
  cm:
    url: https://argocd.example.com
    admin.enabled: false
    dex.config: |
      connectors:
        - type: github
          id: github
          name: GitHub
          config:
            clientID: $dex.github.clientID
            clientSecret: $dex.github.clientSecret
            orgs:
              - name: myorg

  params:
    server.insecure: false
    application.namespaces: "*"

  rbac:
    policy.csv: |
      p, role:developer, applications, get, */*, allow
      p, role:developer, applications, sync, */staging/*, allow
      p, role:deployer, applications, *, */*, allow
      g, developers, role:developer
      g, deployers, role:deployer

  repositories:
    - url: https://github.com/myorg/kubernetes-manifests
      type: git

  credentialTemplates:
    github-https:
      url: https://github.com/myorg
      password: ${GITHUB_TOKEN}
      username: not-used

server:
  replicas: 2
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5

  ingress:
    enabled: true
    ingressClassName: nginx
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
      nginx.ingress.kubernetes.io/ssl-passthrough: "true"
      nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    hosts:
      - argocd.example.com
    tls:
      - secretName: argocd-tls
        hosts:
          - argocd.example.com

  metrics:
    enabled: true
    serviceMonitor:
      enabled: true

repoServer:
  replicas: 2
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5

controller:
  replicas: 1
  metrics:
    enabled: true
    serviceMonitor:
      enabled: true

applicationSet:
  enabled: true
  replicas: 2

notifications:
  enabled: true
  secret:
    items:
      slack-token: $SLACK_TOKEN
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
            "fields": [
              {"title": "Sync Status", "value": "{{.app.status.sync.status}}", "short": true},
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
    template.app-health-degraded: |
      slack:
        attachments: |
          [{
            "color": "warning",
            "title": "{{.app.metadata.name}} Health Degraded",
            "text": "Application health is {{.app.status.health.status}}"
          }]
```

## Application Definitions

### Basic Application with Kustomize

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-production
  namespace: argocd
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: deployments
    notifications.argoproj.io/subscribe.on-sync-failed.slack: deployments
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default

  source:
    repoURL: https://github.com/myorg/kubernetes-manifests
    targetRevision: main
    path: apps/myapp/overlays/production
    kustomize:
      images:
        - myapp=registry.example.com/myapp:v1.2.3

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
      - ServerSideApply=true
      - ApplyOutOfSyncOnly=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas

  revisionHistoryLimit: 10
```

### Application with Helm

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: redis-production
  namespace: argocd
spec:
  project: infrastructure

  source:
    repoURL: https://charts.bitnami.com/bitnami
    chart: redis
    targetRevision: 18.x
    helm:
      releaseName: redis
      valueFiles:
        - values.yaml
      values: |
        architecture: replication
        auth:
          enabled: true
          existingSecret: redis-secret
        replica:
          replicaCount: 3
        metrics:
          enabled: true
          serviceMonitor:
            enabled: true

  destination:
    server: https://kubernetes.default.svc
    namespace: redis

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Multi-Source Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-with-deps
  namespace: argocd
spec:
  project: default

  sources:
    - repoURL: https://charts.bitnami.com/bitnami
      chart: postgresql
      targetRevision: 13.x
      helm:
        releaseName: myapp-db
        valueFiles:
          - $values/apps/myapp/postgres-values.yaml
    - repoURL: https://github.com/myorg/kubernetes-manifests
      targetRevision: main
      ref: values
    - repoURL: https://github.com/myorg/kubernetes-manifests
      targetRevision: main
      path: apps/myapp/overlays/production

  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
```

## AppProject

### Team Project with RBAC

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-payments
  namespace: argocd
spec:
  description: Payments team applications

  sourceRepos:
    - 'https://github.com/myorg/payments-*'
    - 'https://charts.example.com'

  destinations:
    - namespace: 'payments-*'
      server: https://kubernetes.default.svc
    - namespace: 'payments-*'
      server: https://staging-cluster.example.com

  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
    - group: 'networking.k8s.io'
      kind: Ingress

  namespaceResourceBlacklist:
    - group: ''
      kind: ResourceQuota
    - group: ''
      kind: LimitRange

  roles:
    - name: developer
      description: Developer access
      policies:
        - p, proj:team-payments:developer, applications, get, team-payments/*, allow
        - p, proj:team-payments:developer, applications, sync, team-payments/*-staging, allow
      groups:
        - payments-developers

    - name: lead
      description: Tech lead access
      policies:
        - p, proj:team-payments:lead, applications, *, team-payments/*, allow
      groups:
        - payments-leads

  syncWindows:
    - kind: allow
      schedule: '0 9-17 * * 1-5'  # Weekdays 9am-5pm
      duration: 8h
      applications:
        - '*-production'
    - kind: deny
      schedule: '0 0 * * 6,0'  # Weekends
      duration: 48h
      applications:
        - '*-production'
```

## ApplicationSets

### Matrix Generator: Environments x Services

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: microservices
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          - list:
              elements:
                - env: staging
                  cluster: https://staging.k8s.example.com
                  values: values-staging.yaml
                - env: production
                  cluster: https://prod.k8s.example.com
                  values: values-production.yaml
          - git:
              repoURL: https://github.com/myorg/microservices
              revision: HEAD
              directories:
                - path: 'services/*'

  template:
    metadata:
      name: '{{path.basename}}-{{env}}'
      labels:
        app: '{{path.basename}}'
        env: '{{env}}'
    spec:
      project: microservices
      source:
        repoURL: https://github.com/myorg/microservices
        targetRevision: HEAD
        path: '{{path}}'
        helm:
          valueFiles:
            - '{{values}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### Pull Request Generator: Preview Environments

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: preview-environments
  namespace: argocd
spec:
  generators:
    - pullRequest:
        github:
          owner: myorg
          repo: myapp
          tokenRef:
            secretName: github-token
            key: token
          labels:
            - preview
        requeueAfterSeconds: 60

  template:
    metadata:
      name: 'preview-{{number}}'
      annotations:
        notifications.argoproj.io/subscribe.on-sync-succeeded.github: ""
    spec:
      project: previews
      source:
        repoURL: 'https://github.com/myorg/myapp'
        targetRevision: '{{head_sha}}'
        path: deploy/preview
        kustomize:
          nameSuffix: '-{{number}}'
          images:
            - 'myapp=ghcr.io/myorg/myapp:pr-{{number}}'
          commonAnnotations:
            pr-url: '{{head_url}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: 'preview-{{number}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true

  # Clean up when PR is closed/merged
  syncPolicy:
    preserveResourcesOnDeletion: false
```

### Cluster Generator: Multi-Cluster Deployment

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
  namespace: argocd
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production

  template:
    metadata:
      name: 'monitoring-{{name}}'
    spec:
      project: infrastructure
      source:
        repoURL: https://github.com/myorg/cluster-addons
        targetRevision: HEAD
        path: monitoring
        helm:
          valueFiles:
            - 'values-{{metadata.labels.region}}.yaml'
      destination:
        server: '{{server}}'
        namespace: monitoring
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Sync Waves and Hooks

### Ordered Deployment with Waves

```yaml
# Wave -1: Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
# Wave 0: ConfigMaps and Secrets
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "0"
data:
  config.yaml: |
    environment: production
---
# Wave 1: Database
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: myapp-db
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  # ...
---
# Wave 2: Application
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  # ...
```

### PreSync Hook: Database Migration

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myapp-migration
  namespace: myapp
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: migration
          image: registry.example.com/myapp:v1.2.3
          command: ['python', 'manage.py', 'migrate']
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
      restartPolicy: Never
  backoffLimit: 3
```

### PostSync Hook: Smoke Tests

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myapp-smoke-test
  namespace: myapp
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
              curl -f http://myapp:8000/health || exit 1
              echo "Smoke test passed"
      restartPolicy: Never
  backoffLimit: 1
```

## Repository Structure

### Recommended Layout

```
kubernetes-manifests/
├── apps/
│   └── myapp/
│       ├── base/
│       │   ├── kustomization.yaml
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── configmap.yaml
│       └── overlays/
│           ├── staging/
│           │   ├── kustomization.yaml
│           │   └── patch-replicas.yaml
│           └── production/
│               ├── kustomization.yaml
│               ├── patch-replicas.yaml
│               └── patch-resources.yaml
├── infrastructure/
│   ├── cert-manager/
│   ├── ingress-nginx/
│   └── external-secrets/
├── projects/
│   ├── team-a.yaml
│   └── team-b.yaml
└── applicationsets/
    ├── microservices.yaml
    └── preview-environments.yaml
```

### Kustomize Base

```yaml
# apps/myapp/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app.kubernetes.io/name: myapp
  app.kubernetes.io/managed-by: argocd

images:
  - name: myapp
    newName: registry.example.com/myapp
    newTag: latest
```

### Production Overlay

```yaml
# apps/myapp/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
  - ../../base

patches:
  - path: patch-replicas.yaml
  - path: patch-resources.yaml

images:
  - name: myapp
    newName: registry.example.com/myapp
    newTag: v1.2.3

configMapGenerator:
  - name: myapp-config
    behavior: merge
    literals:
      - LOG_LEVEL=info
      - ENVIRONMENT=production
```

---

*ArgoCD GitOps Examples | faion-cicd-engineer*
