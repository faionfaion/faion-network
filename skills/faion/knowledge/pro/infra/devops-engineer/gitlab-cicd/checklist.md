# GitLab CI/CD Implementation Checklist

## Initial Setup

- [ ] Create `.gitlab-ci.yml` in repository root
- [ ] Define `stages:` in logical order (build, test, security, deploy, cleanup)
- [ ] Set `workflow: rules:` to control when pipelines run
- [ ] Configure `default:` settings (image, tags, retry, interruptible)

## Pipeline Structure

### Stages

- [ ] **build** - Compile, package, build Docker images
- [ ] **test** - Unit, integration, E2E tests
- [ ] **security** - SAST, DAST, dependency scanning, secret detection
- [ ] **deploy** - Staging, production deployments
- [ ] **cleanup** - Registry cleanup, environment cleanup

### Jobs

- [ ] Each job has clear `script:` section
- [ ] Jobs use `needs:` for DAG (parallel execution)
- [ ] Jobs use `rules:` for conditional execution
- [ ] Jobs have appropriate `artifacts:` and `cache:`
- [ ] Jobs are `interruptible: true` where appropriate

## Caching Configuration

- [ ] Cache key uses lockfile hash: `key: files: [package-lock.json]`
- [ ] Cache paths include dependency folders only
- [ ] Cache policy set appropriately (pull, push, pull-push)
- [ ] Branch isolation: `key: prefix: ${CI_COMMIT_REF_SLUG}`
- [ ] No compiled assets in cache (use artifacts instead)

### Cache Paths by Language

| Language | Cache Paths |
|----------|-------------|
| Node.js | `node_modules/`, `.npm/` |
| Python | `.venv/`, `.pip-cache/` |
| Go | `$GOPATH/pkg/mod/` |
| Java | `~/.m2/repository/`, `~/.gradle/` |
| Ruby | `vendor/bundle/` |
| PHP | `vendor/` |

## Artifacts Configuration

- [ ] Build artifacts passed to deploy jobs via `needs:`
- [ ] Artifacts have `expire_in:` set (1 day for temp, longer for releases)
- [ ] Test reports use `reports:` section (junit, cobertura)
- [ ] Artifacts are minimal (only necessary files)
- [ ] Coverage reports configured for MR display

### Artifact Types

| Type | Configuration |
|------|---------------|
| Build output | `paths: [dist/]` |
| JUnit report | `reports: junit: junit.xml` |
| Coverage | `reports: coverage_report: { format, path }` |
| SAST | `reports: sast: gl-sast-report.json` |

## Security Integration

- [ ] Include SAST template: `Security/SAST.gitlab-ci.yml`
- [ ] Include dependency scanning: `Security/Dependency-Scanning.gitlab-ci.yml`
- [ ] Include secret detection: `Security/Secret-Detection.gitlab-ci.yml`
- [ ] Include container scanning: `Security/Container-Scanning.gitlab-ci.yml`
- [ ] Variables marked as protected and masked
- [ ] No secrets in `.gitlab-ci.yml`

## Environments

- [ ] Staging environment defined with URL
- [ ] Production environment defined with URL
- [ ] Review apps configured for MRs
- [ ] Environment auto-stop configured: `auto_stop_in: 1 week`
- [ ] Stop jobs defined for cleanup: `on_stop:`

## Docker/Kubernetes Integration

- [ ] Docker-in-Docker (dind) service for builds
- [ ] BuildKit enabled: `DOCKER_BUILDKIT: 1`
- [ ] Registry authentication in `before_script:`
- [ ] Multi-stage builds for smaller images
- [ ] Image tagging strategy (commit SHA + latest)

## Rules Best Practices

- [ ] Use `workflow: rules:` for pipeline-level control
- [ ] Use `rules:` instead of `only/except`
- [ ] Combine conditions with `if:`, `changes:`, `exists:`
- [ ] Set variables per rule context
- [ ] Use `when: manual` for production deploys

### Common Rule Patterns

```yaml
# Run on default branch
- if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Run on merge requests
- if: $CI_MERGE_REQUEST_IID

# Run on tags
- if: $CI_COMMIT_TAG

# Run when specific files change
- changes:
    - "src/**/*"
    - "package.json"
```

## Performance Optimization

- [ ] Jobs use `needs:` to form DAG (skip stage waiting)
- [ ] Independent jobs run in parallel
- [ ] Large jobs split into smaller parallel jobs
- [ ] Tests parallelized with matrix or parallel keyword
- [ ] `GIT_DEPTH` set for large repositories

## Templates and DRY

- [ ] Common configurations in `.template` jobs
- [ ] Jobs use `extends:` for inheritance
- [ ] Shared configs in `include:` files
- [ ] Variables centralized at top level
- [ ] YAML anchors for repeated values

## Auto DevOps (Optional)

- [ ] Enable Auto DevOps if using default workflow
- [ ] Configure `KUBE_INGRESS_BASE_DOMAIN`
- [ ] Set staging/canary deployment options
- [ ] Configure database provisions if needed
- [ ] Customize with override jobs

## Monitoring and Notifications

- [ ] Pipeline failure notifications configured
- [ ] Slack/Teams integration for deployments
- [ ] MR comments for test results
- [ ] Coverage badges in README
- [ ] Pipeline badges in README

## Review Checklist

### Before Merge

- [ ] Pipeline passes on feature branch
- [ ] All tests green (unit, integration, E2E)
- [ ] Security scans pass (no critical issues)
- [ ] Code coverage meets threshold
- [ ] Review app deployed and verified

### Before Production Deploy

- [ ] Staging deployment successful
- [ ] Manual testing completed
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured
- [ ] Team notified of deployment

## Sources

- [GitLab CI/CD Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)
- [How to keep up with CI/CD best practices](https://about.gitlab.com/blog/how-to-keep-up-with-ci-cd-best-practices/)
- [Embracing Best Practices for Efficient CI/CD Pipelines](https://www.sakurasky.com/blog/gitlab-best-practices/)
