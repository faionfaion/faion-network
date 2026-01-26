# GitOps Templates

## ArgoCD Templates

### Basic Application Template

```yaml
# templates/argocd/application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ APP_NAME }}
  namespace: argocd
  labels:
    team: {{ TEAM_NAME }}
    environment: {{ ENVIRONMENT }}
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: {{ PROJECT_NAME | default: "default" }}
  source:
    repoURL: {{ GIT_REPO_URL }}
    targetRevision: {{ GIT_BRANCH | default: "main" }}
    path: {{ MANIFEST_PATH }}
  destination:
    server: {{ CLUSTER_URL | default: "https://kubernetes.default.svc" }}
    namespace: {{ TARGET_NAMESPACE }}
  syncPolicy:
    automated:
      prune: {{ AUTO_PRUNE | default: true }}
      selfHeal: {{ SELF_HEAL | default: true }}
    syncOptions:
      - CreateNamespace=true
```

### Helm Application Template

```yaml
# templates/argocd/helm-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ APP_NAME }}
  namespace: argocd
spec:
  project: {{ PROJECT_NAME }}
  source:
    repoURL: {{ HELM_REPO_URL }}
    chart: {{ CHART_NAME }}
    targetRevision: {{ CHART_VERSION }}
    helm:
      releaseName: {{ RELEASE_NAME }}
      valueFiles:
        - values-{{ ENVIRONMENT }}.yaml
      parameters:
        - name: image.tag
          value: "{{ IMAGE_TAG }}"
  destination:
    server: {{ CLUSTER_URL }}
    namespace: {{ TARGET_NAMESPACE }}
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### ApplicationSet Template (Generator)

```yaml
# templates/argocd/applicationset-clusters.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: {{ APP_NAME }}-set
  namespace: argocd
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: {{ ENVIRONMENT }}
  template:
    metadata:
      name: '{{name}}-{{ APP_NAME }}'
      labels:
        environment: '{{metadata.labels.env}}'
    spec:
      project: {{ PROJECT_NAME }}
      source:
        repoURL: {{ GIT_REPO_URL }}
        targetRevision: {{ GIT_BRANCH }}
        path: 'clusters/{{name}}/{{ APP_NAME }}'
      destination:
        server: '{{server}}'
        namespace: {{ TARGET_NAMESPACE }}
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### Project Template

```yaml
# templates/argocd/project.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: {{ PROJECT_NAME }}
  namespace: argocd
spec:
  description: {{ PROJECT_DESCRIPTION }}
  sourceRepos:
    - '{{ SOURCE_REPO_PATTERN }}'
  destinations:
    - namespace: '{{ NAMESPACE_PATTERN }}'
      server: {{ CLUSTER_URL }}
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
  namespaceResourceBlacklist:
    - group: ''
      kind: ResourceQuota
  roles:
    - name: developer
      policies:
        - p, proj:{{ PROJECT_NAME }}:developer, applications, get, {{ PROJECT_NAME }}/*, allow
        - p, proj:{{ PROJECT_NAME }}:developer, applications, sync, {{ PROJECT_NAME }}/*, allow
      groups:
        - {{ DEVELOPER_GROUP }}
    - name: admin
      policies:
        - p, proj:{{ PROJECT_NAME }}:admin, applications, *, {{ PROJECT_NAME }}/*, allow
      groups:
        - {{ ADMIN_GROUP }}
```

## Flux Templates

### GitRepository Template

```yaml
# templates/flux/git-repository.yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: {{ REPO_NAME }}
  namespace: flux-system
spec:
  interval: {{ SYNC_INTERVAL | default: "1m" }}
  url: {{ GIT_REPO_URL }}
  ref:
    branch: {{ GIT_BRANCH | default: "main" }}
  secretRef:
    name: {{ GIT_SECRET_NAME }}
```

### Kustomization Template

```yaml
# templates/flux/kustomization.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: {{ APP_NAME }}
  namespace: flux-system
spec:
  interval: {{ RECONCILE_INTERVAL | default: "10m" }}
  targetNamespace: {{ TARGET_NAMESPACE }}
  sourceRef:
    kind: GitRepository
    name: {{ SOURCE_REPO_NAME }}
  path: {{ MANIFEST_PATH }}
  prune: {{ PRUNE | default: true }}
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: {{ APP_NAME }}
      namespace: {{ TARGET_NAMESPACE }}
  dependsOn:
    {{#each DEPENDENCIES}}
    - name: {{ this }}
    {{/each}}
```

### HelmRelease Template

