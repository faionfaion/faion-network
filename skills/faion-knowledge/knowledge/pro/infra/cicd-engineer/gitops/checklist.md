# GitOps Implementation Checklist

## Pre-Implementation

- [ ] Current deployment process documented
- [ ] Git repository strategy defined (monorepo vs polyrepo)
- [ ] Environment strategy defined (folders, not branches)
- [ ] Tool selection completed (ArgoCD vs Flux)
- [ ] RBAC requirements identified
- [ ] Secret management strategy chosen

## Repository Setup

- [ ] GitOps repository created (separate from app code)
- [ ] Directory structure established
  - [ ] `/base` for shared configs
  - [ ] `/clusters/{env}` for environment-specific
  - [ ] `/infrastructure` for infra resources
- [ ] Branch protection rules configured
- [ ] PR review requirements set
- [ ] CI validation pipeline for manifests

## GitOps Operator Installation

### ArgoCD

- [ ] ArgoCD installed in cluster
- [ ] ArgoCD namespace configured
- [ ] Admin credentials secured
- [ ] SSO/OIDC configured (if required)
- [ ] RBAC policies defined
- [ ] Projects created for team isolation
- [ ] Repository credentials configured

### Flux

- [ ] Flux controllers installed
- [ ] Source controller configured
- [ ] Kustomize controller configured
- [ ] Helm controller configured (if needed)
- [ ] Notification controller configured
- [ ] Image automation configured (if needed)

## Application Onboarding

- [ ] Application manifests created (Kustomize or Helm)
- [ ] Application registered in GitOps operator
- [ ] Sync policy configured (auto/manual)
- [ ] Health checks defined
- [ ] Sync waves configured (if dependencies exist)
- [ ] Ignore differences configured (for generated fields)

## Multi-Environment Setup

- [ ] Dev environment configured
- [ ] Staging environment configured
- [ ] Production environment configured
- [ ] Environment promotion workflow defined
- [ ] Approval gates for production
- [ ] Rollback procedures documented

## Security

- [ ] Secrets not in plain text
- [ ] Secret management solution deployed
  - [ ] SOPS configured, OR
  - [ ] Sealed Secrets deployed, OR
  - [ ] External Secrets Operator configured
- [ ] Network policies applied
- [ ] Pod security policies/standards enforced
- [ ] RBAC least-privilege applied
- [ ] Audit logging enabled

## Progressive Delivery (Optional)

- [ ] Flagger or Argo Rollouts installed
- [ ] Canary strategy defined
- [ ] Analysis templates created
- [ ] Metrics provider configured (Prometheus)
- [ ] Rollback thresholds defined

## Monitoring & Observability

- [ ] GitOps operator metrics exposed
- [ ] Grafana dashboards deployed
- [ ] Alerts configured for sync failures
- [ ] Alerts configured for drift detection
- [ ] Notification channels set up (Slack, Teams)

## Disaster Recovery

- [ ] Backup strategy for GitOps operator
- [ ] Repository backup/mirror in place
- [ ] Recovery procedures documented
- [ ] Recovery testing scheduled

## Documentation & Training

- [ ] GitOps workflow documented
- [ ] Runbooks created for common operations
- [ ] Team trained on GitOps practices
- [ ] Troubleshooting guide created

## Post-Implementation Validation

- [ ] Drift detection working
- [ ] Auto-sync functioning correctly
- [ ] Manual sync tested
- [ ] Rollback procedure tested
- [ ] Environment promotion tested
- [ ] Audit trail verified
- [ ] Notification pipeline verified

## Compliance (If Required)

- [ ] Change management process integrated
- [ ] Audit requirements met
- [ ] Approval workflows documented
- [ ] Compliance reporting configured

---

*GitOps Checklist | faion-cicd-engineer*
