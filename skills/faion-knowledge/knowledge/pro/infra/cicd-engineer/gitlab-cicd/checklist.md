# GitLab CI/CD Checklist

## Pipeline Setup

- [ ] `.gitlab-ci.yml` in repository root
- [ ] Workflow rules defined for branch/MR/tag triggers
- [ ] Default image and tags configured
- [ ] Stages defined in logical order

## Build Stage

- [ ] Build job uses appropriate base image
- [ ] Docker BuildKit enabled for layer caching
- [ ] Build artifacts defined with expiration
- [ ] Container registry login configured
- [ ] Multi-stage Docker builds for smaller images

## Test Stage

- [ ] Unit tests with coverage reporting
- [ ] Integration tests with service containers
- [ ] E2E tests (Playwright/Cypress)
- [ ] Lint and format checks
- [ ] Test reports in JUnit format
- [ ] Coverage reports in Cobertura format

## Security Stage

- [ ] SAST template included
- [ ] Dependency scanning enabled
- [ ] Container scanning for Docker images
- [ ] Secret detection active
- [ ] License compliance checks
- [ ] Trivy/Grype vulnerability scanning

## Caching

- [ ] Cache key based on lock files
- [ ] Cache policy (pull-push/pull) configured
- [ ] Cache paths for dependencies
- [ ] Fallback cache keys defined
- [ ] Distributed cache for runners (S3/GCS)

## Artifacts

- [ ] Build outputs as artifacts
- [ ] Test reports as artifacts
- [ ] Coverage reports as artifacts
- [ ] Expiration set (`expire_in`)
- [ ] `when: always` for debug artifacts

## Environments

- [ ] Staging environment defined
- [ ] Production environment defined
- [ ] Review apps for MRs
- [ ] Environment URLs configured
- [ ] Auto-stop for review environments
- [ ] Manual approval for production

## Deployment

- [ ] Kubernetes credentials secured
- [ ] Rolling deployment strategy
- [ ] Canary deployment (optional)
- [ ] Rollback capability
- [ ] Health checks after deploy
- [ ] Deployment notifications

## Security Configuration

- [ ] Protected branches configured
- [ ] Protected variables for secrets
- [ ] Masked variables enabled
- [ ] No secrets in `.gitlab-ci.yml`
- [ ] File-type variables for certificates

## Performance

- [ ] DAG with `needs` keyword
- [ ] Parallel jobs where possible
- [ ] `interruptible: true` for cancellable jobs
- [ ] `resource_group` for exclusive access
- [ ] Shallow clone for large repos

## Monitoring

- [ ] Pipeline notifications (Slack/email)
- [ ] Failed job alerts
- [ ] Deployment tracking
- [ ] DORA metrics configured
- [ ] Pipeline analytics reviewed

## Documentation

- [ ] Comments in `.gitlab-ci.yml`
- [ ] CI/CD variables documented
- [ ] Runbook for common issues
- [ ] Pipeline diagram updated

## Auto DevOps (Optional)

- [ ] Auto DevOps enabled
- [ ] Custom Dockerfile (if needed)
- [ ] Helm chart customization
- [ ] Ingress domain configured
- [ ] Database provisioning

## Common Issues Checklist

| Issue | Solution |
|-------|----------|
| Jobs run unexpectedly | Add workflow rules |
| Slow pipelines | Use `needs` for DAG |
| Cache misses | Check cache key strategy |
| Artifacts too large | Reduce paths, add expiration |
| Secrets in logs | Mark variables as masked |
| Flaky tests | Add retry with conditions |
| Review apps not cleaned | Use `auto_stop_in` |
| Runner capacity | Scale runners or use SaaS |
