# GitOps Templates

Copy-paste templates for common GitOps configurations.

## Repository Structure Templates

### Monorepo Initialization

```bash
#!/bin/bash
# Initialize GitOps monorepo structure

mkdir -p apps/{frontend,backend}/base
mkdir -p apps/{frontend,backend}/overlays/{staging,production}
mkdir -p infrastructure/{cert-manager,ingress-nginx,external-secrets}
mkdir -p clusters/{staging,production}
mkdir -p projects

# Create placeholder files
touch apps/frontend/base/{kustomization.yaml,deployment.yaml,service.yaml}
touch apps/frontend/overlays/staging/kustomization.yaml
touch apps/frontend/overlays/production/kustomization.yaml
touch infrastructure/cert-manager/kustomization.yaml
touch clusters/staging/kustomization.yaml
touch clusters/production/kustomization.yaml

echo "GitOps repository structure created"
```

### Base Kustomization Template

```yaml
# apps/{APP_NAME}/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app.kubernetes.io/name: APP_NAME
  app.kubernetes.io/managed-by: gitops

images:
  - name: APP_NAME
    newName: REGISTRY/APP_NAME
    newTag: latest
```

### Environment Overlay Template

```yaml
# apps/{APP_NAME}/overlays/{ENV}/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ENV_NAMESPACE

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

### Replicas Patch Template

```yaml
# apps/{APP_NAME}/overlays/{ENV}/patch-replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: APP_NAME
spec:
  replicas: REPLICA_COUNT
```

### Resources Patch Template

```yaml
# apps/{APP_NAME}/overlays/{ENV}/patch-resources.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: APP_NAME
spec:
  template:
    spec:
      containers:
        - name: APP_NAME
          resources:
            requests:
              cpu: CPU_REQUEST
              memory: MEMORY_REQUEST
            limits:
              cpu: CPU_LIMIT
              memory: MEMORY_LIMIT
```

## ArgoCD Templates

### Basic Application

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
    path: PATH_TO_MANIFESTS
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
    automated:
      selfHeal: true      # Auto-fix drift
      prune: false        # Manual prune
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

### Helm Application

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
        key1: value1
        key2: value2
  destination:
    server: https://kubernetes.default.svc
    namespace: TARGET_NAMESPACE
  syncPolicy:
    automated:
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Multi-Environment ApplicationSet

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
            selfHeal: "true"
          - env: production
            namespace: production
            autoSync: "false"
            selfHeal: "true"

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
          selfHeal: '{{selfHeal}}'
        syncOptions:
          - CreateNamespace=true
```

### Multi-Cluster ApplicationSet

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

### Git Directory ApplicationSet

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
          - path: 'apps/excluded-app'
            exclude: true

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

### PR Preview ApplicationSet

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

### AppProject Template

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

  syncWindows:
    - kind: allow
      schedule: '0 9-17 * * 1-5'
      duration: 8h
      applications:
        - '*'
    - kind: deny
      schedule: '0 0 * * 0,6'
      duration: 24h
      applications:
        - '*-production'
```

## Flux CD Templates

### GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: gitops-repo
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/ORG/REPO
  ref:
    branch: main
  secretRef:
    name: github-credentials
```

### Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: APP_NAME
  namespace: flux-system
spec:
  interval: 10m
  targetNamespace: TARGET_NAMESPACE
  sourceRef:
    kind: GitRepository
    name: gitops-repo
  path: ./PATH_TO_MANIFESTS
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: APP_NAME
      namespace: TARGET_NAMESPACE
```

### HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta2
kind: HelmRelease
metadata:
  name: APP_NAME
  namespace: flux-system
spec:
  interval: 10m
  chart:
    spec:
      chart: CHART_NAME
      version: CHART_VERSION
      sourceRef:
        kind: HelmRepository
        name: REPO_NAME
  targetNamespace: TARGET_NAMESPACE
  values:
    key1: value1
    key2: value2
```

## Progressive Delivery Templates

### Argo Rollouts Canary

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: APP_NAME
  namespace: NAMESPACE
