---
id: github-actions-basics
name: "GitHub Actions Basics"
domain: OPS
skill: faion-cicd-engineer
category: "devops"
version: "2.0.0"
last_updated: "2026-01"
---

# GitHub Actions Basics

## Overview

GitHub Actions is a CI/CD platform integrated directly into GitHub repositories. It enables automated workflows triggered by events like pushes, pull requests, and releases, with support for matrix builds, reusable workflows, and extensive marketplace actions.

**Platform Scale (2025):** 11.5 billion minutes used in public/open source projects (35% YoY growth), powering 71 million jobs per day.

## When to Use

- Projects hosted on GitHub
- Open source projects needing free CI/CD
- Teams already using GitHub ecosystem
- Workflows requiring GitHub integration (issues, PRs, releases)
- Multi-platform builds (Linux, Windows, macOS)

## Key Concepts

| Concept | Description |
|---------|-------------|
| Workflow | Automated process defined in YAML (`.github/workflows/`) |
| Job | Set of steps running on same runner |
| Step | Individual task (action or shell command) |
| Action | Reusable unit of code (marketplace or custom) |
| Runner | Server executing workflows (GitHub-hosted or self-hosted) |
| Event | Trigger that starts workflow (push, PR, schedule, etc.) |
| Artifact | Files persisted between jobs |
| Secret | Encrypted environment variable |

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

## Core Workflow Events

| Event | Trigger |
|-------|---------|
| `push` | Code pushed to branch |
| `pull_request` | PR opened, updated, or closed |
| `workflow_dispatch` | Manual trigger via UI/API |
| `schedule` | Cron-based scheduling |
| `release` | Release created/published |
| `workflow_call` | Called by another workflow |
| `repository_dispatch` | External API trigger |

## Pricing (2026)

| Runner Type | Change |
|-------------|--------|
| GitHub-hosted | Up to 39% price reduction (Jan 2026) |
| Self-hosted | $0.002/min cloud platform charge (Mar 2026) |
| Public repos | Free |

## Upcoming Features (Q1-Q2 2026)

- Timezone support for scheduled jobs
- Schedule reliability improvements
- **Parallel steps** (most requested feature, targeting mid-2026)

## Files in This Methodology

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Production-ready examples |
| [templates.md](templates.md) | Copy-paste workflow templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for GitHub Actions tasks |

## Related Methodologies

- [github-actions-workflows](../github-actions-workflows/) - Advanced workflow patterns
- [gitops](../gitops/) - GitOps principles
- [argocd-gitops](../argocd-gitops/) - ArgoCD deployment

## Sources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Let's talk about GitHub Actions - GitHub Blog](https://github.blog/news-insights/product-news/lets-talk-about-github-actions/)
- [GitHub Actions Best Practices - Exercism](https://exercism.org/docs/building/github/gha-best-practices)
- [GitHub Actions Security Best Practices - GitGuardian](https://blog.gitguardian.com/github-actions-security-cheat-sheet/)
- [GitHub Actions Security Best Practices - Medium](https://medium.com/@amareswer/github-actions-security-best-practices-1d3f33cdf705)
- [GitHub Actions Best Practices - Datree](https://www.datree.io/resources/github-actions-best-practices)
- [GitHub Changelog - Actions Updates](https://github.blog/changelog/2025-11-06-new-releases-for-github-actions-november-2025/)
- [GitHub Changelog - Pricing Update](https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/)

---

*GitHub Actions Basics v2.0.0 | faion-cicd-engineer*
