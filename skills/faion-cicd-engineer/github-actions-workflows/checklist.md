# GitHub Actions Workflows Checklist

## Pre-Implementation Checklist

### Repository Setup

- [ ] `.github/workflows/` directory exists
- [ ] Branch protection rules configured
- [ ] Required status checks defined
- [ ] Secrets configured in repository settings
- [ ] Environment protection rules set (staging, production)

### Security Review

- [ ] All actions pinned to SHA (not tags/branches)
- [ ] GITHUB_TOKEN permissions restricted to minimum
- [ ] Secrets never logged or exposed
- [ ] OIDC configured for cloud providers (AWS, GCP, Azure)
- [ ] No hardcoded credentials in workflows
- [ ] Third-party actions audited

### Performance Optimization

- [ ] Caching enabled for dependencies
- [ ] Matrix strategy used for parallel testing
- [ ] Concurrency configured to cancel redundant runs
- [ ] `fetch-depth: 1` for checkout (unless history needed)
- [ ] Conditional steps with `if:` to skip unnecessary work

## CI Workflow Checklist

### Build Job

- [ ] Checkout code
- [ ] Cache dependencies
- [ ] Install dependencies
- [ ] Run linter
- [ ] Run type checker (if applicable)
- [ ] Build application
- [ ] Upload build artifacts (if needed)

### Test Job

- [ ] Restore cached dependencies
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Generate coverage report
- [ ] Upload coverage to service (Codecov, etc.)
- [ ] Store test results as artifacts

### Matrix Testing

- [ ] Define OS matrix (ubuntu, windows, macos)
- [ ] Define language version matrix
- [ ] Use `exclude` for invalid combinations
- [ ] Use `include` for special configurations
- [ ] Set `fail-fast: false` for comprehensive results
- [ ] Limit `max-parallel` if needed

## CD Workflow Checklist

### Staging Deployment

- [ ] Environment configured with URL
- [ ] Deployment triggered only on main branch
- [ ] Docker image built and pushed
- [ ] Kubernetes/cloud deployment executed
- [ ] Health check performed
- [ ] Smoke tests run
- [ ] Notification on failure

### Production Deployment

- [ ] Manual approval required
- [ ] Staging deployment successful first
- [ ] Canary deployment (optional)
- [ ] Full deployment after validation
- [ ] Sentry/monitoring release created
- [ ] Success notification sent

## Release Workflow Checklist

### Version Tagging

- [ ] Triggered by version tags (v*)
- [ ] Changelog generated
- [ ] GitHub Release created
- [ ] Pre-release flag for alpha/beta/rc

### Package Publishing

- [ ] npm/PyPI/etc. publish configured
- [ ] Auth tokens available as secrets
- [ ] Version extracted from tag
- [ ] Package built and tested before publish

### Container Publishing

- [ ] Multi-platform builds (amd64, arm64)
- [ ] Image tagged with version
- [ ] Image tagged as `latest`
- [ ] Cache used for build layers

## Reusable Workflow Checklist

### Design

- [ ] Single responsibility (one task per workflow)
- [ ] Inputs clearly defined with descriptions
- [ ] Outputs defined for dependent workflows
- [ ] Secrets passed explicitly
- [ ] Default values provided where sensible

### Usage

- [ ] Called with `uses:` syntax
- [ ] Inputs passed via `with:`
- [ ] Secrets passed via `secrets:`
- [ ] Job dependencies defined with `needs:`

## Scheduled Workflow Checklist

### Configuration

- [ ] Cron expression validated
- [ ] Manual trigger available (`workflow_dispatch`)
- [ ] Runs at low-traffic times (UTC consideration)

### Tasks

- [ ] Security scans (Trivy, Dependabot)
- [ ] Artifact cleanup
- [ ] Database backups
- [ ] Stale PR/issue management
- [ ] Dependency updates

## Post-Implementation Review

### Functionality

- [ ] Workflow runs successfully on push
- [ ] Workflow runs successfully on PR
- [ ] Matrix jobs all pass
- [ ] Caching working (check logs)
- [ ] Artifacts uploaded correctly
- [ ] Deployments reach target environments

### Monitoring

- [ ] Notifications configured for failures
- [ ] Workflow duration acceptable
- [ ] No flaky tests causing failures
- [ ] Logs clean and informative

### Documentation

- [ ] Workflow commented inline
- [ ] README updated with CI/CD info
- [ ] Secrets documented (names, not values)
- [ ] Environment setup documented

## Troubleshooting Checklist

### Common Issues

| Issue | Check |
|-------|-------|
| Cache miss | Verify key pattern matches |
| Permission denied | Check GITHUB_TOKEN permissions |
| Secret unavailable | Verify secret exists and name correct |
| Action not found | Check action version and availability |
| Timeout | Increase timeout or optimize job |
| Concurrency issues | Review concurrency group settings |

### Debug Steps

1. Enable debug logging: Set `ACTIONS_RUNNER_DEBUG` secret to `true`
2. Review job logs in Actions tab
3. Check runner version compatibility
4. Validate YAML syntax with online validator
5. Test locally with `act` tool
