# ArgoCD GitOps LLM Prompts

AI assistant prompts for ArgoCD GitOps tasks.

## Application Creation

### Create ArgoCD Application

```
Create an ArgoCD Application for:
- App name: {APP_NAME}
- Repository: {REPO_URL}
- Path: {PATH}
- Target namespace: {NAMESPACE}
- Environment: {staging|production}
- Manifest type: {Kustomize|Helm}
- Auto-sync: {yes|no}
- Prune: {yes|no}

Include:
- Finalizer for cascade deletion
- Notification annotations for Slack channel {CHANNEL}
- Retry policy with exponential backoff
- Sync options: CreateNamespace, ServerSideApply
```

### Create Helm-based Application

```
Create an ArgoCD Application for Helm chart:
- Release name: {RELEASE_NAME}
- Chart repository: {HELM_REPO}
- Chart name: {CHART_NAME}
- Chart version: {VERSION}
- Target namespace: {NAMESPACE}
- Values files: {values.yaml, values-prod.yaml}

Include inline values:
{INLINE_VALUES}
```

## ApplicationSet Creation

### Multi-Environment ApplicationSet

```
Create an ApplicationSet that deploys {APP_NAME} to multiple environments:
- Environments: staging, production
- Repository: {REPO_URL}
- Use list generator
- Different clusters per environment:
  - staging: https://staging.k8s.example.com
  - production: https://prod.k8s.example.com
- Path pattern: apps/{APP_NAME}/overlays/{{env}}
```

### Microservices ApplicationSet

```
Create an ApplicationSet for microservices discovery:
- Repository: {REPO_URL}
- Directory pattern: services/*
- Environment: {ENVIRONMENT}
- Each service gets its own namespace
- Use git directory generator
- Enable auto-sync with prune and self-heal
```

### Preview Environments ApplicationSet

```
Create an ApplicationSet for PR preview environments:
- GitHub org: {ORG}
- Repository: {REPO}
- Secret for GitHub token: github-token
- Only PRs with label: preview
- Namespace pattern: preview-{{number}}
- Image pattern: {REGISTRY}/{APP}:pr-{{number}}
- Auto-cleanup when PR closes
```

### Matrix ApplicationSet

```
Create a matrix ApplicationSet combining:
- Environments: {staging, production}
- Services discovered from: services/*
- Different clusters per environment
- Values file per environment: values-{{env}}.yaml
```

## AppProject Creation

### Team AppProject

```
Create an AppProject for team {TEAM_NAME}:
- Source repos: https://github.com/{ORG}/{TEAM_NAME}-*
- Allowed namespaces: {TEAM_NAME}-*
- Allowed cluster resources: Namespace, Ingress
- Roles:
  - developer: get, sync staging only
  - admin: full access
- OIDC groups: {TEAM_NAME}-developers, {TEAM_NAME}-admins
- Sync windows: deny weekends for production
```

## Sync Waves and Hooks

### Add Sync Waves

```
Add sync wave annotations to these resources for ordered deployment:
1. CRDs first (wave -2)
2. Namespace (wave -1)
3. ConfigMaps, Secrets (wave 0)
4. Database StatefulSet (wave 1)
5. Application Deployment (wave 2)
6. Services, Ingress (wave 3)

Resources:
{PASTE_RESOURCES_HERE}
```

### Create Migration Hook

```
Create a PreSync hook Job for database migration:
- Image: {REGISTRY}/{APP}:{VERSION}
- Command: {MIGRATION_COMMAND}
- Needs DATABASE_URL from secret {SECRET_NAME}
- Delete on success
- Backoff limit: 3
```

### Create Smoke Test Hook

```
Create a PostSync hook Job for smoke testing:
- Test endpoint: http://{SERVICE}:{PORT}/health
- Delete on success
- Timeout: 60 seconds
```

## Repository Structure

### Setup Kustomize Structure

