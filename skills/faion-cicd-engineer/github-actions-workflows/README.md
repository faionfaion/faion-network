---
id: github-actions-workflows
name: "GitHub Actions Advanced Workflows"
domain: OPS
skill: faion-cicd-engineer
category: "devops"
version: "2.0.0"
updated: "2026-01-26"
---

# GitHub Actions Advanced Workflows

Comprehensive guide for CI/CD patterns, matrix builds, caching, artifacts, and deployment strategies.

## Overview

| Aspect | Description |
|--------|-------------|
| Purpose | Production-grade CI/CD pipelines |
| Scope | Build, test, deploy, release workflows |
| Complexity | Intermediate to Advanced |

## Contents

| File | Description |
|------|-------------|
| [README.md](README.md) | Overview and quick reference |
| [checklist.md](checklist.md) | Pre-flight and review checklists |
| [examples.md](examples.md) | Complete workflow examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for workflow generation |

## Key Concepts

### Workflow Types

| Type | Trigger | Use Case |
|------|---------|----------|
| CI | `push`, `pull_request` | Build, test, lint |
| CD | `push` to main | Deploy to environments |
| Release | `push` tags | Publish packages, create releases |
| Scheduled | `schedule` (cron) | Maintenance, security scans |
| Reusable | `workflow_call` | Shared logic across repos |
| Manual | `workflow_dispatch` | On-demand deployments |

### Matrix Strategy

Execute jobs across multiple configurations in parallel.

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [18, 20, 22]
    exclude:
      - os: windows-latest
        node: 18
    include:
      - os: ubuntu-latest
        node: 22
        experimental: true
  fail-fast: false
  max-parallel: 6
```

### Caching Strategy

| Cache Type | Key Pattern | Restore Keys |
|------------|-------------|--------------|
| npm | `${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}` | `${{ runner.os }}-node-` |
| pip | `${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}` | `${{ runner.os }}-pip-` |
| Go | `${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}` | `${{ runner.os }}-go-` |
| Docker | `type=gha` (buildx) | N/A |

### Artifacts vs Cache

| Feature | Cache | Artifacts |
|---------|-------|-----------|
| Purpose | Speed up builds | Store outputs |
| Retention | 7 days (default) | 90 days (configurable) |
| Scope | Same workflow | Cross-workflow |
| Use Case | Dependencies | Test reports, binaries |

### Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel redundant runs
```

### Environment Protection

| Environment | Approvals | Secrets | URL |
|-------------|-----------|---------|-----|
| staging | None | Staging secrets | staging.example.com |
| production | Required | Prod secrets | example.com |

## Best Practices

### Security

1. **Pin action versions to SHA** - Avoid tag/branch references
2. **Use OIDC for cloud auth** - No long-lived credentials
3. **Limit GITHUB_TOKEN permissions** - Principle of least privilege
4. **Audit third-party actions** - Review before using

### Performance

1. **Cache dependencies** - Use `actions/cache@v4`
2. **Use matrix builds** - Parallelize testing
3. **Enable concurrency** - Cancel redundant workflows
4. **Optimize checkout** - Use `fetch-depth: 1`

### Maintainability

1. **Create reusable workflows** - DRY principle
2. **Use composite actions** - Share steps across jobs
3. **Document workflows** - Add comments and descriptions
4. **Use consistent naming** - `ci.yml`, `cd.yml`, `release.yml`

## Action Versions (2026)

| Action | Version | Notes |
|--------|---------|-------|
| actions/checkout | v4 | Standard |
| actions/setup-node | v4 | Node.js setup |
| actions/cache | v4 | New cache service (Feb 2025) |
| docker/build-push-action | v6 | Multi-platform builds |
| docker/setup-buildx-action | v3 | Buildx setup |

## Related Files

- [checklist.md](checklist.md) - Implementation checklists
- [examples.md](examples.md) - Full workflow examples
- [templates.md](templates.md) - Quick-start templates
- [llm-prompts.md](llm-prompts.md) - AI-assisted generation

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [GitHub Actions Security Best Practices](https://www.stepsecurity.io/blog/github-actions-security-best-practices)
- [Matrix Builds with GitHub Actions](https://www.blacksmith.sh/blog/matrix-builds-with-github-actions)
- [GitHub Actions Caching](https://github.com/actions/cache)
- [CI/CD Best Practices](https://graphite.dev/guides/in-depth-guide-ci-cd-best-practices)
