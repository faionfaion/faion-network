---
id: github-actions-cicd
name: "GitHub Actions CI/CD"
domain: OPS
skill: faion-devops-engineer
category: "devops"
version: "2.0.0"
updated: "2026-01"
---

# GitHub Actions CI/CD

## Overview

GitHub Actions is a CI/CD platform integrated directly into GitHub repositories. It enables automated workflows triggered by events like pushes, pull requests, and releases, with support for matrix builds, reusable workflows, and extensive marketplace actions.

## When to Use

- Projects hosted on GitHub
- Open source projects needing free CI/CD
- Teams already using GitHub ecosystem
- Workflows requiring GitHub integration (issues, PRs, releases)
- Multi-platform builds (Linux, Windows, macOS)

## Key Concepts

| Concept | Description |
|---------|-------------|
| Workflow | Automated process defined in YAML |
| Job | Set of steps running on same runner |
| Step | Individual task (action or shell command) |
| Action | Reusable unit of code |
| Runner | Server executing workflows |
| Event | Trigger that starts workflow |
| Artifact | Files persisted between jobs |
| Secret | Encrypted environment variable |
| Reusable Workflow | Workflow callable from other workflows |
| Composite Action | Bundled steps as single action |

## Workflow Structure

```
.github/
├── workflows/
│   ├── ci.yml           # CI pipeline
│   ├── cd.yml           # CD pipeline
│   ├── release.yml      # Release workflow
│   └── scheduled.yml    # Scheduled tasks
├── actions/
│   └── custom-action/   # Custom composite action
│       └── action.yml
└── CODEOWNERS           # Code review assignments
```

## 2025-2026 Platform Updates

| Feature | Status | Notes |
|---------|--------|-------|
| Nested reusable workflows | Available | Up to 10 levels, 50 total |
| Timezone in schedules | Q1 2026 | Schedule reliability improved |
| Parallel steps | Mid-2026 | Most requested feature |
| OIDC authentication | Stable | Credentialless cloud auth |

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Security and best practices checklist |
| [examples.md](examples.md) | Complete workflow examples |
| [templates.md](templates.md) | Copy-paste workflow templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for generating workflows |

## Quick Reference

### Trigger Events

| Event | Use Case |
|-------|----------|
| `push` | On code push to branches |
| `pull_request` | On PR open/update |
| `workflow_dispatch` | Manual trigger |
| `schedule` | Cron-based scheduling |
| `release` | On release publish |
| `workflow_call` | Reusable workflow |

### Common Actions (v4+)

| Action | Purpose |
|--------|---------|
| `actions/checkout@v4` | Clone repository |
| `actions/setup-node@v4` | Setup Node.js |
| `actions/setup-python@v5` | Setup Python |
| `actions/cache@v4` | Cache dependencies |
| `actions/upload-artifact@v4` | Upload artifacts |
| `actions/download-artifact@v4` | Download artifacts |
| `docker/build-push-action@v6` | Build/push Docker |

### GITHUB_TOKEN Permissions

```yaml
permissions:
  contents: read      # Default for safety
  packages: write     # For GHCR
  pull-requests: write # For PR comments
  id-token: write     # For OIDC
```

## Decision Tree

```
Need CI/CD for GitHub project?
├── Yes → GitHub Actions
│   ├── Simple project → Basic CI template
│   ├── Multiple environments → Use environments
│   ├── Multiple repos need same workflow → Reusable workflows
│   ├── Common steps repeated → Composite actions
│   └── Complex builds → Matrix strategy
└── No → Consider GitLab CI, Jenkins, or ArgoCD
```

## Related Resources

- [faion-cicd-engineer](../faion-cicd-engineer/CLAUDE.md) - Parent skill
- [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) - DevOps orchestrator

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run terraform plan, docker build, kubectl get commands | haiku | Mechanical CLI operations |
| Review Dockerfile for best practices | sonnet | Code review, security patterns |
| Debug pod crashes, container networking issues | sonnet | Diagnosis and error analysis |
| Design multi-region failover architecture | opus | Complex distributed systems decisions |
| Write Helm values for production rollout | sonnet | Configuration and templating |
| Create monitoring strategy for microservices | opus | System-wide observability design |
| Troubleshoot Kubernetes pod evictions under load | sonnet | Performance debugging and analysis |

---

## Sources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [GitHub Blog - Actions Updates](https://github.blog/news-insights/product-news/lets-talk-about-github-actions/)
- [StepSecurity Best Practices](https://www.stepsecurity.io/blog/github-actions-security-best-practices)
- [GitGuardian Security Cheat Sheet](https://blog.gitguardian.com/github-actions-security-cheat-sheet/)
