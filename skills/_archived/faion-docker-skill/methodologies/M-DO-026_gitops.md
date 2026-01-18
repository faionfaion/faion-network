# M-DO-026: GitOps with ArgoCD

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Advanced
- **Tags:** #devops, #gitops, #argocd, #kubernetes, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Kubernetes configurations drift from desired state. Manual kubectl applies are error-prone. Rollbacks require finding previous manifests.

## Promise

After this methodology, you will manage Kubernetes declaratively with GitOps. Git becomes the source of truth, with automated sync and drift detection.

## Overview

GitOps uses Git as the single source of truth for infrastructure. ArgoCD watches Git repositories and syncs Kubernetes clusters automatically.

---

## Framework

### Step 1: ArgoCD Installation

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port forward to UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Install CLI
brew install argocd

# Login
argocd login localhost:8080
argocd account update-password
```

### Step 2: Repository Structure

```
gitops-repo/
├── apps/                    # Application definitions
│   ├── production/
│   │   ├── api.yaml
│   │   ├── web.yaml
│   │   └── workers.yaml
│   └── staging/
│       └── ...
├── base/                    # Base Kubernetes manifests
│   ├── api/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   └── web/
│       └── ...
├── overlays/                # Environment-specific patches
│   ├── production/
│   │   ├── api/
│   │   │   ├── kustomization.yaml
│   │   │   └── replicas-patch.yaml
│   │   └── ...
│   └── staging/
│       └── ...
└── projects/                # ArgoCD projects
    ├── production.yaml
    └── staging.yaml
```

### Step 3: Application Definition

```yaml
# apps/production/api.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api-production
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: production

  source:
    repoURL: https://github.com/org/gitops-repo.git
    targetRevision: main
    path: overlays/production/api

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
        - /spec/replicas  # Ignore HPA-managed replicas
```

### Step 4: Kustomize Base

```yaml
# base/api/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: api:latest
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
          envFrom:
            - configMapRef:
                name: api-config
            - secretRef:
                name: api-secrets
```

```yaml
# base/api/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app.kubernetes.io/name: api
  app.kubernetes.io/managed-by: argocd
```

### Step 5: Environment Overlays

```yaml
# overlays/production/api/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
  - ../../../base/api

images:
  - name: api
    newName: 123456789.dkr.ecr.us-east-1.amazonaws.com/api
    newTag: v1.2.3

replicas:
  - name: api
    count: 3

patches:
  - path: replicas-patch.yaml
  - path: resources-patch.yaml

configMapGenerator:
  - name: api-config
    behavior: merge
    literals:
      - NODE_ENV=production
      - LOG_LEVEL=info

secretGenerator:
  - name: api-secrets
    behavior: merge
    envs:
      - secrets.env
```

```yaml
# overlays/production/api/resources-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  template:
    spec:
      containers:
        - name: api
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
```

### Step 6: App of Apps Pattern

```yaml
# apps/production/apps.yaml (root application)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-apps
  namespace: argocd
spec:
  project: production
  source:
    repoURL: https://github.com/org/gitops-repo.git
    targetRevision: main
    path: apps/production
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```yaml
# apps/production/api.yaml (child application)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api-production
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "1"
spec:
  # ...
```

---

## Templates

### CI/CD Integration

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.build.outputs.tag }}
    steps:
      - uses: actions/checkout@v4

      - name: Build and push
        id: build
        run: |
          TAG="${GITHUB_SHA::8}"
          docker build -t $ECR_REPO:$TAG .
          docker push $ECR_REPO:$TAG
          echo "tag=$TAG" >> $GITHUB_OUTPUT

  update-gitops:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Checkout gitops repo
        uses: actions/checkout@v4
        with:
          repository: org/gitops-repo
          token: ${{ secrets.GITOPS_TOKEN }}

      - name: Update image tag
        run: |
          cd overlays/staging/api
          kustomize edit set image api=$ECR_REPO:${{ needs.build.outputs.image_tag }}

      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "Update api to ${{ needs.build.outputs.image_tag }}"
          git push
```

### Notifications

```yaml
# ArgoCD notifications config
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token
  template.app-deployed: |
    message: |
      Application {{.app.metadata.name}} is now {{.app.status.sync.status}}.
      Revision: {{.app.status.sync.revision}}
  trigger.on-deployed: |
    - when: app.status.operationState.phase in ['Succeeded']
      send: [app-deployed]
```

### Rollback

```bash
# View history
argocd app history api-production

# Rollback to specific revision
argocd app rollback api-production 3

# Or sync to specific git commit
argocd app sync api-production --revision abc123
```

---

## Common Mistakes

1. **Secrets in Git** - Use sealed-secrets or external-secrets
2. **No sync policies** - Manual sync defeats GitOps
3. **Too many repos** - Start with mono-repo
4. **No RBAC** - ArgoCD projects for isolation
5. **Ignoring drift** - Enable self-heal

---

## Checklist

- [ ] ArgoCD installed and configured
- [ ] Git repository structure defined
- [ ] Kustomize overlays for environments
- [ ] App of Apps pattern for management
- [ ] Automated sync enabled
- [ ] Self-heal enabled
- [ ] CI/CD updates GitOps repo
- [ ] Notifications configured

---

## Next Steps

- M-DO-005: Kubernetes Basics
- M-DO-006: Helm Charts
- M-DO-001: GitHub Actions

---

*Methodology M-DO-026 v1.0*