spec:
  replicas: REPLICA_COUNT
  strategy:
    canary:
      canaryService: APP_NAME-canary
      stableService: APP_NAME-stable
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
      app: APP_NAME
  template:
    metadata:
      labels:
        app: APP_NAME
    spec:
      containers:
        - name: APP_NAME
          image: IMAGE:TAG
          ports:
            - containerPort: PORT
```

### Analysis Template

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= SUCCESS_THRESHOLD
      failureCondition: result[0] < FAILURE_THRESHOLD
      failureLimit: 3
      provider:
        prometheus:
          address: PROMETHEUS_URL
          query: |
            sum(rate(
              http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m]
            )) /
            sum(rate(
              http_requests_total{service="{{args.service-name}}"}[5m]
            ))
```

### Blue-Green Rollout

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: APP_NAME
  namespace: NAMESPACE
spec:
  replicas: REPLICA_COUNT
  strategy:
    blueGreen:
      activeService: APP_NAME-active
      previewService: APP_NAME-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 300
  selector:
    matchLabels:
      app: APP_NAME
  template:
    metadata:
      labels:
        app: APP_NAME
    spec:
      containers:
        - name: APP_NAME
          image: IMAGE:TAG
          ports:
            - containerPort: PORT
```

## Sync Wave Templates

```yaml
# Wave -1: Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: APP_NAMESPACE
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
# Wave 0: ConfigMaps/Secrets
apiVersion: v1
kind: ConfigMap
metadata:
  name: APP_NAME-config
  namespace: APP_NAMESPACE
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
  namespace: APP_NAMESPACE
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
  namespace: APP_NAMESPACE
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  # ...
---
# Wave 3: Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: APP_NAME
  namespace: APP_NAMESPACE
  annotations:
    argocd.argoproj.io/sync-wave: "3"
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
          image: IMAGE:TAG
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

## Secrets Management Templates

### External Secret

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: APP_NAME-secrets
  namespace: NAMESPACE
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: SECRET_STORE_NAME
    kind: ClusterSecretStore
  target:
    name: APP_NAME-secrets
    creationPolicy: Owner
  data:
    - secretKey: SECRET_KEY
      remoteRef:
        key: PATH/TO/SECRET
        property: PROPERTY_NAME
```

### ClusterSecretStore (Vault)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: VAULT_URL
      path: secret
      version: v2
      auth:
        kubernetes:
          mountPath: kubernetes
          role: external-secrets
          serviceAccountRef:
            name: external-secrets
            namespace: external-secrets
```

## CI/CD Integration Templates

### GitHub Actions Update Manifest

```yaml
name: Update GitOps Manifest

on:
  push:
    branches: [main]
    paths:
      - 'src/**'

jobs:
  update-manifest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and push image
        run: |
          docker build -t ${{ secrets.REGISTRY }}/APP_NAME:${{ github.sha }} .
          docker push ${{ secrets.REGISTRY }}/APP_NAME:${{ github.sha }}

      - name: Checkout GitOps repo
        uses: actions/checkout@v4
        with:
          repository: ORG/gitops-repo
          token: ${{ secrets.GH_TOKEN }}
          path: gitops

      - name: Update manifest
        run: |
          cd gitops/apps/APP_NAME/overlays/production
          kustomize edit set image APP_NAME=${{ secrets.REGISTRY }}/APP_NAME:${{ github.sha }}

      - name: Commit and push
        run: |
          cd gitops
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git commit -am "Update APP_NAME to ${{ github.sha }}"
          git push
```

### GitLab CI Update Manifest

```yaml
update-gitops:
  stage: deploy
  image: bitnami/git:latest
  script:
    - git clone https://oauth2:${GITOPS_TOKEN}@gitlab.com/org/gitops-repo.git
    - cd gitops-repo/apps/APP_NAME/overlays/production
    - |
      cat > kustomization.yaml << EOF
      apiVersion: kustomize.config.k8s.io/v1beta1
      kind: Kustomization
      resources:
        - ../../base
      images:
        - name: APP_NAME
          newName: ${CI_REGISTRY_IMAGE}
          newTag: ${CI_COMMIT_SHA}
      EOF
    - git config user.name "GitLab CI"
    - git config user.email "ci@gitlab.com"
    - git commit -am "Update APP_NAME to ${CI_COMMIT_SHA}"
    - git push
  only:
    - main
```
