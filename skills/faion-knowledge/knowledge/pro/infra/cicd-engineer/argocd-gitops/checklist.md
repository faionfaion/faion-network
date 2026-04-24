# ArgoCD GitOps Checklist

## Pre-Installation

- [ ] Kubernetes cluster running (1.25+)
- [ ] kubectl configured with cluster access
- [ ] Helm 3.x installed
- [ ] Git repository for GitOps config created
- [ ] DNS record for ArgoCD UI planned
- [ ] TLS certificate strategy defined (cert-manager recommended)

## Installation

- [ ] Create argocd namespace
- [ ] Add Argo Helm repository
- [ ] Configure values.yaml with:
  - [ ] Domain/ingress settings
  - [ ] HA configuration (replicas)
  - [ ] SSO/OIDC integration
  - [ ] Repository credentials
  - [ ] Notifications setup
- [ ] Install ArgoCD via Helm
- [ ] Verify all pods running
- [ ] Access UI and change admin password
- [ ] Configure CLI (`argocd login`)

## Repository Structure

- [ ] Separate GitOps repo from application code
- [ ] Use folder structure for environments:
  ```
  kubernetes-manifests/
  ├── apps/{app}/base/
  ├── apps/{app}/overlays/{env}/
  ├── infrastructure/
  └── projects/
  ```
- [ ] Choose Helm or Kustomize (no raw YAML)
- [ ] Configure repository credentials in ArgoCD

## Application Setup

- [ ] Create AppProject for team/tenant
- [ ] Define source repositories whitelist
- [ ] Define destination namespaces/clusters
- [ ] Configure RBAC roles in project
- [ ] Create Application resource with:
  - [ ] Source (repo, path, revision)
  - [ ] Destination (cluster, namespace)
  - [ ] Sync policy (automated/manual)
  - [ ] Health checks
  - [ ] Ignore differences (if needed)

## Sync Policy Configuration

- [ ] Decide automated vs manual sync
- [ ] Configure prune policy
- [ ] Enable self-heal (if automated)
- [ ] Set retry policy with backoff
- [ ] Configure sync options:
  - [ ] CreateNamespace
  - [ ] PrunePropagationPolicy
  - [ ] ServerSideApply (recommended)
  - [ ] ApplyOutOfSyncOnly

## ApplicationSets (Multi-Env/Cluster)

- [ ] Identify use case:
  - [ ] Multiple environments (staging, prod)
  - [ ] Multiple clusters
  - [ ] Multiple services (microservices)
  - [ ] Preview environments (PR-based)
- [ ] Choose generator type:
  - [ ] List (static environments)
  - [ ] Git (directory/file discovery)
  - [ ] Matrix (combinations)
  - [ ] Pull Request (preview envs)
  - [ ] Cluster (registered clusters)
- [ ] Define template with placeholders
- [ ] Test with single environment first

## Security

- [ ] Disable admin account after SSO setup
- [ ] Configure RBAC policies
- [ ] Use External Secrets or Sealed Secrets (never plain secrets in Git)
- [ ] Enable audit logging
- [ ] Configure network policies
- [ ] Scan manifests with KubeSec/Kubescan
- [ ] Scan container images with Trivy

## Sync Waves and Hooks

- [ ] Identify deployment order requirements
- [ ] Add sync-wave annotations (-1, 0, 1, ...)
- [ ] Configure hooks for:
  - [ ] PreSync (migrations, validations)
  - [ ] Sync (main deployment)
  - [ ] PostSync (tests, notifications)
  - [ ] SyncFail (rollback, alerts)
- [ ] Set hook-delete-policy

## Notifications

- [ ] Configure notification service (Slack, Teams, etc.)
- [ ] Set up triggers:
  - [ ] on-sync-succeeded
  - [ ] on-sync-failed
  - [ ] on-health-degraded
  - [ ] on-deployed (custom)
- [ ] Create message templates
- [ ] Subscribe applications to notifications
- [ ] Test notification delivery

## Sync Windows

- [ ] Define production maintenance windows
- [ ] Configure deny windows for:
  - [ ] Weekends
  - [ ] Holidays
  - [ ] Incident response periods
- [ ] Set allow windows for controlled times
- [ ] Apply to production applications only

## Monitoring and Observability

- [ ] Enable metrics endpoints
- [ ] Deploy ServiceMonitors (Prometheus)
- [ ] Create Grafana dashboards:
  - [ ] Sync status overview
  - [ ] Application health
  - [ ] Repo server performance
- [ ] Configure alerts for:
  - [ ] Sync failures
  - [ ] Health degradation
  - [ ] High reconciliation time

## CI/CD Integration

- [ ] Configure CI to update manifests (not deploy directly)
- [ ] Use image updater or Kustomize image patches
- [ ] Implement PR-based workflow for production
- [ ] Add validation in CI:
  - [ ] Manifest linting
  - [ ] Policy checks (OPA/Kyverno)
  - [ ] Security scanning
- [ ] Configure webhooks for faster sync

## Disaster Recovery

- [ ] Document ArgoCD configuration
- [ ] Backup ArgoCD resources (Applications, Projects)
- [ ] Test recovery procedure
- [ ] Define RTO/RPO for GitOps system

## Post-Deployment Validation

- [ ] All applications synced and healthy
- [ ] Notifications working
- [ ] RBAC tested with different users
- [ ] Sync windows enforced
- [ ] Metrics visible in monitoring
- [ ] Team trained on ArgoCD UI/CLI

---

*ArgoCD GitOps Checklist | faion-cicd-engineer*
