# ArgoCD Implementation Checklist

## Installation

### Prerequisites

- [ ] Kubernetes cluster running (v1.24+)
- [ ] kubectl configured and connected
- [ ] Helm v3 installed
- [ ] Git repository for manifests created
- [ ] Domain for ArgoCD UI configured (optional)

### ArgoCD Installation

- [ ] Create argocd namespace
- [ ] Add Argo Helm repository
- [ ] Configure values.yaml with:
  - [ ] Domain/ingress settings
  - [ ] HA replicas (server: 2+, repo-server: 2+)
  - [ ] Authentication (SSO/OIDC/GitHub)
  - [ ] Notifications (Slack/Teams/Email)
  - [ ] Metrics enabled
- [ ] Install ArgoCD via Helm
- [ ] Verify all pods running
- [ ] Get initial admin password
- [ ] Configure ingress/load balancer

## Repository Setup

### GitOps Repository Structure

- [ ] Create dedicated GitOps repository
- [ ] Set up folder structure:
  - [ ] `apps/` for application manifests
  - [ ] `infrastructure/` for cluster components
  - [ ] `projects/` for AppProject definitions
- [ ] Configure Kustomize base/overlay structure
- [ ] Set up branch protection rules
- [ ] Configure repository credentials in ArgoCD

### Repository Best Practices

- [ ] Separate config from application source code
- [ ] Use folders (not branches) for environments
- [ ] Separate prod and staging repositories
- [ ] Enable PR reviews for changes
- [ ] Set up pre-commit validation (OPA/Conftest)

## Security Configuration

### RBAC Setup

- [ ] Disable default admin account (production)
- [ ] Configure SSO/OIDC integration
- [ ] Create AppProjects per team
- [ ] Define RBAC policies in projects
- [ ] Set up role bindings (developer, deployer, admin)
- [ ] Test access permissions

### Secrets Management

- [ ] Choose secrets solution:
  - [ ] External Secrets Operator
  - [ ] Sealed Secrets
  - [ ] Vault integration
- [ ] Configure secrets sync
- [ ] Verify secrets not in Git
- [ ] Test secret rotation

### Network Security

- [ ] Enable TLS for ArgoCD server
- [ ] Configure HTTPS for Git repositories
- [ ] Restrict cluster API access
- [ ] Set up network policies (optional)

## Application Configuration

### First Application

- [ ] Create Application manifest
- [ ] Configure source (repo, path, revision)
- [ ] Configure destination (cluster, namespace)
- [ ] Set sync policy (manual for production)
- [ ] Add health checks
- [ ] Deploy and verify

### Sync Policy Configuration

| Environment | Auto Sync | Self Heal | Prune |
|-------------|-----------|-----------|-------|
| Development | Yes | Yes | Yes |
| Staging | Yes | Yes | Yes |
| Production | No* | Yes | No** |

*Consider automated with sync windows
**Enable with PruneLast

- [ ] Configure sync options:
  - [ ] CreateNamespace=true
  - [ ] ServerSideApply=true
  - [ ] ApplyOutOfSyncOnly=true
  - [ ] PruneLast=true (if prune enabled)
- [ ] Configure retry policy
- [ ] Set up ignoreDifferences for managed fields

### ApplicationSets

- [ ] Identify patterns for multi-env deployment
- [ ] Create ApplicationSet for:
  - [ ] Multiple environments (Matrix generator)
  - [ ] Multiple services (Git directory generator)
  - [ ] Preview environments (PR generator)
- [ ] Configure appropriate sync strategies
- [ ] Test application generation

## Multi-Cluster Setup

### Cluster Registration

- [ ] Get cluster contexts (`kubectl config get-contexts`)
- [ ] Add clusters to ArgoCD (`argocd cluster add`)
- [ ] Verify cluster connectivity
- [ ] Configure cluster-specific secrets

### Multi-Cluster Architecture

- [ ] Decide: Hub-and-spoke vs distributed
- [ ] Configure ApplicationSets for multi-cluster
- [ ] Set up cluster-specific overlays
- [ ] Test cross-cluster deployments

### Scaling Considerations

- [ ] Enable controller sharding (if needed)
- [ ] Tune controller resources
- [ ] Configure repository caching
- [ ] Set appropriate refresh intervals

## Sync Waves and Hooks

### Deployment Ordering

- [ ] Define sync waves for dependencies:
  - [ ] -1: Namespaces, CRDs
  - [ ] 0: ConfigMaps, Secrets
  - [ ] 1: Deployments, Services
  - [ ] 2: Ingress, monitoring
- [ ] Add sync-wave annotations

### Hooks

- [ ] Configure PreSync hooks (migrations)
- [ ] Configure PostSync hooks (notifications)
- [ ] Configure SyncFail hooks (cleanup)
- [ ] Set hook delete policies

## Notifications

### Notification Setup

- [ ] Enable notifications controller
- [ ] Configure notification services:
  - [ ] Slack webhook
  - [ ] Microsoft Teams
  - [ ] Email SMTP
  - [ ] GitHub status
- [ ] Create notification templates
- [ ] Define triggers:
  - [ ] on-sync-succeeded
  - [ ] on-sync-failed
  - [ ] on-health-degraded
- [ ] Subscribe applications to notifications

## Monitoring and Observability

### Metrics

- [ ] Enable Prometheus metrics
- [ ] Deploy ServiceMonitor (if using Prometheus Operator)
- [ ] Import Grafana dashboards
- [ ] Set up alerts:
  - [ ] Sync failures
  - [ ] Health degradation
  - [ ] Resource quota

### Logging

- [ ] Configure log level
- [ ] Integrate with log aggregation (ELK/Loki)
- [ ] Set up audit logging

## Maintenance

### Sync Windows

- [ ] Define maintenance windows for production
- [ ] Configure deny windows (weekends, holidays)
- [ ] Test window enforcement

### Disaster Recovery

- [ ] Document backup procedure
- [ ] Export Application definitions
- [ ] Test restore process
- [ ] Document rollback procedures

### Upgrades

- [ ] Pin ArgoCD version
- [ ] Test upgrades in staging first
- [ ] Review changelog before upgrades
- [ ] Plan for CRD updates

## Progressive Delivery (Optional)

### Argo Rollouts Integration

- [ ] Install Argo Rollouts
- [ ] Configure Rollout resources
- [ ] Set up analysis templates
- [ ] Configure canary/blue-green strategy
- [ ] Integrate with monitoring for analysis

## Validation Checklist

### Post-Installation Tests

- [ ] Login to ArgoCD UI
- [ ] Create test application
- [ ] Verify sync works
- [ ] Verify health checks
- [ ] Test rollback
- [ ] Verify notifications
- [ ] Test RBAC restrictions

### Production Readiness

- [ ] HA configuration verified
- [ ] Secrets not in Git
- [ ] RBAC configured
- [ ] Notifications working
- [ ] Monitoring enabled
- [ ] Backup procedure documented
- [ ] Runbooks created
