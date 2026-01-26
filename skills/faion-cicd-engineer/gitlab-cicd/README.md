# GitLab CI/CD

## Overview

GitLab CI/CD is an integrated continuous integration and delivery platform built into GitLab. It uses `.gitlab-ci.yml` to define pipelines with stages, jobs, and rules, supporting complex workflows, container registries, and Kubernetes integration.

## When to Use

- Projects hosted on GitLab (cloud or self-hosted)
- Organizations needing integrated DevSecOps platform
- Complex pipelines with parent-child relationships
- Projects requiring built-in container registry
- Teams using GitLab for project management

## Key Concepts

| Concept | Description |
|---------|-------------|
| Pipeline | Collection of jobs organized in stages |
| Stage | Group of jobs that run in parallel |
| Job | Individual task with script and configuration |
| Runner | Agent executing CI/CD jobs |
| Artifact | Files passed between jobs |
| Cache | Dependencies cached between pipelines |
| Environment | Deployment target with tracking |
| Rules | Conditional job execution |

## Pipeline Flow

```
Commit → Pipeline → Stages → Jobs → Artifacts → Deploy
         ↓
    ┌────────┬────────┬────────┬────────┐
    │ build  │  test  │  scan  │ deploy │
    ├────────┼────────┼────────┼────────┤
    │compile │ unit   │ sast   │staging │
    │docker  │ integ  │ dast   │ prod   │
    │        │ e2e    │secrets │        │
    └────────┴────────┴────────┴────────┘
```

## Best Practices (2025-2026)

### Pipeline Structure

1. **Use DAG with `needs` keyword** - Avoid sequential stages, create directed acyclic graph for parallelism
2. **Stageless pipelines** - Since GitLab 14.2, run all jobs in one stage with `needs`-based ordering
3. **Keep builds fast** - Target 10-minute builds (Martin Fowler guideline)
4. **Fail fast** - Quality checks should provide quick feedback

### Jobs

1. **Minimal commands per job** - Use appropriate Docker images instead of installing packages
2. **Dedicated runners** - Separate runners for build vs test to avoid resource contention
3. **Use job templates** - DRY with `extends` and YAML anchors
4. **Set retry policies** - Handle flaky tests with appropriate retry conditions

### Caching & Artifacts

1. **Cache dependencies** - Use cache for `node_modules`, `.npm`, `pip` packages
2. **Artifacts for build outputs** - Pass only necessary files between jobs
3. **Set expiration** - Use `expire_in` to clean up old artifacts
4. **Cache key strategy** - Key on lock files for dependency caching

### Security

1. **Protected variables** - Mark secrets as protected and masked
2. **Use HashiCorp Vault** - External secrets management
3. **Include security templates** - SAST, DAST, dependency scanning
4. **Immutable tags** - GitLab 18 artifact management features

### Environments

1. **Review apps** - Preview changes in merge requests
2. **Auto-stop environments** - Use `auto_stop_in` for cleanup
3. **Environment URLs** - Track deployments with proper URLs
4. **Canary deployments** - Gradual rollouts for production

## GitLab 18 Features (2025)

- Built-in artifact management with immutable tags
- Virtual registry for Maven
- Structured inputs for pipelines
- Enhanced parent/child pipeline management
- Improved pipeline execution optimization

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Pre-deployment checklist |
| [examples.md](examples.md) | Real-world pipeline examples |
| [templates.md](templates.md) | Reusable pipeline templates |
| [llm-prompts.md](llm-prompts.md) | AI-assisted CI/CD prompts |

## References

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [.gitlab-ci.yml Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [CI/CD Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)
- [GitLab Runner](https://docs.gitlab.com/runner/)
- [Auto DevOps](https://docs.gitlab.com/ee/topics/autodevops/)

## Sources

- [GitLab CI Best Practices](https://about.gitlab.com/topics/ci-cd/continuous-integration-best-practices/)
- [GitLab CI 10+ Best Practices](https://dev.to/zenika/gitlab-ci-10-best-practices-to-avoid-widespread-anti-patterns-2mb5)
- [Efficient CI/CD Pipelines](https://www.sakurasky.com/blog/gitlab-best-practices/)
- [GitLab CI/CD Mastery Guide](https://medium.com/@salwan.mohamed/the-complete-gitlab-ci-cd-mastery-guide-from-runners-to-production-part-2-3-749be8dc96e7)
- [7 GitLab CI/CD Best Practices](https://www.techcloudup.com/2025/04/7-gitlab-cicd-pipeline-best-practices.html)
- [GitLab 18 Updates](https://devops.com/gitlab-extends-scope-and-reach-of-core-ci-cd-platform-2/)
