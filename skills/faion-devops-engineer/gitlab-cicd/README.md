---
id: gitlab-cicd
name: "GitLab CI/CD"
domain: OPS
skill: faion-devops-engineer
category: "ci-cd"
version: "2.0.0"
updated: "2026-01-26"
---

# GitLab CI/CD

## Overview

GitLab CI/CD is an integrated continuous integration and delivery platform built into GitLab. It uses a `.gitlab-ci.yml` file to define pipelines with stages, jobs, and rules, supporting complex workflows, container registries, and Kubernetes integration.

## When to Use

- Projects hosted on GitLab (cloud or self-hosted)
- Organizations needing integrated DevSecOps platform
- Complex pipelines with parent-child relationships
- Projects requiring built-in container registry
- Teams using GitLab for project management
- Monorepo architectures with multiple services

## Key Concepts

| Concept | Description |
|---------|-------------|
| Pipeline | Collection of jobs organized in stages |
| Stage | Group of jobs that run in parallel |
| Job | Individual task with script and configuration |
| Runner | Agent executing CI/CD jobs |
| Artifact | Files passed between jobs (guaranteed delivery) |
| Cache | Dependencies cached between pipelines (best-effort) |
| Environment | Deployment target with tracking |
| Rules | Conditional job execution (modern syntax) |
| DAG | Directed Acyclic Graph via `needs:` keyword |

## Pipeline Flow

```
Commit/MR → Pipeline Created → Stages Execute → Deploy
     ↓
  ┌──────────┬──────────┬──────────┬──────────┬──────────┐
  │  build   │   test   │   scan   │  deploy  │  cleanup │
  ├──────────┼──────────┼──────────┼──────────┼──────────┤
  │ compile  │ unit     │ sast     │ staging  │ registry │
  │ docker   │ integ    │ dast     │ prod     │ envs     │
  │          │ e2e      │ secrets  │          │          │
  └──────────┴──────────┴──────────┴──────────┴──────────┘
```

## Best Practices Summary (2025-2026)

### Pipeline Structure

1. **Keep stages few, jobs many** - Parallelization through jobs, not stages
2. **Use `needs:` for DAG** - Jobs start when dependencies ready, not stage order
3. **Use `rules:` over `only/except`** - Modern, flexible conditional execution
4. **Structure stages around risk** - What must you prove before deploy?
5. **Fail fast** - Run quick validations first

### Caching Strategy

1. **Cache package manager folders** - `node_modules/`, `.npm/`, `.gradle/`, `~/.m2`
2. **Use branch-scoped keys** - `key: ${CI_COMMIT_REF_SLUG}` prevents pollution
3. **Don't cache compiled assets** - Use artifacts for `dist/`, `build/`
4. **Use `policy: pull-push` intentionally** - Only when updating cache

### Artifacts Strategy

1. **Build once, deploy many** - Single artifact flows through pipeline
2. **Set expiration** - `expire_in: 1 day` for temporary artifacts
3. **Use dependencies explicitly** - `needs:` ensures artifact availability
4. **Keep artifacts small** - Only what downstream jobs need

### Security

1. **Use protected variables** - Mark secrets as protected and masked
2. **Include security templates** - SAST, DAST, dependency scanning
3. **Use environments** - Track deployments with URLs
4. **Implement review apps** - Preview changes safely

## Folder Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Complete pipeline examples |
| [templates.md](templates.md) | Reusable job templates |
| [llm-prompts.md](llm-prompts.md) | AI-assisted pipeline generation |

## Quick Commands

```bash
# Validate pipeline locally
gitlab-ci-lint .gitlab-ci.yml

# Simulate pipeline
gitlab-runner exec docker job-name

# Check pipeline status
glab ci status

# View pipeline logs
glab ci view
```

## References

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [.gitlab-ci.yml Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [CI/CD Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)
- [GitLab Runner](https://docs.gitlab.com/runner/)
- [Auto DevOps](https://docs.gitlab.com/ee/topics/autodevops/)

## Sources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [How to Write a GitLab CI/CD Pipeline From Scratch (2026 Edition)](https://thelinuxcode.com/how-to-write-a-gitlab-cicd-pipeline-from-scratch-2026-edition/)
- [GitLab CI: 10+ Best Practices to Avoid Widespread Anti-Patterns](https://dev.to/zenika/gitlab-ci-10-best-practices-to-avoid-widespread-anti-patterns-2mb5)
- [Building a Production-Grade GitLab CI/CD Pipeline](https://medium.com/@amit151993/building-a-production-grade-gitlab-ci-cd-pipeline-31d040cb66b3)
- [Optimizing GitLab Performance: Runners, Caching, and CI/CD Tips](https://www.mindfulchase.com/deep-dives/gitlab-proficiency-master-devops-workflows/optimizing-gitlab-performance-runners,-caching,-and-ci-cd-tips.html)