```
Create Kustomize folder structure for {APP_NAME}:
- Base with: deployment, service, configmap
- Overlays: staging, production
- Production: 3 replicas, higher resources
- Staging: 1 replica, lower resources
- Common labels: app.kubernetes.io/name, managed-by: argocd
```

### Convert Raw YAML to Kustomize

```
Convert these raw Kubernetes manifests to Kustomize structure:
- Create base/ with common resources
- Create overlays/staging/ and overlays/production/
- Extract environment-specific values to patches
- Use image transformer for versioning

Manifests:
{PASTE_MANIFESTS_HERE}
```

## Troubleshooting

### Debug Sync Issues

```
My ArgoCD application {APP_NAME} is stuck in OutOfSync state.
Error message: {ERROR}

Current Application spec:
{PASTE_APP_SPEC}

Suggest:
1. Possible causes
2. ignoreDifferences rules if needed
3. Sync options to try
```

### Fix Health Check

```
Application {APP_NAME} shows Degraded health status.
Deployment is running but health check fails.

Current health assessment:
{PASTE_HEALTH_STATUS}

Suggest:
1. Custom health check configuration
2. Probe adjustments
3. Resource configurations
```

### Optimize Sync Performance

```
ArgoCD sync is slow for application {APP_NAME}.
- Repository size: {SIZE}
- Number of resources: {COUNT}
- Current sync time: {TIME}

Suggest optimizations for:
1. Repository structure
2. Sync options
3. Resource caching
4. Webhook configuration
```

## Migration

### Migrate from kubectl/CI Deploy

```
We currently deploy {APP_NAME} via CI pipeline using:
{PASTE_CI_CONFIG}

Convert to ArgoCD GitOps:
1. Create Application manifest
2. Repository structure for manifests
3. CI changes (only build/push, no deploy)
4. Image update strategy
```

### Migrate from Helm Release to ArgoCD

```
Convert Helm deployment to ArgoCD-managed:
Current helm install command:
{HELM_COMMAND}

values.yaml:
{PASTE_VALUES}

Create:
1. ArgoCD Application with Helm source
2. Recommended sync policy
3. Notification setup
```

## Security

### Setup RBAC

```
Configure ArgoCD RBAC for:
- Team: {TEAM_NAME}
- GitHub org: {ORG}
- Access levels:
  - Developers: read all, sync staging
  - Tech leads: sync all except prod
  - SRE: full access

Output:
1. AppProject with roles
2. Global RBAC policy (if needed)
3. OIDC group mappings
```

### Secrets Management

```
Setup external secrets for {APP_NAME}:
- Secret store: {AWS Secrets Manager|Vault|GCP Secret Manager}
- Secrets needed: {LIST}
- Target namespace: {NAMESPACE}

Create:
1. ExternalSecret resource
2. Sync wave annotation (before app)
3. Reference in deployment
```

## Notifications

### Setup Slack Notifications

```
Configure ArgoCD notifications for Slack:
- Channel: {CHANNEL}
- Events: sync-succeeded, sync-failed, health-degraded
- Include: app name, revision, health status, link to ArgoCD

Output notification config for values.yaml
```

### Setup GitHub Commit Status

```
Configure ArgoCD to update GitHub commit status:
- For preview environment ApplicationSet
- Mark commit as success/failure based on sync
- Link to ArgoCD application
```

## Multi-Cluster

### Add Remote Cluster

```
Setup ArgoCD to manage remote cluster:
- Cluster name: {NAME}
- Server URL: {URL}
- Authentication: {ServiceAccount|OIDC|AWS IAM}
- Labels: env={ENV}, region={REGION}

Provide:
1. Cluster secret manifest
2. Required RBAC in remote cluster
3. Network requirements
```

### Deploy to Multiple Clusters

```
Create ApplicationSet to deploy {APP_NAME} to all production clusters:
- Cluster selector: env=production
- Per-cluster values based on region label
- Staggered rollout (staging first, then prod clusters)
```

---

*ArgoCD GitOps LLM Prompts | faion-cicd-engineer*
