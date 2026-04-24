# GitHub Actions Checklist

## Pre-Implementation

- [ ] Repository is hosted on GitHub
- [ ] `.github/workflows/` directory exists
- [ ] Required secrets configured in repository settings
- [ ] Branch protection rules defined

## Workflow Configuration

### Security (Critical)

- [ ] **Pin actions to full SHA** - Not `@main` or `@v1`, use `@a5ac77e...`
- [ ] **GITHUB_TOKEN minimal permissions** - Set `permissions:` block explicitly
- [ ] **Secrets in GitHub Secrets** - Never hardcode in YAML
- [ ] **Rotate secrets regularly** - Quarterly minimum
- [ ] **Audit third-party actions** - Review source before using
- [ ] **No secrets in logs** - Use `add-mask` for dynamic secrets

### Performance

- [ ] **Enable caching** - `actions/cache@v4` for dependencies
- [ ] **Use concurrency groups** - Prevent duplicate runs
- [ ] **Set job timeouts** - `timeout-minutes:` on each job
- [ ] **Matrix builds with fail-fast** - Consider `fail-fast: false` for coverage
- [ ] **Conditional jobs** - Use `if:` to skip unnecessary runs

### Structure

- [ ] **workflow_dispatch enabled** - For manual debugging
- [ ] **Clear job names** - Descriptive `name:` fields
- [ ] **Logical job dependencies** - Use `needs:` correctly
- [ ] **Environment variables** - Use `env:` at workflow level for shared values
- [ ] **Reusable workflows** - Extract common patterns

## CI Pipeline Checklist

- [ ] Lint job runs first
- [ ] Tests run with services (if needed)
- [ ] Build job depends on lint + test
- [ ] Coverage uploaded
- [ ] Security scan included
- [ ] Artifacts uploaded with retention

## CD Pipeline Checklist

- [ ] Environment protection rules set
- [ ] OIDC configured for cloud auth (no long-lived secrets)
- [ ] Deployment approval gates
- [ ] Rollback strategy documented
- [ ] Smoke tests after deployment
- [ ] Notifications configured

## Secrets Management

- [ ] Use repository secrets for repo-specific values
- [ ] Use organization secrets for shared values
- [ ] Use environment secrets for env-specific values
- [ ] OIDC for AWS/GCP/Azure (preferred over access keys)
- [ ] Document which secrets are needed in README

## Best Practices Compliance

| Practice | Status |
|----------|--------|
| Actions pinned to SHA | [ ] |
| Concurrency controls | [ ] |
| Caching enabled | [ ] |
| Timeouts set | [ ] |
| GITHUB_TOKEN scoped | [ ] |
| Secrets not hardcoded | [ ] |
| workflow_dispatch present | [ ] |
| Job outputs for cross-job data | [ ] |

## Common Issues Checklist

- [ ] **No unpinned actions** - `@main` or `@latest` is a security risk
- [ ] **No missing concurrency** - Parallel runs can cause conflicts
- [ ] **No hardcoded secrets** - Use `${{ secrets.* }}`
- [ ] **No missing caching** - Speeds up builds significantly
- [ ] **No ignored job outputs** - Data doesn't persist between jobs
- [ ] **No missing workflow_dispatch** - Can't debug without it

## Post-Implementation

- [ ] Workflows tested on feature branch
- [ ] PR checks pass consistently
- [ ] Build times acceptable (< 10 min for CI)
- [ ] Flaky tests addressed
- [ ] Team trained on workflow usage
- [ ] Documentation updated

---

*Checklist for GitHub Actions implementation*