```yaml
# templates/flux/helm-release.yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: {{ RELEASE_NAME }}
  namespace: {{ NAMESPACE }}
spec:
  interval: {{ RECONCILE_INTERVAL | default: "5m" }}
  chart:
    spec:
      chart: {{ CHART_NAME }}
      version: '{{ CHART_VERSION }}'
      sourceRef:
        kind: HelmRepository
        name: {{ HELM_REPO_NAME }}
        namespace: flux-system
  values:
    {{ VALUES | toYaml | indent 4 }}
  valuesFrom:
    - kind: ConfigMap
      name: {{ APP_NAME }}-values
      valuesKey: values.yaml
      optional: true
```

### ImagePolicy Template

```yaml
# templates/flux/image-policy.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: {{ APP_NAME }}
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: {{ APP_NAME }}
  policy:
    semver:
      range: '{{ SEMVER_RANGE | default: ">=1.0.0" }}'
```

## Kustomize Templates

### Base Kustomization

```yaml
# templates/kustomize/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - namespace.yaml
  - deployment.yaml
  - service.yaml
  - configmap.yaml
commonLabels:
  app: {{ APP_NAME }}
  managed-by: gitops
```

### Environment Overlay Template

```yaml
# templates/kustomize/overlays/{{ ENVIRONMENT }}/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: {{ APP_NAME }}-{{ ENVIRONMENT }}
resources:
  - ../../base
patches:
  - path: replica-patch.yaml
  - path: resources-patch.yaml
images:
  - name: {{ IMAGE_NAME }}
    newTag: {{ IMAGE_TAG }}
configMapGenerator:
  - name: {{ APP_NAME }}-config
    behavior: merge
    literals:
      - ENVIRONMENT={{ ENVIRONMENT }}
      - LOG_LEVEL={{ LOG_LEVEL }}
```

## Progressive Delivery Templates

### Flagger Canary Template

```yaml
# templates/flagger/canary.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: {{ APP_NAME }}
  namespace: {{ NAMESPACE }}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ APP_NAME }}
  progressDeadlineSeconds: {{ DEADLINE | default: 60 }}
  service:
    port: {{ SERVICE_PORT | default: 80 }}
    targetPort: {{ TARGET_PORT | default: 8080 }}
  analysis:
    interval: {{ ANALYSIS_INTERVAL | default: "30s" }}
    threshold: {{ FAILURE_THRESHOLD | default: 5 }}
    maxWeight: {{ MAX_WEIGHT | default: 50 }}
    stepWeight: {{ STEP_WEIGHT | default: 10 }}
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: {{ SUCCESS_RATE_MIN | default: 99 }}
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: {{ LATENCY_MAX_MS | default: 500 }}
        interval: 30s
```

### Argo Rollout Template

```yaml
# templates/argo-rollouts/rollout.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: {{ APP_NAME }}
  namespace: {{ NAMESPACE }}
spec:
  replicas: {{ REPLICAS }}
  selector:
    matchLabels:
      app: {{ APP_NAME }}
  template:
    metadata:
      labels:
        app: {{ APP_NAME }}
    spec:
      containers:
        - name: {{ APP_NAME }}
          image: {{ IMAGE }}:{{ TAG }}
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: { duration: 1m }
        - setWeight: 40
        - pause: { duration: 1m }
        - setWeight: 60
        - pause: { duration: 1m }
        - setWeight: 80
        - pause: { duration: 1m }
      trafficRouting:
        nginx:
          stableIngress: {{ APP_NAME }}-stable
```

## Secrets Management Templates

### SOPS Secret Template

```yaml
# templates/sops/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ SECRET_NAME }}
  namespace: {{ NAMESPACE }}
type: Opaque
stringData:
  {{ KEY_NAME }}: {{ VALUE | encrypt }}
```

### External Secrets Template

```yaml
# templates/external-secrets/external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ SECRET_NAME }}
  namespace: {{ NAMESPACE }}
spec:
  refreshInterval: {{ REFRESH_INTERVAL | default: "1h" }}
  secretStoreRef:
    kind: ClusterSecretStore
    name: {{ SECRET_STORE_NAME }}
  target:
    name: {{ SECRET_NAME }}
    creationPolicy: Owner
  data:
    {{#each SECRET_KEYS}}
    - secretKey: {{ this.localKey }}
      remoteRef:
        key: {{ this.remoteKey }}
        property: {{ this.property }}
    {{/each}}
```

## Notification Templates

### Slack Notification (Flux)

```yaml
# templates/flux/notification-provider.yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta1
kind: Provider
metadata:
  name: slack
  namespace: flux-system
spec:
  type: slack
  channel: {{ SLACK_CHANNEL }}
  secretRef:
    name: slack-webhook
---
apiVersion: notification.toolkit.fluxcd.io/v1beta1
kind: Alert
metadata:
  name: {{ APP_NAME }}-alerts
  namespace: flux-system
spec:
  providerRef:
    name: slack
  eventSeverity: {{ SEVERITY | default: "info" }}
  eventSources:
    - kind: Kustomization
      name: {{ APP_NAME }}
```

---

*GitOps Templates | faion-cicd-engineer*
