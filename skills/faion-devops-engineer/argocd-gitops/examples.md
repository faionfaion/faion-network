# ArgoCD GitOps Examples

## Installation

### Helm Installation

```bash
# Add Argo Helm repository
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Create namespace
kubectl create namespace argocd

# Install with custom values
helm install argocd argo/argo-cd \
  --namespace argocd \
  --version 7.7.0 \
  -f values.yaml

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### Production Helm Values

```yaml
# values.yaml
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
    - url: https://charts.example.com
      type: helm
      name: private-charts

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
        when: app.status.sync.status == 'OutOfSync' and time.Now().Sub(time.Parse(app.status.operationState.startedAt)).Minutes() > 5
    trigger.on-health-degraded: |
      - send: [app-health-degraded]
        when: app.status.health.status == 'Degraded'
  templates:
    template.app-sync-succeeded: |
      message: |
        Application {{.app.metadata.name}} synced successfully.
        Sync Status: {{.app.status.sync.status}}
        Health Status: {{.app.status.health.status}}
      slack:
        attachments: |
          [{
            "color": "good",
            "title": "{{.app.metadata.name}} Synced",
            "fields": [
              {"title": "Sync Status", "value": "{{.app.status.sync.status}}", "short": true},
              {"title": "Repository", "value": "{{.app.spec.source.repoURL}}", "short": true}
            ]
          }]
    template.app-sync-failed: |
      slack:
        attachments: |
          [{
            "color": "danger",
            "title": "{{.app.metadata.name}} Sync Failed",
            "text": "Application sync failed"
          }]
```

## Application Definitions

### Basic Application (Kustomize)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
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
        - myapp=registry.example.com/myapp:1.0.0

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
    - group: ""
      kind: ConfigMap
      jqPathExpressions:
        - .data["config.json"] | fromjson | del(.generatedAt)

  revisionHistoryLimit: 10
```

### Helm Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: prometheus
  namespace: argocd
spec:
  project: infrastructure

  source:
    repoURL: https://prometheus-community.github.io/helm-charts
    chart: kube-prometheus-stack
    targetRevision: 65.1.0
    helm:
      releaseName: prometheus
      valuesObject:
        grafana:
          enabled: true
          adminPassword: ${GRAFANA_PASSWORD}
        prometheus:
          prometheusSpec:
            retention: 15d
            storageSpec:
              volumeClaimTemplate:
                spec:
                  storageClassName: standard
                  resources:
                    requests:
                      storage: 50Gi

  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring

  syncPolicy:
    automated:
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
```

### Multi-Source Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-with-secrets
  namespace: argocd
spec:
  project: default

  sources:
    - repoURL: https://github.com/myorg/kubernetes-manifests
      targetRevision: main
      path: apps/myapp/overlays/production
      kustomize:
        images:
          - myapp=registry.example.com/myapp:1.0.0

    - repoURL: https://github.com/myorg/secrets
      targetRevision: main
      path: myapp/production
      ref: secrets

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

## AppProject

### Team Project with RBAC

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-backend
  namespace: argocd
spec:
  description: Backend team applications

  sourceRepos:
    - 'https://github.com/myorg/team-backend-*'
    - 'https://charts.example.com'

  destinations:
    - namespace: 'backend-*'
      server: https://kubernetes.default.svc
    - namespace: 'backend-*'
      server: https://staging.k8s.example.com

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
        - p, proj:team-backend:developer, applications, get, team-backend/*, allow
        - p, proj:team-backend:developer, applications, sync, team-backend/*, allow
      groups:
        - backend-developers

    - name: admin
      description: Admin access
      policies:
        - p, proj:team-backend:admin, applications, *, team-backend/*, allow
      groups:
        - backend-admins

  syncWindows:
    - kind: allow
      schedule: '0 * * * *'
      duration: 1h
      applications:
        - '*'
      namespaces:
        - 'backend-staging'
    - kind: deny
      schedule: '0 22 * * 5'
      duration: 48h
      applications:
        - '*-production'
```

## ApplicationSets

### Multi-Environment Matrix Generator

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

### Pull Request Preview Environments

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

### Cluster Generator for Multi-Cluster

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
      name: '{{name}}-addons'
    spec:
      project: infrastructure
      source:
        repoURL: https://github.com/myorg/cluster-addons
        targetRevision: HEAD
        path: addons
        helm:
          values: |
            clusterName: {{name}}
            clusterURL: {{server}}
      destination:
        server: '{{server}}'
        namespace: cluster-addons
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
  name: apps-from-directories
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/myorg/apps
        revision: HEAD
        directories:
          - path: apps/*
          - path: apps/excluded
            exclude: true

  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/apps
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

## Sync Waves and Hooks

### Ordered Deployment with Sync Waves

```yaml
# Wave -1: Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
# Wave 0: ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "0"
data:
  LOG_LEVEL: info
---
# Wave 1: Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: registry.example.com/myapp:1.0.0
          ports:
            - containerPort: 8000
---
# Wave 2: Service
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8000
```

### Database Migration Hook

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
          image: registry.example.com/myapp:1.0.0
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

### Post-Sync Notification Hook

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
              curl -X POST $WEBHOOK_URL \
                -H "Content-Type: application/json" \
                -d '{"text": "Deployment completed successfully"}'
          env:
            - name: WEBHOOK_URL
              valueFrom:
                secretKeyRef:
                  name: notification-secrets
                  key: webhook-url
      restartPolicy: Never
  backoffLimit: 1
```

## Kustomize Structure

### Base Configuration

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

```yaml
# apps/myapp/overlays/production/patch-replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
```

```yaml
# apps/myapp/overlays/production/patch-resources.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
        - name: myapp
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
```

## Multi-Cluster Management

### Adding a Cluster

```bash
# List available contexts
kubectl config get-contexts

# Add cluster to ArgoCD
argocd cluster add staging-context --name staging

# Add with labels for ApplicationSet selectors
argocd cluster add production-context --name production \
  --label env=production \
  --label region=us-east-1
```

### Cluster Secret (Declarative)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: production-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
    env: production
type: Opaque
stringData:
  name: production
  server: https://production.k8s.example.com
  config: |
    {
      "bearerToken": "<token>",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<base64-ca-cert>"
      }
    }
```

## Progressive Delivery with Argo Rollouts

### Rollout with Canary Strategy

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 5
  strategy:
    canary:
      canaryService: myapp-canary
      stableService: myapp-stable
      trafficRouting:
        nginx:
          stableIngress: myapp-ingress
      steps:
        - setWeight: 10
        - pause: {duration: 5m}
        - setWeight: 30
        - pause: {duration: 5m}
        - setWeight: 50
        - pause: {duration: 5m}
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: registry.example.com/myapp:1.0.0
          ports:
            - containerPort: 8000
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.95
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{app="myapp",status=~"2.."}[5m])) /
            sum(rate(http_requests_total{app="myapp"}[5m]))
```
