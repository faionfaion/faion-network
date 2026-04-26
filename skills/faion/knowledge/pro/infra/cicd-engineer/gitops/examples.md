# GitOps Examples

## Repository Structure Examples

### Example 1: Monorepo with Kustomize

```
gitops-config/
├── README.md
├── base/
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── overlays/
│   ├── dev/
│   │   ├── kustomization.yaml
│   │   ├── replica-patch.yaml
│   │   └── configmap-patch.yaml
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   ├── replica-patch.yaml
│   │   └── configmap-patch.yaml
│   └── production/
│       ├── kustomization.yaml
│       ├── replica-patch.yaml
│       ├── configmap-patch.yaml
│       └── hpa.yaml
└── infrastructure/
    ├── cert-manager/
    ├── ingress-nginx/
    └── monitoring/
```

### Example 2: Multi-Team Structure

```
platform-gitops/
├── clusters/
│   ├── production/
│   │   ├── flux-system/
│   │   └── tenants.yaml
│   └── staging/
│       ├── flux-system/
│       └── tenants.yaml
├── infrastructure/
│   ├── base/
│   │   ├── cert-manager/
│   │   ├── external-dns/
│   │   └── ingress-nginx/
│   ├── production/
│   └── staging/
└── tenants/
    ├── team-frontend/
    │   ├── base/
    │   ├── production/
    │   └── staging/
    └── team-backend/
        ├── base/
        ├── production/
        └── staging/
```

## ArgoCD Examples

### ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo.git
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### ArgoCD ApplicationSet (Multi-Cluster)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-app-set
  namespace: argocd
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production
  template:
    metadata:
      name: '{{name}}-my-app'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/gitops-repo.git
        targetRevision: main
        path: overlays/production
      destination:
        server: '{{server}}'
        namespace: my-app
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### ArgoCD Project with RBAC

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-frontend
  namespace: argocd
spec:
  description: Frontend team project
  sourceRepos:
    - 'https://github.com/org/frontend-*'
  destinations:
    - namespace: 'frontend-*'
      server: https://kubernetes.default.svc
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
  namespaceResourceBlacklist:
    - group: ''
      kind: ResourceQuota
    - group: ''
      kind: LimitRange
  roles:
    - name: developer
      description: Frontend developers
      policies:
        - p, proj:team-frontend:developer, applications, get, team-frontend/*, allow
        - p, proj:team-frontend:developer, applications, sync, team-frontend/*, allow
      groups:
        - frontend-team
```

## Flux Examples

### Flux GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: gitops-repo
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/gitops-repo.git
  ref:
    branch: main
  secretRef:
    name: github-credentials
```

### Flux Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 10m
  targetNamespace: my-app
  sourceRef:
    kind: GitRepository
    name: gitops-repo
  path: ./overlays/production
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: my-app
      namespace: my-app
  timeout: 2m
  dependsOn:
    - name: infrastructure
```

### Flux HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: nginx-ingress
  namespace: ingress-nginx
spec:
  interval: 5m
  chart:
    spec:
      chart: ingress-nginx
      version: '4.x'
      sourceRef:
        kind: HelmRepository
        name: ingress-nginx
        namespace: flux-system
  values:
    controller:
      replicaCount: 2
      service:
        type: LoadBalancer
```

## Kustomize Examples

### Base Deployment

```yaml
# base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: app
          image: my-app:latest
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

### Production Overlay

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: my-app-prod
resources:
  - ../../base
patches:
  - path: replica-patch.yaml
  - path: resources-patch.yaml
images:
  - name: my-app
    newTag: v1.2.3
configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - LOG_LEVEL=info
      - ENVIRONMENT=production
```

```yaml
# overlays/production/replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
```

## Progressive Delivery Example (Flagger)

### Canary with ArgoCD

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: my-app
  namespace: my-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  progressDeadlineSeconds: 60
  service:
    port: 80
    targetPort: 8080
  analysis:
    interval: 30s
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 30s
    webhooks:
      - name: load-test
        url: http://flagger-loadtester/
        timeout: 5s
        metadata:
          cmd: "hey -z 1m -q 10 -c 2 http://my-app-canary/"
```

## Secrets Management Example (SOPS)

### Encrypted Secret

```yaml
# secrets/production/db-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  username: ENC[AES256_GCM,data:abc123==,iv:xyz==,tag:def==]
  password: ENC[AES256_GCM,data:ghi456==,iv:uvw==,tag:jkl==]
sops:
  kms:
    - arn: arn:aws:kms:us-east-1:123456789:key/abc-def-ghi
  gcp_kms: []
  azure_kv: []
  lastmodified: '2025-01-15T10:00:00Z'
  mac: ENC[AES256_GCM,data:mac==,iv:maciv==,tag:mactag==]
  version: 3.7.3
```

---

*GitOps Examples | faion-cicd-engineer*
